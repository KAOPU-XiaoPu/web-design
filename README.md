# web-design

A Claude Code SKILL for designing beautiful, consistent web pages — **spec first, code second**.

Feed it a PRD, a reference URL, or a screenshot. It produces a readable, editable, portable `DESIGN.md` first. Then it generates web code where UI, visuals, motion, and responsiveness all land.

**Live landing page:** [kaopu-xiaopu.github.io/web-design](https://kaopu-xiaopu.github.io/web-design/)

## How it works

**Phase A — Understand.** Extracts design cues from PRD / URL / screenshot / keywords / brand name. A graceful fallback chain keeps it working even with sparse inputs.

**Phase B — Produce `DESIGN.md`.** A full 9-section spec: color, type, component, layout, motion, depth, do's & don'ts, responsive rules, accessibility. Once you approve it, the spec lives in your project and can be edited by hand.

**Phase C — Generate code.** Strictly follows the spec. Self-audits against a 100-score quality checklist. Diff-audits when a reference URL exists.

## Repository layout

```
web-design/
├── SKILL.md            # the skill itself (instructions for Claude)
├── references/         # design systems, style seeds, motion library,
│                       # interaction patterns, quality checklist, etc.
├── scripts/            # Playwright crawler, static token extractor,
│                       # Unsplash image fetcher
└── docs/               # landing page (served via GitHub Pages)
    ├── index.html
    ├── styles.css
    ├── app.js
    ├── DESIGN.md       # this page's own design spec (produced by the SKILL)
    └── images/optimized/
```

## Install

Clone this repo into your Claude Code skills directory:

```bash
git clone https://github.com/KAOPU-XiaoPu/web-design ~/.claude/skills/web-design
```

Claude Code will auto-discover the SKILL the next time you start a session.

## Run the landing page locally

```bash
cd web-design/docs
python3 -m http.server 8000
# open http://localhost:8000
```

Opening `index.html` directly with `file://` won't work — Google Fonts and the OGL ES module need an HTTP origin.

## Credits

Motion effects on the landing page derive from work by David Haz:

- [vue-bits](https://github.com/DavidHDev/vue-bits) (MIT) — GradientBlinds, RollingGallery
- [react-bits](https://github.com/DavidHDev/react-bits) (MIT) — DomeGallery

Reference inspirations for the DESIGN.md structure from [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT).

## License

MIT
