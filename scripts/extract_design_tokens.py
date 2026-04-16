#!/usr/bin/env python3
"""
Design Token Extractor

Extract design tokens, page structure, and image assets from HTML/CSS.
When the input is HTML, linked stylesheets are fetched and merged automatically.

Usage:
    python extract_design_tokens.py --file page.html
    python extract_design_tokens.py --url https://example.com
    cat page.html | python extract_design_tokens.py --stdin --base-url https://example.com
    python extract_design_tokens.py --file styles.css --format json
"""

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


BASE_FONT_SIZE_PX = 16
DEFAULT_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (compatible; design-token-extractor/1.0)"


def dedupe(items):
    seen = set()
    result = []
    for item in items:
        marker = json.dumps(item, sort_keys=True, ensure_ascii=False) if isinstance(item, dict) else item
        if marker in seen:
            continue
        seen.add(marker)
        result.append(item)
    return result


def read_text_from_url(url, timeout=DEFAULT_TIMEOUT):
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
            charset = response.headers.get_content_charset()
    except Exception:
        # Fallback to curl because some sites work in curl but fail urllib TLS validation
        # in local environments with incomplete certificate chains.
        result = subprocess.run(
            ["curl", "-Ls", "--max-time", str(timeout), url],
            capture_output=True,
            text=False,
            check=True,
        )
        raw = result.stdout
        charset = None

    encodings = [charset, "utf-8", "latin-1"]
    for encoding in encodings:
        if not encoding:
            continue
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def load_text(source, timeout=DEFAULT_TIMEOUT):
    parsed = urlparse(source)
    if parsed.scheme in {"http", "https"}:
        return read_text_from_url(source, timeout=timeout)
    return Path(source).read_text(encoding="utf-8")


def resolve_reference(ref, base_source):
    if not ref:
        return None

    ref = ref.strip().strip("'\"")
    if not ref:
        return None

    parsed_ref = urlparse(ref)
    if parsed_ref.scheme in {"http", "https", "data"}:
        return ref
    if parsed_ref.scheme in {"mailto", "javascript", "tel"}:
        return None
    if not base_source:
        return ref

    parsed_base = urlparse(base_source)
    if parsed_base.scheme in {"http", "https"}:
        return urljoin(base_source, ref)

    base_path = Path(base_source)
    base_dir = base_path if base_path.is_dir() else base_path.parent
    return str((base_dir / ref).resolve())


def looks_like_html(content):
    lowered = content.lower()
    return any(tag in lowered for tag in ("<html", "<body", "<div", "<section", "<head"))


def is_image_reference(ref):
    cleaned = ref.strip().strip("'\"")
    if cleaned.startswith("data:image/"):
        return True
    path = urlparse(cleaned).path.lower()
    image_exts = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif", ".bmp", ".ico")
    return path.endswith(image_exts)


def extract_css_url_refs(css_text):
    refs = re.findall(r'url\((.*?)\)', css_text, re.IGNORECASE)
    cleaned = []
    for ref in refs:
        value = ref.strip().strip("'\"")
        if not value or value.startswith("data:"):
            continue
        cleaned.append(value)
    return dedupe(cleaned)


def css_values_to_px(values):
    px_values = []
    for value in values:
        for number, unit in re.findall(r'(\d+(?:\.\d+)?)\s*(px|rem|em)\b', value, re.IGNORECASE):
            multiplier = {"px": 1, "rem": BASE_FONT_SIZE_PX, "em": BASE_FONT_SIZE_PX}[unit.lower()]
            px_values.append(int(round(float(number) * multiplier)))
    return px_values


def normalize_text_value(value):
    return re.sub(r"\s+", " ", value).strip().strip("'\"")


def normalize_font_family(value):
    return re.sub(r"\s+", " ", value).strip().replace('"', "").replace("'", "")


class ResourceHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.css_links = []
        self.google_font_links = []
        self.images = []
        self.modules = []
        self.script_links = []
        self.inline_styles = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        href = attrs.get("href")
        src = attrs.get("src")
        rel = (attrs.get("rel") or "").lower()

        if "style" in attrs:
            self.inline_styles.append(attrs["style"])

        if tag == "link" and href:
            if "fonts.googleapis.com" in href:
                self.google_font_links.append(href)
            if "stylesheet" in rel or href.lower().split("?")[0].endswith(".css"):
                self.css_links.append(href)

        if tag == "img" and src:
            self.images.append(src)

        if tag in {"header", "section", "footer", "main"}:
            self.modules.append(
                {
                    "tag": tag,
                    "id": attrs.get("id"),
                    "class": attrs.get("class"),
                }
            )

        if tag == "script" and src:
            self.script_links.append(src)


def gather_external_css(css_links, base_source, timeout=DEFAULT_TIMEOUT, fetch_external=True):
    resolved_links = []
    css_sources = []
    errors = []

    for href in dedupe(css_links):
        resolved = resolve_reference(href, base_source)
        resolved_links.append({"href": href, "resolved": resolved})

        if not fetch_external or not resolved or urlparse(resolved).scheme == "data":
            continue

        try:
            css_text = load_text(resolved, timeout=timeout)
        except Exception as exc:
            errors.append({"source": resolved, "error": str(exc)})
            continue

        css_sources.append((resolved, css_text))

    return resolved_links, css_sources, errors


def analyze_html(html_text, source=None, fetch_external=True, timeout=DEFAULT_TIMEOUT):
    parser = ResourceHTMLParser()
    parser.feed(html_text)

    style_blocks = re.findall(r'<style\b[^>]*>(.*?)</style>', html_text, re.IGNORECASE | re.DOTALL)
    inline_css_chunks = [(source or "inline", block) for block in style_blocks]
    if parser.inline_styles:
        inline_css_chunks.extend((source or "inline", style) for style in parser.inline_styles)

    external_css_links, external_css_sources, fetch_errors = gather_external_css(
        parser.css_links,
        source,
        timeout=timeout,
        fetch_external=fetch_external,
    )

    css_sources = inline_css_chunks + external_css_sources
    combined_css = "\n".join(chunk for _, chunk in css_sources)

    html_images = []
    for ref in dedupe(parser.images):
        html_images.append({"raw": ref, "resolved": resolve_reference(ref, source)})

    css_background_images = []
    for css_source, css_text in css_sources:
        for ref in extract_css_url_refs(css_text):
            if not is_image_reference(ref):
                continue
            css_background_images.append(
                {
                    "raw": ref,
                    "resolved": resolve_reference(ref, css_source or source),
                    "from": css_source,
                }
            )

    script_links = []
    for ref in dedupe(parser.script_links):
        script_links.append({"raw": ref, "resolved": resolve_reference(ref, source)})

    all_images = dedupe(
        [item["resolved"] for item in html_images + css_background_images if item.get("resolved")]
    )

    return {
        "css_content": combined_css,
        "structure": {
            "modules": parser.modules,
            "module_count": len(parser.modules),
            "script_links": script_links,
        },
        "assets": {
            "html_images": html_images,
            "css_background_images": dedupe(css_background_images),
            "all_images": all_images,
        },
        "meta": {
            "external_css_links": external_css_links,
            "fetched_css_files": [{"source": source_ref, "length": len(text)} for source_ref, text in external_css_sources],
            "google_fonts_links": dedupe(parser.google_font_links),
            "fetch_errors": fetch_errors,
        },
    }


def extract_colors(css_text):
    hex_colors = re.findall(r'#(?:[0-9a-fA-F]{3,8})\b', css_text)
    rgb_colors = re.findall(r'rgba?\([^)]+\)', css_text)
    hsl_colors = re.findall(r'hsla?\([^)]+\)', css_text)
    css_vars = re.findall(r'--[\w-]*color[\w-]*:\s*([^;}{]+)', css_text, re.IGNORECASE)
    css_color_vars = re.findall(
        r'--[\w-]*(?:bg|background|text|border|accent|primary|secondary)[\w-]*:\s*([^;}{]+)',
        css_text,
        re.IGNORECASE,
    )

    all_hex = [color.upper() for color in hex_colors]
    color_freq = Counter(all_hex).most_common(20)

    neutral_colors = {
        "#000",
        "#000000",
        "#FFF",
        "#FFFFFF",
        "#333",
        "#333333",
        "#666",
        "#666666",
        "#999",
        "#999999",
        "#CCC",
        "#CCCCCC",
        "#EEE",
        "#EEEEEE",
        "#F5F5F5",
        "#FAFAFA",
    }
    accent_colors = [(color, freq) for color, freq in color_freq if color not in neutral_colors]

    return {
        "all_hex_colors": color_freq[:20],
        "accent_colors": accent_colors[:10],
        "rgb_colors": dedupe(rgb_colors)[:10],
        "hsl_colors": dedupe(hsl_colors)[:10],
        "css_color_variables": dedupe([normalize_text_value(value) for value in css_vars + css_color_vars])[:20],
        "analysis": {
            "total_unique_colors": len(set(all_hex)),
            "likely_primary": accent_colors[0][0] if accent_colors else None,
            "likely_secondary": accent_colors[1][0] if len(accent_colors) > 1 else None,
        },
    }


def extract_fonts(css_text):
    font_families = re.findall(r'font-family:\s*([^;}{]+)', css_text)
    google_font_urls = re.findall(r'https?://fonts\.googleapis\.com[^"\'\s)]+', css_text)
    google_font_imports = re.findall(
        r'@import\s+url\(([^)]*fonts\.googleapis\.com[^)]*)\)',
        css_text,
        re.IGNORECASE,
    )
    font_sizes = re.findall(r'font-size:\s*([^;}{]+)', css_text)
    font_weights = re.findall(r'font-weight:\s*([^;}{]+)', css_text)
    line_heights = re.findall(r'line-height:\s*([^;}{]+)', css_text)
    letter_spacings = re.findall(r'letter-spacing:\s*([^;}{]+)', css_text)

    cleaned_families = dedupe([normalize_font_family(family) for family in font_families])
    cleaned_google_font_urls = dedupe([normalize_text_value(url) for url in google_font_urls + google_font_imports])

    return {
        "font_families": cleaned_families[:10],
        "google_fonts_urls": cleaned_google_font_urls[:10],
        "font_sizes": Counter([size.strip() for size in font_sizes]).most_common(10),
        "font_weights": Counter([weight.strip() for weight in font_weights]).most_common(5),
        "line_heights": dedupe([height.strip() for height in line_heights])[:10],
        "letter_spacings": dedupe([spacing.strip() for spacing in letter_spacings])[:10],
    }


def extract_spacing(css_text):
    paddings = re.findall(r'padding(?:-\w+)?:\s*([^;}{]+)', css_text)
    margins = re.findall(r'margin(?:-\w+)?:\s*([^;}{]+)', css_text)
    gaps = re.findall(r'gap:\s*([^;}{]+)', css_text)

    raw_values = paddings + margins + gaps
    px_values = css_values_to_px(raw_values)

    return {
        "common_values_raw": Counter([value.strip() for value in raw_values]).most_common(15),
        "common_values_px": Counter(px_values).most_common(15),
        "spacing_scale_px": sorted(set(px_values))[:20],
        "gap_values": dedupe([gap.strip() for gap in gaps])[:10],
    }


def extract_border_radius(css_text):
    radii = re.findall(r'border-radius:\s*([^;}{]+)', css_text)
    return {"values": Counter([radius.strip() for radius in radii]).most_common(10)}


def extract_shadows(css_text):
    shadows = re.findall(r'box-shadow:\s*([^;}{]+)', css_text)
    cleaned = [shadow.strip() for shadow in shadows if shadow.strip() != "none"]
    return {"values": Counter(cleaned).most_common(10), "total_unique": len(set(cleaned))}


def extract_animations(css_text):
    transitions = re.findall(r'transition:\s*([^;}{]+)', css_text)
    animations = re.findall(r'animation:\s*([^;}{]+)', css_text)
    keyframes = re.findall(r'@keyframes\s+([\w-]+)', css_text)
    transforms = re.findall(r'transform:\s*([^;}{]+)', css_text)

    return {
        "transitions": dedupe([value.strip() for value in transitions])[:20],
        "animations": dedupe([value.strip() for value in animations])[:20],
        "keyframe_names": dedupe(keyframes),
        "transforms": Counter([value.strip() for value in transforms]).most_common(10),
    }


def extract_css_variables(css_text):
    variables = re.findall(r'(--[\w-]+):\s*([^;}{]+)', css_text)
    unique_variables = []
    seen = set()
    for name, value in variables:
        if name in seen:
            continue
        seen.add(name)
        unique_variables.append((name, value.strip()))

    return {
        "variables": unique_variables[:50],
        "total": len(unique_variables),
    }


def extract_all_tokens(content, source=None, fetch_external=True, timeout=DEFAULT_TIMEOUT):
    if looks_like_html(content):
        analysis = analyze_html(content, source=source, fetch_external=fetch_external, timeout=timeout)
        css_content = analysis["css_content"]
        structure = analysis["structure"]
        assets = analysis["assets"]
        meta = analysis["meta"]
    else:
        css_content = content
        css_background_images = []
        for ref in extract_css_url_refs(css_content):
            if not is_image_reference(ref):
                continue
            css_background_images.append(
                {
                    "raw": ref,
                    "resolved": resolve_reference(ref, source),
                    "from": source,
                }
            )

        structure = {"modules": [], "module_count": 0, "script_links": []}
        assets = {
            "html_images": [],
            "css_background_images": dedupe(css_background_images),
            "all_images": dedupe([item["resolved"] for item in css_background_images if item.get("resolved")]),
        }
        meta = {
            "external_css_links": [],
            "fetched_css_files": [],
            "google_fonts_links": [],
            "fetch_errors": [],
        }

    return {
        "colors": extract_colors(css_content),
        "typography": extract_fonts(css_content),
        "spacing": extract_spacing(css_content),
        "borderRadius": extract_border_radius(css_content),
        "shadows": extract_shadows(css_content),
        "animations": extract_animations(css_content),
        "cssVariables": extract_css_variables(css_content),
        "structure": structure,
        "assets": assets,
        "meta": {
            "source": source,
            "external_css_links": meta["external_css_links"],
            "fetched_css_files": meta["fetched_css_files"],
            "google_fonts_links": meta["google_fonts_links"],
            "fetch_errors": meta["fetch_errors"],
            "total_css_length": len(css_content),
        },
    }


def format_summary(tokens):
    lines = []
    lines.append("=" * 60)
    lines.append("DESIGN TOKEN EXTRACTION SUMMARY")
    lines.append("=" * 60)

    lines.append("\n[STRUCTURE]")
    lines.append(f"  Modules found: {tokens['structure']['module_count']}")
    for module in tokens["structure"]["modules"][:10]:
        parts = [module["tag"]]
        if module.get("id"):
            parts.append(f"id={module['id']}")
        if module.get("class"):
            parts.append(f"class={module['class']}")
        lines.append(f"    - {' '.join(parts)}")

    lines.append("\n[ASSETS]")
    lines.append(f"  HTML images: {len(tokens['assets']['html_images'])}")
    lines.append(f"  CSS background images: {len(tokens['assets']['css_background_images'])}")
    lines.append(f"  Total unique images: {len(tokens['assets']['all_images'])}")

    lines.append("\n[COLORS]")
    if tokens["colors"]["analysis"]["likely_primary"]:
        lines.append(f"  Primary (likely): {tokens['colors']['analysis']['likely_primary']}")
    if tokens["colors"]["analysis"]["likely_secondary"]:
        lines.append(f"  Secondary (likely): {tokens['colors']['analysis']['likely_secondary']}")
    lines.append(f"  Total unique hex colors: {tokens['colors']['analysis']['total_unique_colors']}")
    for color, freq in tokens["colors"]["all_hex_colors"][:8]:
        lines.append(f"    {color}: {freq}x")

    lines.append("\n[TYPOGRAPHY]")
    lines.append(f"  Font families: {', '.join(tokens['typography']['font_families'][:5])}")
    if tokens["typography"]["google_fonts_urls"]:
        lines.append(f"  Google Fonts URLs: {len(tokens['typography']['google_fonts_urls'])}")
    for size, freq in tokens["typography"]["font_sizes"][:6]:
        lines.append(f"    {size}: {freq}x")

    lines.append("\n[SPACING]")
    lines.append(f"  Common px values: {[value for value, _ in tokens['spacing']['common_values_px'][:10]]}")

    lines.append("\n[BORDER RADIUS]")
    for radius, freq in tokens["borderRadius"]["values"][:5]:
        lines.append(f"  {radius}: {freq}x")

    lines.append(f"\n[SHADOWS] {tokens['shadows']['total_unique']} unique")
    for shadow, freq in tokens["shadows"]["values"][:3]:
        lines.append(f"  {shadow[:70]}...: {freq}x")

    lines.append("\n[ANIMATIONS]")
    if tokens["animations"]["keyframe_names"]:
        lines.append(f"  Keyframes: {', '.join(tokens['animations']['keyframe_names'][:8])}")
    if tokens["animations"]["transitions"]:
        lines.append(f"  Transitions: {len(tokens['animations']['transitions'])} unique")

    lines.append(f"\n[CSS VARIABLES] {tokens['cssVariables']['total']} total")
    for name, value in tokens["cssVariables"]["variables"][:10]:
        lines.append(f"  {name}: {value[:60]}")

    if tokens["meta"]["external_css_links"]:
        lines.append("\n[EXTERNAL CSS]")
        lines.append(f"  Linked CSS files: {len(tokens['meta']['external_css_links'])}")
        lines.append(f"  Successfully fetched: {len(tokens['meta']['fetched_css_files'])}")

    if tokens["meta"]["fetch_errors"]:
        lines.append("\n[FETCH ERRORS]")
        for error in tokens["meta"]["fetch_errors"][:5]:
            lines.append(f"  {error['source']}: {error['error']}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract design tokens from HTML/CSS")
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--file", type=str, help="Local HTML or CSS file path")
    source_group.add_argument("--url", type=str, help="Remote page URL")
    source_group.add_argument("--stdin", action="store_true", help="Read HTML/CSS from stdin")
    parser.add_argument("--base-url", type=str, help="Resolve relative links against this URL or local file path when using --stdin")
    parser.add_argument("--format", type=str, choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--no-fetch", action="store_true", help="Do not fetch linked stylesheets from HTML")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout in seconds")
    args = parser.parse_args()

    if args.url:
        source = args.url
        content = load_text(args.url, timeout=args.timeout)
    elif args.file:
        source = str(Path(args.file).resolve())
        content = load_text(source, timeout=args.timeout)
    else:
        source = args.base_url
        content = sys.stdin.read()

    tokens = extract_all_tokens(
        content,
        source=source,
        fetch_external=not args.no_fetch,
        timeout=args.timeout,
    )

    if args.format == "json":
        print(json.dumps(tokens, indent=2, ensure_ascii=False))
    else:
        print(format_summary(tokens))


if __name__ == "__main__":
    main()
