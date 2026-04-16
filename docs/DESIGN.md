# DESIGN.md

> 先出规范，再出代码。—— 一份为「方法论本身」而设计的页面。

**项目**：web-design SKILL 开源介绍页
**定位**：让 AI 做网页，产出一份可读、可改、可传递的设计规范（DESIGN.md）
**参考起点**：hueapp.io（暗色编辑风，克制软光感）——沿用其骨架，改强调色与字体组合以建立自我识别

---

## 1. Visual Theme & Atmosphere

**Style**: Dark Editorial × Design System × Cinematic Scroll
**Keywords**: 克制、编辑、方法论、软光感、文档感、精密、可读、可信、电影式
**Tone**: 深色但不冷峻、技术但不赛博、**信息密度 Stripe 级 + 签名动效 Apple 级 + 骨架 Linear 级** — NOT 霓虹、朋克、花哨、营销感
**Feel**: 一本打开的深色技术手册，每翻一页都有一处值得驻足的视觉瞬间 — 但书还是书，不是游戏

**Interaction Tier**: **L3 沉浸体验 · 电影级 scroll-story**（对标 doubao.com/about 叙事密度，保持暗色编辑骨架）
**Dependencies**: GSAP 3 + ScrollTrigger + Lenis + **Three.js**（WebGL 签名时刻）+ OGL（Aurora 背景）+ CSS `@property` + CSS 3D transforms

**Scroll-story 招式覆盖**（对照 `references/scroll-story-patterns.md`）：
- ✅ **Pattern 1 卡片星座 Hero** → 12 张 DESIGN.md 样本卡在 3D 空间浮动
- ✅ **Pattern 2 卡片汇聚过渡** → Hero → Why 区所有卡片飞向中心合并成一张
- ✅ **Pattern 3 左 pin / 右 swap** → Three Inputs 与 Phase A→B→C 两处用这模式
- ✅ **Pattern 4 WebGL 3D 签名** → "What's Inside" 用 Three.js iridescent torus-knot 替代 CSS cube
- ✅ **Pattern 5 标题光晕** → Section 大标题带 `::before` ghost
- ✅ **Pattern 6 抽象艺术顶** → Feature 卡片顶部是 mesh gradient art

**Motion Library 选型**（从 [vue-bits](https://github.com/DavidHDev/vue-bits) 直接移植，MIT）：

| 类别 | 选用 | 落点 |
|------|------|------|
| Background（氛围层） | **Aurora** | Hero 全屏背景（柔软极光流动，编辑暗色首选） |
| Text — Hero H1 | **SplitText** + **ShinyText** | H1 按字符 stagger 入场；关键词"规范""代码"用 Shiny 金属光扫过 |
| Text — Section H2 | **ScrollFloat** | 每个 section 的 H2 滚动到视口时逐字浮入 |
| Text — Body / Label | **ScrollReveal**（正文段落）+ **ScrambleText**（eyebrow labels）+ **TextType**（Install 代码块） | 三个不同粒度覆盖正文、标签、代码 |
| Animation — 元素级 | **Magnet** + **GlareHover** + **ClickSpark** | CTA 磁吸；卡片 hover 光扫；按钮点击粒子溅射 |
| Component — 交互构件 | **CardSwap**（Hero 右侧 3D 卡片堆）+ **SpotlightCard**（What's Inside 卡片）+ **InfiniteScroll**（Showcase 作品条）+ **MagicBento**（Why 对比网格） | 4 个组件分担 4 段叙事 |

**累计 signature moments: 10+**（Hero 3 处 + Phase pin 1 处 + 每个 section 1-2 处）

---

## 2. Color Palette & Roles

```css
:root {
  /* Backgrounds — 比 hueapp 再暗半档，强化"深色手册"气质 */
  --bg: #0a0b0e;
  --bg-2: #07080b;
  --surface-1: #111217;
  --surface-2: #171921;
  --surface-3: #1f222d;
  --surface-hover: #242836;

  /* Borders */
  --border: rgba(67, 70, 81, 0.5);
  --border-strong: rgba(67, 70, 81, 0.9);
  --border-accent: rgba(94, 234, 212, 0.3);

  /* Text — 四级层次 */
  --text-1: #ebecef;
  --text-2: #c6c9d2;
  --text-3: #8d909c;
  --text-4: #60636f;

  /* Accent — 冷青 + 暖橙（规范 × 温度） */
  --accent-cool: #5EEAD4;
  --accent-cool-hover: #8CF5E3;
  --accent-cool-soft: rgba(94, 234, 212, 0.12);

  --accent-warm: #FB923C;
  --accent-warm-hover: #FDB874;
  --accent-warm-soft: rgba(251, 146, 60, 0.12);

  /* Gradient — 关键词装饰专用，不泛用 */
  --gradient-key: linear-gradient(135deg, #5EEAD4 0%, #FB923C 100%);

  /* RGB variants */
  --bg-rgb: 10, 11, 14;
  --accent-cool-rgb: 94, 234, 212;
  --accent-warm-rgb: 251, 146, 60;

  /* Semantic */
  --success: #5EEAD4;
  --error: #F87171;
  --warning: #FB923C;
}
```

**Color Rules**:
- 所有颜色通过 CSS 变量引用，严格禁止硬编码 hex
- 冷青 & 暖橙**只用在强调位**（CTA、关键词、选中态、hover 辅助）；大面积着色一律用 surface
- **渐变（`--gradient-key`）只用于 1-2 个核心词**（"规范"、"100 分"、"DESIGN.md"）— 一屏不超过一处
- 同一 section 内只有一种强调色系主导；冷/暖同时出现时留白区分
- 文字颜色按层级：标题 `--text-1`、正文 `--text-2`、辅助 `--text-3`、标签 `--text-4`

---

## 3. Typography Rules

**Font Stack**:
```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400..700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');

--font-ui: 'DM Sans', system-ui, -apple-system, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif;
--font-serif: 'Instrument Serif', 'Noto Serif SC', Georgia, serif;
--font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
```

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
| Hero H1 | DM Sans | `clamp(48px, 6vw, 84px)` | 700 | 1.05 | -0.02em |
| Hero Serif Accent | Instrument Serif (italic) | inherit | 400 | 1.05 | 0 |
| Section H2 | DM Sans | `clamp(28px, 3.2vw, 42px)` | 700 | 1.15 | -0.015em |
| H3 | DM Sans | 22px | 600 | 1.3 | -0.01em |
| Eyebrow Label | DM Sans | 13px | 500 | 1.4 | 0.08em (uppercase) |
| Body Lg | DM Sans | 17px | 400 | 1.6 | 0 |
| Body | DM Sans | 15px | 400 | 1.65 | 0 |
| Small | DM Sans | 13px | 500 | 1.5 | 0 |
| Micro | DM Sans | 11px | 500 | 1.4 | 0.06em (uppercase) |
| Code / Mono | JetBrains Mono | 14px | 500 | 1.5 | 0 |
| Serif Quote | Instrument Serif | 28-36px | 400 (italic) | 1.3 | 0 |

**Typography Rules**:
- 正文 heading 一律 DM Sans；**Instrument Serif 仅用于关键词的斜体装饰**（如 "*design*.md"、"*100 分*"），一页不超 3 处
- Heading weight ≥ 600（hero 700）
- 中文内容时：字体栈自动 fallback 到 Noto Sans SC，行高 ≥ 1.7，字距 0.02em
- **NEVER use**: Arial, Times New Roman, Comic Sans, 任何艺术字体

**Text Decoration**（按 `text-decoration-rules.md` 决策）:
- Hero H1：关键词（"规范"、"代码"）用 `--gradient-key` 填充，**无投影**（深色底 + 大字不需要）
- Section H2：纯色 `--text-1`，无渐变无投影
- H3 / Body：纯色，无任何装饰

---

## 4. Component Stylings

### Buttons

```css
/* Primary — 冷青填充，关键 CTA */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 9999px;
  background: var(--accent-cool);
  color: var(--bg);
  font: 500 14px/1 var(--font-ui);
  letter-spacing: -0.005em;
  border: 1px solid var(--accent-cool);
  cursor: pointer;
  transition: transform 0.22s cubic-bezier(.2,0,0,1),
              background 0.12s cubic-bezier(.2,0,0,1),
              box-shadow 0.22s cubic-bezier(.2,0,0,1);
}
.btn-primary:hover {
  background: var(--accent-cool-hover);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(var(--accent-cool-rgb), 0.25);
}
.btn-primary:active { transform: translateY(0); }
.btn-primary:focus-visible { outline: 2px solid var(--accent-cool); outline-offset: 3px; }
.btn-primary:disabled { opacity: 0.45; cursor: not-allowed; transform: none; box-shadow: none; }

/* Ghost — 边框版，次级 CTA */
.btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 11px 19px;
  border-radius: 9999px;
  background: transparent;
  color: var(--text-1);
  border: 1px solid var(--border-strong);
  font: 500 14px/1 var(--font-ui);
  cursor: pointer;
  transition: background 0.12s, border-color 0.12s, transform 0.22s;
}
.btn-ghost:hover { background: var(--surface-2); border-color: var(--text-3); transform: translateY(-1px); }
.btn-ghost:active { transform: translateY(0); }
.btn-ghost:focus-visible { outline: 2px solid var(--accent-cool); outline-offset: 3px; }

/* Pill — 小标签按钮，三步简述用 */
.pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px;
  border-radius: 9999px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  color: var(--text-2);
  font: 500 12px/1 var(--font-mono);
}
```

### Cards

```css
.card {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  transition: background 0.22s cubic-bezier(.2,0,0,1),
              border-color 0.22s cubic-bezier(.2,0,0,1),
              transform 0.22s cubic-bezier(.2,0,0,1);
}
.card:hover {
  background: var(--surface-2);
  border-color: var(--border-strong);
  transform: translateY(-2px);
}
.card:focus-within { border-color: var(--accent-cool); }

/* Feature card with accent icon slot */
.card .card-icon {
  width: 36px; height: 36px;
  border-radius: 8px;
  background: var(--accent-cool-soft);
  color: var(--accent-cool);
  display: inline-flex; align-items: center; justify-content: center;
  margin-bottom: 16px;
}
.card .card-title { font: 600 18px/1.3 var(--font-ui); color: var(--text-1); margin: 0 0 6px; }
.card .card-body  { font: 400 14px/1.6 var(--font-ui); color: var(--text-3); margin: 0; }
```

### Navigation

```css
.nav {
  position: sticky; top: 0; z-index: 50;
  padding: 14px 0;
  background: transparent;
  border-bottom: 1px solid transparent;
  transition: background 0.22s, border-color 0.22s, backdrop-filter 0.22s;
}
.nav.is-scrolled {
  background: rgba(var(--bg-rgb), 0.72);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom-color: var(--border);
}
.nav-link {
  color: var(--text-3);
  font: 500 14px/1 var(--font-ui);
  transition: color 0.12s;
}
.nav-link:hover { color: var(--text-1); }
.nav-link.is-active { color: var(--accent-cool); }
```

### Links

```css
.link {
  color: var(--accent-cool);
  text-decoration: none;
  background-image: linear-gradient(var(--accent-cool), var(--accent-cool));
  background-size: 0% 1px;
  background-position: 0 100%;
  background-repeat: no-repeat;
  transition: background-size 0.28s cubic-bezier(.2,0,0,1), color 0.12s;
}
.link:hover { background-size: 100% 1px; color: var(--accent-cool-hover); }
.link:focus-visible { outline: 2px solid var(--accent-cool); outline-offset: 3px; border-radius: 2px; }
```

### Tags / Badges

```css
.tag {
  display: inline-flex; align-items: center;
  padding: 4px 10px;
  border-radius: 9999px;
  background: var(--accent-cool-soft);
  color: var(--accent-cool);
  font: 500 11px/1.4 var(--font-mono);
  letter-spacing: 0.04em;
}
.tag.tag-warm { background: var(--accent-warm-soft); color: var(--accent-warm); }
.tag.tag-neutral { background: var(--surface-2); color: var(--text-3); border: 1px solid var(--border); }
```

### Code Block / Install Command

```css
.codeblock {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 18px;
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: 12px;
  font: 500 14px/1 var(--font-mono);
  color: var(--text-2);
}
.codeblock .prompt { color: var(--text-4); user-select: none; }
.codeblock .copy-btn {
  margin-left: auto;
  padding: 6px 10px;
  font: 500 11px/1 var(--font-mono);
  color: var(--text-3);
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 6px;
  cursor: pointer;
  transition: color 0.12s, border-color 0.12s;
}
.codeblock .copy-btn:hover { color: var(--accent-cool); border-color: var(--accent-cool); }
.codeblock .copy-btn.is-copied { color: var(--accent-cool); }
```

### Step Indicator (三步简述专用)

```css
.steps { display: flex; flex-wrap: wrap; gap: 24px; justify-content: center; }
.step {
  display: inline-flex; align-items: center; gap: 8px;
  font: 400 13px/1 var(--font-mono);
  color: var(--text-3);
}
.step .step-num { color: var(--text-4); letter-spacing: 0.04em; }
.step .step-sep { color: var(--text-4); margin: 0 4px; }
```

---

## 5. Layout Principles

**Container**:
- `max-width: 1120px`
- Side padding: `clamp(20px, 4vw, 40px)`
- Narrow variant (正文/install): `max-width: 720px`

**Spacing Scale**（与 hueapp 的 4→128 梯度一致）:
```
--sp-1: 4px    --sp-6: 32px
--sp-2: 8px    --sp-7: 48px
--sp-3: 12px   --sp-8: 64px
--sp-4: 16px   --sp-9: 96px
--sp-5: 24px   --sp-10: 128px
```

- Section 上下 padding: `96px → 128px`（桌面），`64px → 80px`（移动）
- 卡片内 padding: 24px
- 组件 gap: 16-24px
- Hero 内部元素间隔：16-24-32 梯度

**Grid**:
```css
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
@media (max-width: 900px) { .grid-3, .grid-4 { grid-template-columns: 1fr 1fr; } }
@media (max-width: 600px) { .grid-3, .grid-4 { grid-template-columns: 1fr; } }
```

---

## 6. Depth & Elevation

深色语境下**少用投影，多用表面层级**。

| Level | Treatment | Use |
|-------|-----------|-----|
| Flat | 无 border 无 shadow | 背景装饰、大片色块 |
| Bordered | `1px solid var(--border)` | 默认卡片、输入框 |
| Bordered Hover | `1px solid var(--border-strong)` + `translateY(-2px)` | 卡片悬停 |
| Glow (仅 CTA Hover) | `box-shadow: 0 8px 24px rgba(var(--accent-cool-rgb), 0.25)` | Primary 按钮 hover |
| Blurred Overlay | `backdrop-filter: blur(14px) + rgba bg` | sticky nav 滚动态 |

禁止使用多层重叠投影或巨大模糊。

---

## 7. Animation & Interaction

**Motion Philosophy**：编辑风骨架 + 电影级签名时刻。绝大多数区域仍然安静，**2-3 个 signature moments 负责 wow**。动效服务于叙事：Hero 建立氛围、Phase A→B→C 讲方法论、Showcase 展示产出。
**Tier**: **L3 沉浸体验**

### Dependencies

```html
<!-- GSAP + ScrollTrigger + Lenis (全部 CDN，零构建) -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.14/dist/lenis.min.js"></script>
```

### Timing Tokens

```css
--ease: cubic-bezier(.2, 0, 0, 1);
--ease-soft: cubic-bezier(.2, .8, .2, 1);
--ease-cinema: cubic-bezier(.16, 1, .3, 1);
--dur-fast: 0.12s;
--dur-mid: 0.22s;
--dur-slow: 0.36s;
--dur-reveal: 0.8s;
--dur-signature: 1.4s;
```

### Base Setup — Lenis + GSAP

```js
// 1. Lenis 平滑滚动
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
  smoothTouch: false,
});
function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
requestAnimationFrame(raf);

// 2. GSAP + ScrollTrigger 桥接 Lenis
gsap.registerPlugin(ScrollTrigger);
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);

// 3. 顶部滚动进度条
gsap.to('.scroll-progress', {
  scaleX: 1,
  ease: 'none',
  scrollTrigger: { trigger: document.body, start: 'top top', end: 'bottom bottom', scrub: true },
});
```

### Entrance Animation

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0); filter: blur(0); }
}
.reveal { opacity: 0; }
.reveal.in-view { animation: fadeUp 0.8s var(--ease-cinema) forwards; }

/* Stagger 子元素 */
.reveal.in-view > * { animation: fadeUp 0.8s var(--ease-cinema) backwards; }
.reveal.in-view > *:nth-child(1) { animation-delay: 0.00s; }
.reveal.in-view > *:nth-child(2) { animation-delay: 0.08s; }
.reveal.in-view > *:nth-child(3) { animation-delay: 0.16s; }
.reveal.in-view > *:nth-child(4) { animation-delay: 0.24s; }
.reveal.in-view > *:nth-child(5) { animation-delay: 0.32s; }
```

### Hover & Focus States

- 所有按钮、卡片、链接必须有 hover + focus-visible
- 卡片 hover：surface 提亮 + 边框加深 + `translateY(-2px)` + 内部图标轻微放大
- 主按钮 hover：上浮 1px + 青色 glow + 磁吸跟随鼠标 ±8px
- 链接 hover：底线 0% → 100% 滑开

### Magnetic Button

```js
document.querySelectorAll('[data-magnetic]').forEach(btn => {
  const strength = 0.35;
  btn.addEventListener('pointermove', (e) => {
    const r = btn.getBoundingClientRect();
    const x = (e.clientX - r.left - r.width / 2) * strength;
    const y = (e.clientY - r.top - r.height / 2) * strength;
    gsap.to(btn, { x, y, duration: 0.4, ease: 'power3.out' });
  });
  btn.addEventListener('pointerleave', () => {
    gsap.to(btn, { x: 0, y: 0, duration: 0.6, ease: 'elastic.out(1, 0.4)' });
  });
});
```

### Custom Cursor（dot + ring）

```css
* { cursor: none; }
@media (hover: none) { * { cursor: auto; } .cursor-dot, .cursor-ring { display: none; } }
.cursor-dot, .cursor-ring {
  position: fixed; top: 0; left: 0; pointer-events: none; z-index: 9999;
  border-radius: 50%; transform: translate(-50%, -50%);
  mix-blend-mode: difference;
}
.cursor-dot  { width: 6px;  height: 6px;  background: #fff; transition: transform 0.08s linear; }
.cursor-ring { width: 36px; height: 36px; border: 1px solid #fff; transition: transform 0.2s var(--ease-cinema), width 0.22s, height 0.22s; }
.cursor-ring.is-hover { width: 60px; height: 60px; border-color: var(--accent-cool); }
```

```js
const dot = document.querySelector('.cursor-dot');
const ring = document.querySelector('.cursor-ring');
let rx = 0, ry = 0, dx = 0, dy = 0;
window.addEventListener('pointermove', (e) => {
  dx = e.clientX; dy = e.clientY;
  dot.style.transform = `translate(${dx}px, ${dy}px) translate(-50%, -50%)`;
});
(function followRing() {
  rx += (dx - rx) * 0.18; ry += (dy - ry) * 0.18;
  ring.style.transform = `translate(${rx}px, ${ry}px) translate(-50%, -50%)`;
  requestAnimationFrame(followRing);
})();
document.querySelectorAll('a, button, [data-magnetic], .card, .codeblock .copy-btn').forEach(el => {
  el.addEventListener('pointerenter', () => ring.classList.add('is-hover'));
  el.addEventListener('pointerleave', () => ring.classList.remove('is-hover'));
});
```

### Hero Background — 动态网格渐变（CSS-only）

```css
@property --grad-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}
@keyframes gradRotate {
  to { --grad-angle: 360deg; }
}
.hero-bg {
  position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(60% 50% at 30% 20%, rgba(var(--accent-cool-rgb), 0.18), transparent 70%),
    radial-gradient(50% 40% at 75% 35%, rgba(var(--accent-warm-rgb), 0.14), transparent 65%),
    conic-gradient(from var(--grad-angle) at 50% 50%,
      rgba(var(--accent-cool-rgb), 0.08),
      rgba(var(--accent-warm-rgb), 0.08),
      rgba(var(--accent-cool-rgb), 0.08));
  filter: blur(40px) saturate(120%);
  animation: gradRotate 30s linear infinite;
  opacity: 0.85;
}
.hero-bg::after {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 100%, var(--bg) 0%, transparent 70%);
}
```

### Signature #1 — Hero 卡片星座（Pattern 1）

**12 张 DESIGN.md 样本卡在 3D 空间里浮动**，每张卡是一个真实设计规范的切片（色板、字体表、组件 CSS、Do/Don't 条目）。围绕中心标题"先出规范，再出代码"，鼠标整体视差，每张卡各自呼吸。

```css
.constellation {
  position: absolute; inset: 0;
  perspective: 1500px; transform-style: preserve-3d;
  pointer-events: none; /* 允许 hero 文字点击 */
}
.star-card {
  position: absolute; top: 50%; left: 50%;
  background: var(--surface-1);
  border: 1px solid var(--border-strong);
  border-radius: 14px;
  padding: 16px 18px;
  box-shadow: 0 24px 60px rgba(0,0,0,0.5);
  will-change: transform, filter;
  pointer-events: auto;
  transform:
    translate3d(calc(-50% + var(--x) * 1px), calc(-50% + var(--y) * 1px), var(--z, 0px))
    rotateX(var(--rx, 0deg)) rotateY(var(--ry, 0deg)) rotateZ(var(--rz, 0deg));
  filter: blur(var(--blur, 0px));
  opacity: calc(1 - var(--blur, 0) * 0.06);
}
/* 近/中/远三组 */
.star-card.near   { --blur: 0;  --z:  0; }
.star-card.mid    { --blur: 3;  --z: -250; }
.star-card.far    { --blur: 7;  --z: -500; opacity: 0.55; }
/* 12 张的 x/y/rx/ry/rz 通过 data-i 和 CSS var 展开；具体值在 Phase C 生成 */
```

卡片内容示例（12 张对应 12 类规范摘录）：
1. 色板（4 个色块 + 变量名）
2. 字体表（3 行 font-family + weight）
3. 按钮 CSS（5-6 行代码片）
4. 阴影梯度（3 层 box-shadow 预览）
5. 间距刻度（8 个刻度条）
6. 圆角样板（4 个不同 border-radius 方块）
7. Do/Don't 清单（4-5 条）
8. 动效曲线（SVG easing 曲线图）
9. Grid 系统（12 列预览）
10. Icon 集合（6 个 lucide 图标）
11. 代码块预览（3 行 mono code）
12. 响应式断点（3 屏尺寸示意）

```js
// 1. 位置初始化（12 个点沿两个椭圆环分布）
const positions = [
  { x: -380, y: -180, rx:  8, ry: -12, rz: -4, cls: 'near' },
  { x:  360, y: -200, rx: -6, ry:   8, rz:  6, cls: 'near' },
  { x: -460, y:   40, rx:  4, ry: -10, rz: -8, cls: 'mid' },
  { x:  480, y:   60, rx: -4, ry:  10, rz:  8, cls: 'mid' },
  { x: -280, y:  220, rx:  6, ry:  -6, rz: -2, cls: 'near' },
  { x:  320, y:  240, rx: -8, ry:   6, rz:  4, cls: 'near' },
  { x: -600, y: -100, rx:  2, ry: -14, rz: -6, cls: 'far' },
  { x:  620, y: -120, rx: -2, ry:  14, rz:  6, cls: 'far' },
  { x: -150, y: -260, rx: 10, ry:   4, rz: -2, cls: 'mid' },
  { x:  180, y: -240, rx:-10, ry:  -4, rz:  2, cls: 'mid' },
  { x:    0, y:  340, rx: -6, ry:   0, rz:  0, cls: 'far' },
  { x:    0, y: -360, rx:  6, ry:   0, rz:  0, cls: 'far' },
];
document.querySelectorAll('.star-card').forEach((el, i) => {
  const p = positions[i];
  el.classList.add(p.cls);
  Object.entries(p).forEach(([k, v]) => {
    if (['x','y','rx','ry','rz'].includes(k)) el.style.setProperty(`--${k}`, v);
  });
});

// 2. 每张卡的 idle 呼吸
gsap.utils.toArray('.star-card').forEach((c) => {
  gsap.to(c, {
    '--y': `+=${gsap.utils.random(-18, 18)}`,
    '--rz': `+=${gsap.utils.random(-3, 3)}`,
    duration: gsap.utils.random(5, 8),
    ease: 'sine.inOut', yoyo: true, repeat: -1,
  });
});

// 3. 整体鼠标视差
const stage = document.querySelector('.hero');
stage.addEventListener('pointermove', (e) => {
  const cx = innerWidth/2, cy = innerHeight/2;
  const dx = (e.clientX - cx) / cx, dy = (e.clientY - cy) / cy;
  gsap.utils.toArray('.star-card').forEach((c) => {
    const depth = Math.abs(parseFloat(c.style.getPropertyValue('--z') || 0)) / 500;
    gsap.to(c, { x: dx * 30 * (1-depth), y: dy * 30 * (1-depth), duration: 0.8, ease: 'power3.out' });
  });
});
```

### Signature #2 — 卡片汇聚过渡（Pattern 2）

Hero → Why section 之间，卡片从散落位置飞向中心合并成一张 DESIGN.md 大卡。

```js
gsap.timeline({
  scrollTrigger: {
    trigger: '.hero',
    start: 'bottom 70%',
    end: 'bottom top',
    scrub: 1,
  },
})
.to('.star-card', {
  '--x': 0, '--y': 0, '--z': 0, '--rx': 0, '--ry': 0, '--rz': 0,
  '--blur': 0,
  scale: 0.2,
  opacity: 0,
  stagger: { amount: 0.8, from: 'random' },
  ease: 'power2.in',
})
.from('.why-hero-card', { scale: 0.6, opacity: 0, duration: 1, ease: 'power3.out' }, '-=0.5');
```

### Signature #3 — Phase A→B→C Pinned Scrollytelling（Pattern 3 强化版）

**核心装置**。Pin 这个 section 大约 150vh 滚动距离，让"输入 → DESIGN.md → 代码"的形变跟着滚动进度发生。

```js
const phaseTl = gsap.timeline({
  scrollTrigger: {
    trigger: '.phase-scene',
    start: 'top top',
    end: '+=1500',
    scrub: 1,
    pin: true,
    anticipatePin: 1,
  },
});

// 阶段 A: 三个输入图标漂浮 → 合并
phaseTl
  .from('.phase-input-prd',    { y: 40, opacity: 0, duration: 1 })
  .from('.phase-input-url',    { y: 40, opacity: 0, duration: 1 }, '-=0.7')
  .from('.phase-input-shot',   { y: 40, opacity: 0, duration: 1 }, '-=0.7')
  .to(['.phase-input-prd', '.phase-input-url', '.phase-input-shot'], {
    x: (i) => [-40, 0, 40][i] * -1, y: 0, scale: 0.8, opacity: 0.3, duration: 1.2,
  })
  // 阶段 B: DESIGN.md 卡片从右浮入，token 行逐行填充
  .from('.phase-design-card', { x: 120, opacity: 0, duration: 1.2, ease: 'power3.out' }, '<')
  .from('.phase-token-row', { width: 0, opacity: 0, stagger: 0.12, duration: 0.6 }, '-=0.6')
  // 阶段 C: 代码行从 DESIGN.md 流出
  .to('.phase-design-card', { x: -80, scale: 0.9, opacity: 0.5, duration: 1 }, '+=0.4')
  .from('.phase-code-line', { x: -40, opacity: 0, stagger: 0.05, duration: 0.5 }, '-=0.8')
  // 最终: 成品网页缩略图
  .from('.phase-final', { y: 40, opacity: 0, duration: 1 }, '+=0.3');
```

进度条沿 section 左侧出现，三段颜色（青→青橙→橙）标示 Phase。

### Signature #4 — WebGL 3D Iridescent Knot（Pattern 4 · 替代 CSS Cube）

"What's Inside" section 的视觉主角。**Three.js TorusKnotGeometry + MeshPhysicalMaterial**（transmission 0.92, iridescence 1, clearcoat 1）。滚动驱动旋转，青/橙双点光染色，50 个粒子 sprite 做"尘埃"，轨道环用 SVG / CSS 叠加。

```js
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const canvas = document.querySelector('.knot-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const resize = () => {
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  camera.aspect = canvas.clientWidth / canvas.clientHeight;
  camera.updateProjectionMatrix();
};

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.z = 5;

const mat = new THREE.MeshPhysicalMaterial({
  transmission: 0.92, thickness: 1.5, roughness: 0.15,
  iridescence: 1, iridescenceIOR: 1.3, clearcoat: 1,
  color: 0xffffff,
});
const knot = new THREE.Mesh(new THREE.TorusKnotGeometry(1, 0.3, 180, 32), mat);
scene.add(knot);

scene.add(new THREE.HemisphereLight(0xffffff, 0x101020, 0.6));
const l1 = new THREE.PointLight(0x5EEAD4, 4, 20); l1.position.set(3, 3, 3); scene.add(l1);
const l2 = new THREE.PointLight(0xFB923C, 4, 20); l2.position.set(-3, -2, 3); scene.add(l2);

// 粒子尘埃
const pgeo = new THREE.BufferGeometry();
const positions = new Float32Array(150 * 3);
for (let i = 0; i < 150; i++) {
  positions[i*3]   = (Math.random()-0.5) * 8;
  positions[i*3+1] = (Math.random()-0.5) * 6;
  positions[i*3+2] = (Math.random()-0.5) * 4;
}
pgeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
const particles = new THREE.Points(pgeo, new THREE.PointsMaterial({ color: 0xaaaaaa, size: 0.03, transparent: true, opacity: 0.7 }));
scene.add(particles);

gsap.to(knot.rotation, {
  y: Math.PI * 2, x: Math.PI,
  scrollTrigger: { trigger: '.whats-inside', start: 'top 80%', end: 'bottom 20%', scrub: 1 },
});

function tick() {
  knot.rotation.z += 0.002;
  particles.rotation.y += 0.0008;
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
resize(); tick();
new ResizeObserver(resize).observe(canvas);
```

**What's Inside 的卡片部分**仍然存在（展示 58 品牌 / 10 种子 / 3 档 / 7 场景 等 6 类资产），放在 WebGL 场景的下方，卡片顶部用 **Pattern 6 抽象艺术顶**（青橙渐变 mesh）。

### Signature #5 — Three Inputs 左 pin / 右 swap（Pattern 3）

Three Inputs section pin 300vh，左侧标题固定（"任何起点都可以"），右侧容器按滚动切换 3 个场景：**PRD 文档 → 参考 URL 截图 → 用户草图**，每个场景是一张放大的拟真卡片（带光泽、带细节）。切换时用 crossfade + 轻微 scale。

```js
const scenes = gsap.utils.toArray('.input-scene');
const labels = ['PRD 文档', '参考 URL', '截图 / 草稿'];

ScrollTrigger.create({
  trigger: '.three-inputs',
  start: 'top top', end: 'bottom bottom',
  pin: '.three-inputs-inner',
  scrub: 0.5,
  onUpdate: (self) => {
    const idx = Math.min(Math.floor(self.progress * scenes.length), scenes.length - 1);
    scenes.forEach((s, i) => {
      gsap.to(s, { opacity: i === idx ? 1 : 0, scale: i === idx ? 1 : 0.94, duration: 0.4 });
    });
    document.querySelector('.input-label').textContent = labels[idx];
  },
});
```

### Signature #6 — Section 大标题光晕（Pattern 5）

```css
.section-h2 {
  position: relative; display: inline-block;
  font: 700 clamp(36px, 5vw, 64px)/1.1 var(--font-ui);
  color: var(--text-1);
}
.section-h2::before {
  content: attr(data-ghost);
  position: absolute; left: 0; top: 0;
  background: var(--gradient-key);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: blur(24px); opacity: 0.45;
  z-index: -1;
  transform: translate(6px, 6px);
}
```

### Signature #7 — 抽象艺术顶 Feature Cards（Pattern 6）

```css
.art-card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; }
.art-top {
  aspect-ratio: 4 / 3;
  background:
    radial-gradient(circle at 30% 40%, var(--accent-cool) 0%, transparent 48%),
    radial-gradient(circle at 72% 60%, var(--accent-warm) 0%, transparent 44%),
    radial-gradient(circle at 50% 85%, #c084fc 0%, transparent 40%);
  background-size: 200% 200%;
  filter: saturate(130%);
  animation: artShift 20s ease-in-out infinite alternate;
}
@keyframes artShift { to { background-position: 100% 100%; } }
.art-bottom { padding: 20px 22px 22px; }
```

### Signature #8 — Showcase 3D Perspective Marquee

两行反向流动的作品缩略图，整体在 3D 空间里倾斜（x-axis -8°），形成"从画面后方飞过"的视差感。

```css
.marquee {
  perspective: 1200px;
  overflow: hidden;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 12%, #000 88%, transparent);
          mask-image: linear-gradient(to right, transparent, #000 12%, #000 88%, transparent);
}
.marquee-track {
  display: flex; gap: 24px;
  transform: rotateX(-8deg) rotateZ(-2deg);
  animation: marqueeSlide 40s linear infinite;
}
.marquee.reverse .marquee-track { animation-direction: reverse; animation-duration: 50s; }
@keyframes marqueeSlide { to { transform: rotateX(-8deg) rotateZ(-2deg) translateX(-50%); } }
```

### Signature #5 — 色板 Token 汇聚动画（Why DESIGN.md 区）

进入视窗时，12 个散乱浮动的色块飞入格点，形成 `:root { --bg: ... }` 代码块。

```js
ScrollTrigger.create({
  trigger: '.token-assemble',
  start: 'top 70%',
  onEnter: () => {
    gsap.from('.token-chip', {
      x: () => gsap.utils.random(-200, 200),
      y: () => gsap.utils.random(-100, 100),
      rotate: () => gsap.utils.random(-30, 30),
      opacity: 0,
      stagger: 0.05,
      duration: 1,
      ease: 'power3.out',
    });
    gsap.from('.token-code-line', { opacity: 0, x: -20, stagger: 0.06, duration: 0.5, delay: 0.8 });
  },
});
```

### Signature #6 — Text Scramble（eyebrow 标签）

所有 eyebrow label 进入视窗时做 0.8s 的字符乱码 → 稳定动画。

```js
function scrambleText(el, duration = 800) {
  const final = el.dataset.scramble || el.textContent;
  el.dataset.scramble = final;
  const chars = '!<>-_\\/[]{}—=+*^?#________';
  let start = performance.now();
  function tick(now) {
    const p = Math.min(1, (now - start) / duration);
    const out = final.split('').map((c, i) => {
      if (p * final.length > i) return c;
      if (c === ' ') return ' ';
      return chars[Math.floor(Math.random() * chars.length)];
    }).join('');
    el.textContent = out;
    if (p < 1) requestAnimationFrame(tick);
    else el.textContent = final;
  }
  requestAnimationFrame(tick);
}
document.querySelectorAll('[data-scramble]').forEach(el => {
  new IntersectionObserver(([e], obs) => {
    if (e.isIntersecting) { scrambleText(el); obs.unobserve(el); }
  }, { threshold: 0.8 }).observe(el);
});
```

### Signature #7 — Hero 关键词渐变流动

Hero 里的"**规范**"和"**代码**"两词的渐变不是静态的，沿文字表面缓慢流动（30s 一周期）。

```css
.key-gradient {
  background: linear-gradient(135deg, var(--accent-cool), var(--accent-warm), var(--accent-cool));
  background-size: 300% 100%;
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientSlide 18s linear infinite;
}
@keyframes gradientSlide { to { background-position: -300% 0; } }
```

### Signature #8 — 顶部滚动进度条

```css
.scroll-progress {
  position: fixed; top: 0; left: 0; right: 0; height: 2px;
  background: var(--gradient-key);
  transform-origin: 0 50%; transform: scaleX(0);
  z-index: 100;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .reveal { opacity: 1; animation: none; }
  .hero-bg, .cube, .marquee-track, .key-gradient { animation: none !important; }
  .stack-card { transform: none !important; }
  * { cursor: auto !important; }
  .cursor-dot, .cursor-ring { display: none !important; }
}
```

```js
// JS 端同样降级
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
  lenis.destroy?.();
  ScrollTrigger.getAll().forEach(t => t.kill());
}
```

---

## 8. Do's and Don'ts

### Do
- ✅ 保持深色底 + 四级文字层次，让信息节奏完全靠**字重、间距、层级**建立
- ✅ 冷青 + 暖橙**成对出现但留白分隔**，永远不直接拼接
- ✅ 关键词渐变装饰一屏最多 1 处，视为「指针」而非「装饰」
- ✅ 每个 section 有 eyebrow label（uppercase, letter-spacing）+ H2 + sub 三件套
- ✅ 用 Instrument Serif **斜体**点缀 2-3 个关键词，建立"文档感"
- ✅ 代码块和命令用 JetBrains Mono，永远不用纯文字代替
- ✅ 卡片 hover 只做 "surface 提亮 + 边框加深 + 上浮 2px"，不变色
- ✅ L2 动效必须包含 prefers-reduced-motion 降级

### Don't
- ❌ 不要用霓虹色、饱和大色块、发光边框（这是暗色**编辑**风，不是赛博）
- ❌ 不要堆叠 4 个以上颜色；冷青 + 暖橙 + 四级灰已经是全部
- ❌ 不要把渐变用在 body 文字、按钮、边框上（仅限 1-2 个关键词的填充 + 顶部进度条）
- ❌ 不要给卡片加厚投影（`box-shadow` 仅限 primary CTA hover 和 3D 卡片堆叠）
- ❌ 不要用 emoji（方法论产品气质不合）
- ❌ **Pin / 自定义 cursor 仅用在明确的签名区**；不要整页开 scroll-jack 或全页光标替换（本页仅 Phase A→B→C 一处 pin；custom cursor 全局但用 mix-blend-mode 保持低调）
- ❌ 不要用 serif 写正文（只做关键词点缀）
- ❌ 不要让英文字体**独自**承载中文（fallback 必须配 Noto Sans SC）
- ❌ 不要硬编码 hex，任何颜色都走 CSS 变量
- ❌ 不要在 install 命令框里放装饰（它要看起来像真命令，不是装饰条）
- ❌ 不要让 3D 效果持续高强度运动（Cube 24s/周期、Stack 低频呼吸 — 不要让页面看起来躁动）
- ❌ 不要在低性能设备（`matchMedia('(max-width: 640px)')` + `navigator.hardwareConcurrency < 4`）保留 3D 立方体和复杂 pin，要降级为静态卡片

---

## 9. Responsive Behavior

**Breakpoints**:

| Name | Width | Key Changes |
|------|-------|-------------|
| Desktop | ≥ 1024px | 3-4 列网格、hero 两行标题、section padding 96-128px |
| Tablet | 640-1023px | 2 列网格、hero 仍两行但字号缩一档、nav 折叠为精简 |
| Mobile | < 640px | 单列、hero 字号 clamp 下限、section padding 64-80px、步骤简述纵向排 |

**Touch Targets**: 最小 44×44px
**Collapsing Strategy**:
- Nav：桌面全量 → 平板隐藏次级链接 → 移动端收成汉堡（或仅保留 Logo + GitHub 图标）
- Grid：3 列 → 2 列 → 1 列
- Hero 三步简述：横排 → 纵排

```css
@media (max-width: 1023px) {
  :root { --sp-section: 80px; }
  .grid-3, .grid-4 { grid-template-columns: 1fr 1fr; }
  .nav .nav-link-secondary { display: none; }
}

@media (max-width: 639px) {
  :root { --sp-section: 64px; }
  .container { padding-left: 20px; padding-right: 20px; }
  .grid-3, .grid-4 { grid-template-columns: 1fr; }
  .steps { flex-direction: column; gap: 12px; }
  .hero-title { font-size: clamp(36px, 9vw, 48px); }
}
```

---

## 附：与参考站（hueapp.io）的差异审计

| 维度 | hueapp.io | 本页面 | 理由 |
|------|-----------|--------|------|
| 底色 | #0d0e12 | #0a0b0e（更深） | 强化"深色手册"而非"产品页" |
| 强调色 | 冷蓝 #63b3ed + 暖粉 #ec6cb9 | 冷青 #5EEAD4 + 暖橙 #FB923C | 规避雷同 + 呼应"规范 × 温度"方法论 |
| 字体 | DM Sans 单家族 | DM Sans + Instrument Serif（装饰） | 建立"文档感"识别 |
| Hero 大小 | 56-72px | 48-84px | 与 hueapp 拉开，更具冲击力 |
| Section 结构 | Hero → Proofs → System → Install | Hero → Why DESIGN.md → 三输入 → A→B→C 流程 → 资产 → Demo → Install | 故事线不同（方法论 vs 品牌转 UI） |
| 动效档位 | L1-L2 | L2 | 基本一致 |
| 特殊点 | 横滚 showcase | 对比图（AI 直撸 vs 先规范再撸） | 方法论需要对比论证，作品展示退到次要 |
