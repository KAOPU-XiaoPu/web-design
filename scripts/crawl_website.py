#!/usr/bin/env python3
"""
crawl_website.py — 使用 Playwright 无头浏览器爬取网站

功能：
1. 真实浏览器渲染（绕过大部分反爬、支持 SPA）
2. 模拟滚动到底部（触发懒加载、scroll-linked 动画）
3. 截图（全页 + 每屏视口截图）
4. 提取渲染后的 CSS 变量、计算样式、字体、颜色
5. 提取页面结构（所有 section、img、外链 CSS）

用法：
  python3 crawl_website.py --url https://example.com --output ./output
  python3 crawl_website.py --url https://linear.app --output ./output --full-page
  python3 crawl_website.py --url https://vercel.com --output ./output --scroll-delay 800

输出：
  output/
  ├── full-page.png          全页截图
  ├── viewport-001.png       第 1 屏截图
  ├── viewport-002.png       第 2 屏截图
  ├── ...
  ├── tokens.json            提取的设计 Token
  ├── structure.json          页面结构（sections, images, css links）
  └── styles.css             所有内联 <style> 和外链 CSS 合并
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright not installed. Run: pip3 install playwright && python3 -m playwright install chromium")
    sys.exit(1)


def crawl(url: str, output_dir: str, scroll_delay: int = 500, full_page: bool = False, viewport_width: int = 1440, viewport_height: int = 900):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="en-US",
        )
        page = context.new_page()

        print(f"[1/6] Navigating to {url}...")
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:
            print("  networkidle timeout, trying domcontentloaded...")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Wait for fonts and images
        page.wait_for_timeout(2000)

        print("[2/6] Scrolling through page...")
        viewport_screenshots = scroll_and_capture(page, output, scroll_delay, viewport_height)
        print(f"  Captured {len(viewport_screenshots)} viewport screenshots")

        # Scroll back to top for full-page screenshot
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)

        if full_page:
            print("[3/6] Taking full-page screenshot...")
            page.screenshot(path=str(output / "full-page.png"), full_page=True)
        else:
            print("[3/6] Taking top screenshot...")
            page.screenshot(path=str(output / "full-page.png"))

        print("[4/6] Extracting design tokens...")
        tokens = extract_tokens(page)
        with open(output / "tokens.json", "w", encoding="utf-8") as f:
            json.dump(tokens, f, indent=2, ensure_ascii=False)

        print("[5/6] Extracting page structure...")
        structure = extract_structure(page, url)
        with open(output / "structure.json", "w", encoding="utf-8") as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)

        print("[6/6] Extracting stylesheets...")
        css = extract_stylesheets(page)
        with open(output / "styles.css", "w", encoding="utf-8") as f:
            f.write(css)

        browser.close()

    print(f"\nDone! Output saved to {output_dir}/")
    print(f"  - {len(viewport_screenshots)} viewport screenshots")
    print(f"  - tokens.json ({len(tokens.get('cssVariables', {}))} CSS vars, {len(tokens.get('colors', []))} colors, {len(tokens.get('fonts', []))} fonts)")
    print(f"  - structure.json ({len(structure.get('sections', []))} sections, {len(structure.get('images', []))} images)")
    print(f"  - styles.css ({len(css)} chars)")


def scroll_and_capture(page, output: Path, scroll_delay: int, viewport_height: int) -> list:
    """Scroll through the page step by step, capturing viewport screenshots."""
    total_height = page.evaluate("document.body.scrollHeight")
    screenshots = []
    scroll_pos = 0
    idx = 1

    while scroll_pos < total_height:
        # Take viewport screenshot
        path = output / f"viewport-{idx:03d}.png"
        page.screenshot(path=str(path))
        screenshots.append(str(path))

        # Scroll one viewport
        scroll_pos += int(viewport_height * 0.85)  # 15% overlap
        page.evaluate(f"window.scrollTo({{ top: {scroll_pos}, behavior: 'smooth' }})")
        page.wait_for_timeout(scroll_delay)

        # Check if page grew (lazy loading / infinite scroll)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height > total_height:
            total_height = new_height

        idx += 1

        # Safety cap
        if idx > 50:
            print("  Warning: hit 50 viewport cap, stopping scroll")
            break

    return screenshots


def extract_tokens(page) -> dict:
    """Extract design tokens from the rendered page."""
    return page.evaluate("""() => {
        const result = {
            cssVariables: {},
            colors: [],
            fonts: [],
            fontSizes: [],
            borderRadii: [],
            shadows: [],
            transitions: [],
            keyframes: [],
        };

        // 1. Extract CSS custom properties from :root
        const rootStyles = getComputedStyle(document.documentElement);
        const sheets = document.styleSheets;
        for (const sheet of sheets) {
            try {
                for (const rule of sheet.cssRules) {
                    if (rule.selectorText === ':root' || rule.selectorText === ':root, :host') {
                        for (const prop of rule.style) {
                            if (prop.startsWith('--')) {
                                result.cssVariables[prop] = rule.style.getPropertyValue(prop).trim();
                            }
                        }
                    }
                    // Collect @keyframes
                    if (rule instanceof CSSKeyframesRule) {
                        result.keyframes.push(rule.name);
                    }
                }
            } catch(e) { /* cross-origin stylesheet */ }
        }

        // 2. Sample computed styles from key elements
        const selectors = ['body', 'h1', 'h2', 'h3', 'p', 'a', 'button', 'nav', 'header', 'footer', 'section', 'main'];
        const colorSet = new Set();
        const fontSet = new Set();
        const fontSizeSet = new Set();
        const radiusSet = new Set();
        const shadowSet = new Set();
        const transitionSet = new Set();

        for (const sel of selectors) {
            const els = document.querySelectorAll(sel);
            for (const el of Array.from(els).slice(0, 5)) {
                const s = getComputedStyle(el);

                // Colors
                [s.color, s.backgroundColor, s.borderColor].forEach(c => {
                    if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') colorSet.add(c);
                });

                // Fonts
                if (s.fontFamily) fontSet.add(s.fontFamily.split(',')[0].trim().replace(/['"]/g, ''));

                // Font sizes
                if (s.fontSize) fontSizeSet.add(s.fontSize);

                // Border radius
                if (s.borderRadius && s.borderRadius !== '0px') radiusSet.add(s.borderRadius);

                // Shadows
                if (s.boxShadow && s.boxShadow !== 'none') shadowSet.add(s.boxShadow);

                // Transitions
                if (s.transition && s.transition !== 'all 0s ease 0s') transitionSet.add(s.transition);
            }
        }

        result.colors = [...colorSet];
        result.fonts = [...fontSet];
        result.fontSizes = [...fontSizeSet].sort((a, b) => parseFloat(a) - parseFloat(b));
        result.borderRadii = [...radiusSet];
        result.shadows = [...shadowSet];
        result.transitions = [...transitionSet];

        // 3. Google Fonts detection
        const fontLinks = document.querySelectorAll('link[href*="fonts.googleapis.com"]');
        result.googleFonts = Array.from(fontLinks).map(l => l.href);

        // Also check @import in stylesheets
        for (const sheet of sheets) {
            try {
                for (const rule of sheet.cssRules) {
                    if (rule instanceof CSSImportRule && rule.href && rule.href.includes('fonts.googleapis.com')) {
                        result.googleFonts.push(rule.href);
                    }
                }
            } catch(e) {}
        }

        return result;
    }""")


def extract_structure(page, base_url: str) -> dict:
    """Extract page structure: sections, images, CSS links, JS libraries."""
    return page.evaluate("""(baseUrl) => {
        const result = {
            title: document.title,
            sections: [],
            images: [],
            cssLinks: [],
            jsLibraries: [],
            navLinks: [],
        };

        // Sections
        const sectionEls = document.querySelectorAll('section, [class*="section"], header, footer, main, [role="main"]');
        sectionEls.forEach((el, i) => {
            result.sections.push({
                index: i,
                tag: el.tagName.toLowerCase(),
                id: el.id || null,
                className: el.className ? el.className.toString().slice(0, 100) : null,
                rect: {
                    top: Math.round(el.getBoundingClientRect().top + window.scrollY),
                    height: Math.round(el.getBoundingClientRect().height),
                },
            });
        });

        // Images
        document.querySelectorAll('img[src]').forEach(img => {
            let src = img.src;
            if (src && !src.startsWith('data:')) {
                result.images.push({
                    src: src,
                    alt: img.alt || '',
                    width: img.naturalWidth,
                    height: img.naturalHeight,
                });
            }
        });

        // CSS background images
        const allEls = document.querySelectorAll('*');
        for (const el of Array.from(allEls).slice(0, 500)) {
            const bg = getComputedStyle(el).backgroundImage;
            if (bg && bg !== 'none' && bg.includes('url(')) {
                const match = bg.match(/url\\(['"]?(.+?)['"]?\\)/);
                if (match && !match[1].startsWith('data:')) {
                    result.images.push({ src: match[1], alt: '', type: 'css-background' });
                }
            }
        }

        // CSS links
        document.querySelectorAll('link[rel="stylesheet"]').forEach(l => {
            result.cssLinks.push(l.href);
        });

        // JS libraries detection
        const scripts = document.querySelectorAll('script[src]');
        const libPatterns = ['gsap', 'scrolltrigger', 'lenis', 'locomotive', 'three', 'framer-motion', 'animejs', 'barba'];
        scripts.forEach(s => {
            const src = s.src.toLowerCase();
            for (const lib of libPatterns) {
                if (src.includes(lib)) {
                    result.jsLibraries.push({ name: lib, src: s.src });
                }
            }
        });

        // Also check inline scripts for library references
        document.querySelectorAll('script:not([src])').forEach(s => {
            const text = s.textContent.toLowerCase();
            for (const lib of libPatterns) {
                if (text.includes(lib)) {
                    result.jsLibraries.push({ name: lib, src: 'inline' });
                }
            }
        });

        // Nav links
        document.querySelectorAll('nav a, header a').forEach(a => {
            result.navLinks.push({ text: a.textContent.trim(), href: a.href });
        });

        return result;
    }""", base_url)


def extract_stylesheets(page) -> str:
    """Extract all inline styles and same-origin stylesheet content."""
    return page.evaluate("""() => {
        let css = '';

        // Inline <style> tags
        document.querySelectorAll('style').forEach(s => {
            css += '/* === inline <style> === */\\n' + s.textContent + '\\n\\n';
        });

        // Same-origin stylesheets
        for (const sheet of document.styleSheets) {
            try {
                const rules = sheet.cssRules;
                if (rules && rules.length > 0) {
                    const href = sheet.href || 'inline';
                    if (!css.includes(Array.from(rules).slice(0, 3).map(r => r.cssText).join(''))) {
                        css += '/* === ' + href + ' === */\\n';
                        for (const rule of rules) {
                            css += rule.cssText + '\\n';
                        }
                        css += '\\n';
                    }
                }
            } catch(e) {
                // Cross-origin, skip
                if (sheet.href) {
                    css += '/* === CROSS-ORIGIN (cannot read): ' + sheet.href + ' === */\\n\\n';
                }
            }
        }

        return css;
    }""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl a website using headless Chromium")
    parser.add_argument("--url", required=True, help="URL to crawl")
    parser.add_argument("--output", default="./crawl-output", help="Output directory")
    parser.add_argument("--scroll-delay", type=int, default=500, help="Delay between scroll steps in ms (default: 500)")
    parser.add_argument("--full-page", action="store_true", help="Take full-page screenshot (can be very tall)")
    parser.add_argument("--width", type=int, default=1440, help="Viewport width (default: 1440)")
    parser.add_argument("--height", type=int, default=900, help="Viewport height (default: 900)")

    args = parser.parse_args()
    crawl(args.url, args.output, args.scroll_delay, args.full_page, args.width, args.height)
