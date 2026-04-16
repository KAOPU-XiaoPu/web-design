# Interaction Patterns

三档交互代码库。所有代码可直接复用，按用户选定的档位组合进生成的 Style SKILL。

---

## 公共基础

### useInView Hook（L1/L2/L3 通用）

```jsx
function useInView(options = {}) {
  const [ref, setRef] = React.useState(null);
  const [isInView, setIsInView] = React.useState(false);
  React.useEffect(() => {
    if (!ref) return;
    const obs = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { setIsInView(true); obs.unobserve(ref); }
    }, { threshold: 0.15, ...options });
    obs.observe(ref);
    return () => obs.disconnect();
  }, [ref]);
  return [setRef, isInView];
}
```

### 原生 JS 版（无框架时）

```js
function initScrollReveal(selector = '.reveal', cls = 'in-view') {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add(cls); obs.unobserve(e.target); } });
  }, { threshold: 0.15 });
  document.querySelectorAll(selector).forEach(el => obs.observe(el));
}
document.addEventListener('DOMContentLoaded', () => initScrollReveal());
```

### Smooth Scroll 基础

```css
html { scroll-behavior: smooth; }
[id] { scroll-margin-top: 80px; }
```

### Reduced Motion 降级

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## L1: 精致静态

> 优雅的 hover 反馈 + 柔和入场。不喧宾夺主，信息优先。

### 入场：淡入

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.reveal {
  opacity: 0;
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.in-view { opacity: 1; }
```

### 入场：轻微上浮

```css
.reveal {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.in-view {
  opacity: 1;
  transform: translateY(0);
}
```

### Hover：轻浮起 + 阴影

```css
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(0,0,0,0.06);
}
```

### Hover：颜色渐变

```css
.btn {
  background: var(--color-primary);
  transition: background 0.2s ease, color 0.2s ease;
}
.btn:hover {
  background: var(--color-primary-hover);
}
```

### Hover：下划线滑入

```css
.link {
  position: relative;
  text-decoration: none;
}
.link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-primary);
  transition: width 0.3s ease;
}
.link:hover::after { width: 100%; }
```

### Focus Ring

```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## L2: 流畅交互

> 滚动 reveal、视差、导航变化。有节奏感，每个 section 像一个"场景"。

### 入场：fadeInUp + Stagger

```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(28px); }
  to { opacity: 1; transform: translateY(0); }
}
.reveal {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.in-view { opacity: 1; transform: translateY(0); }

/* Stagger：子元素交错入场 */
.reveal.in-view > *:nth-child(1) { transition-delay: 0s; }
.reveal.in-view > *:nth-child(2) { transition-delay: 0.1s; }
.reveal.in-view > *:nth-child(3) { transition-delay: 0.2s; }
.reveal.in-view > *:nth-child(4) { transition-delay: 0.3s; }
.reveal.in-view > *:nth-child(5) { transition-delay: 0.4s; }
```

JS 动态 stagger（不限制子元素数量）：
```js
function initStaggerReveal(containerSelector = '.stagger-reveal') {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const children = e.target.children;
      Array.from(children).forEach((child, i) => {
        child.style.transitionDelay = `${Math.min(i * 0.1, 0.6)}s`;
      });
      e.target.classList.add('in-view');
      obs.unobserve(e.target);
    });
  }, { threshold: 0.15 });
  document.querySelectorAll(containerSelector).forEach(el => obs.observe(el));
}
```

### 入场：scaleIn

```css
.reveal-scale {
  opacity: 0;
  transform: scale(0.92);
  transition: opacity 0.5s cubic-bezier(0.34, 1.56, 0.64, 1),
              transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.reveal-scale.in-view { opacity: 1; transform: scale(1); }
```

### 视差：CSS scroll-driven（现代浏览器）

```css
@supports (animation-timeline: scroll()) {
  .parallax-bg {
    animation: parallaxShift linear both;
    animation-timeline: scroll();
  }
  @keyframes parallaxShift {
    from { transform: translateY(0); }
    to { transform: translateY(-80px); }
  }
}
```

### 视差：简单 JS 方案（兼容性好）

```js
function initParallax(selector = '.parallax', speed = 0.3) {
  const els = document.querySelectorAll(selector);
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const scrollY = window.scrollY;
      els.forEach(el => {
        const rect = el.getBoundingClientRect();
        const offset = (rect.top + scrollY - window.innerHeight / 2) * speed;
        el.style.transform = `translateY(${offset}px)`;
      });
      ticking = false;
    });
  }, { passive: true });
}
```

### 导航：滚动后透明→毛玻璃

```css
.nav {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 100;
  background: transparent;
  backdrop-filter: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.nav.scrolled {
  background: rgba(var(--color-bg-rgb), 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom-color: var(--color-border);
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
```

```js
const nav = document.querySelector('.nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });
```

### 滚动进度条

```css
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-primary);
  z-index: 1000;
  transform-origin: left;
  transform: scaleX(0);
}
```

```js
const bar = document.querySelector('.scroll-progress');
window.addEventListener('scroll', () => {
  const pct = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  bar.style.transform = `scaleX(${pct})`;
}, { passive: true });
```

### Hover：卡片图片缩放

```css
.img-card { overflow: hidden; border-radius: var(--radius); }
.img-card img {
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  display: block;
  width: 100%;
}
.img-card:hover img { transform: scale(1.06); }
```

### Hover：发光边框（暗色风格）

```css
.glow-card {
  position: relative;
  transition: box-shadow 0.3s ease;
}
.glow-card:hover {
  box-shadow: 0 0 0 1px var(--color-primary),
              0 0 20px rgba(var(--color-primary-rgb), 0.15);
}
```

### 按钮按压微交互

```css
.btn {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb), 0.25);
}
.btn:active {
  transform: translateY(0) scale(0.97);
  box-shadow: none;
}
```

### 数字计数器

```js
function countUp(el, end, duration = 2000) {
  let start = 0;
  const step = (end / duration) * 16;
  const timer = setInterval(() => {
    start += step;
    if (start >= end) { el.textContent = end.toLocaleString(); clearInterval(timer); }
    else { el.textContent = Math.floor(start).toLocaleString(); }
  }, 16);
}

// 配合 IntersectionObserver 触发
function initCounters(selector = '.count-up') {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const end = parseInt(e.target.dataset.end, 10);
      countUp(e.target, end);
      obs.unobserve(e.target);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll(selector).forEach(el => obs.observe(el));
}
```

```html
<span class="count-up" data-end="1200">0</span>+
```

---

## L3: 沉浸体验

> 滚动驱动时间线、section pin、光标跟随、页面转场。需要用户确认是否引入 GSAP 等依赖。

### GSAP + ScrollTrigger 基础设置

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>
<script>
gsap.registerPlugin(ScrollTrigger);
</script>
```

### Section Pin（滚动时固定区域，内容变化）

```js
gsap.to('.pinned-content', {
  scrollTrigger: {
    trigger: '.pin-section',
    start: 'top top',
    end: '+=200%',       // pin 持续的滚动距离
    pin: true,
    scrub: 1,            // 滚动绑定
  },
  opacity: 1,
  y: 0,
});
```

### 滚动驱动时间线

```js
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.timeline-section',
    start: 'top center',
    end: 'bottom center',
    scrub: true,
  }
});

tl.from('.step-1', { opacity: 0, y: 40 })
  .from('.step-2', { opacity: 0, y: 40 }, '+=0.1')
  .from('.step-3', { opacity: 0, y: 40 }, '+=0.1');
```

### 水平滚动 Section

```js
const panels = gsap.utils.toArray('.h-panel');
gsap.to(panels, {
  xPercent: -100 * (panels.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '.h-scroll-container',
    pin: true,
    scrub: 1,
    end: () => `+=${document.querySelector('.h-scroll-container').scrollWidth}`,
  },
});
```

```css
.h-scroll-container {
  display: flex;
  width: fit-content;
  flex-wrap: nowrap;
}
.h-panel {
  width: 100vw;
  height: 100vh;
  flex-shrink: 0;
}
```

### 光标跟随（磁性效果）

```js
const cursor = document.querySelector('.custom-cursor');
document.addEventListener('mousemove', (e) => {
  cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
});

// 磁性按钮
document.querySelectorAll('.magnetic').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
  });
});
```

```css
.custom-cursor {
  position: fixed;
  top: -16px;
  left: -16px;
  width: 32px;
  height: 32px;
  border: 2px solid var(--color-primary);
  border-radius: 50%;
  pointer-events: none;
  z-index: 9999;
  transition: width 0.2s, height 0.2s, border-color 0.2s;
  mix-blend-mode: difference;
}
```

### 光标辉光（暗色风格）

```css
.cursor-glow {
  position: fixed;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(var(--color-primary-rgb), 0.08) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
  transform: translate(-50%, -50%);
  transition: opacity 0.3s;
}
```

```js
const glow = document.querySelector('.cursor-glow');
document.addEventListener('mousemove', (e) => {
  glow.style.left = e.clientX + 'px';
  glow.style.top = e.clientY + 'px';
});
```

### 文字逐词 Reveal

```js
function initTextReveal(selector = '.text-reveal') {
  document.querySelectorAll(selector).forEach(el => {
    const text = el.textContent;
    // 中文按字拆分，英文按空格
    const isChinese = /[\u4e00-\u9fa5]/.test(text);
    const parts = isChinese ? text.split('') : text.split(' ');
    el.innerHTML = parts.map((p, i) =>
      `<span style="display:inline-block;opacity:0;transform:translateY(100%);transition:all 0.5s cubic-bezier(0.16,1,0.3,1) ${i * (isChinese ? 40 : 80)}ms">${p}${isChinese ? '' : '&nbsp;'}</span>`
    ).join('');
    el.style.overflow = 'hidden';
  });
}

// 配合 IO 触发
function triggerTextReveal(selector = '.text-reveal') {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.querySelectorAll('span').forEach(s => {
        s.style.opacity = '1';
        s.style.transform = 'translateY(0)';
      });
      obs.unobserve(e.target);
    });
  }, { threshold: 0.3 });
  document.querySelectorAll(selector).forEach(el => obs.observe(el));
}
```

### 页面转场

```css
.page-transition {
  animation: pageEnter 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes pageEnter {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 退出（配合路由切换使用） */
.page-exit {
  animation: pageExit 0.25s ease-in both;
}
@keyframes pageExit {
  to { opacity: 0; transform: translateY(-8px); }
}
```

### 3D 透视卡片

```css
.perspective-card {
  perspective: 1000px;
}
.perspective-card-inner {
  transition: transform 0.4s ease;
  transform-style: preserve-3d;
}
```

```js
document.querySelectorAll('.perspective-card').forEach(card => {
  const inner = card.querySelector('.perspective-card-inner');
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    inner.style.transform = `rotateY(${x * 12}deg) rotateX(${-y * 12}deg)`;
  });
  card.addEventListener('mouseleave', () => {
    inner.style.transform = '';
  });
});
```

### Lenis 平滑滚动（可选增强）

```html
<script src="https://cdn.jsdelivr.net/npm/lenis@1/dist/lenis.min.js"></script>
<script>
const lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
requestAnimationFrame(raf);

// 与 GSAP ScrollTrigger 同步
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
</script>
```

---

## 装饰性效果（按风格选用）

### 渐变流动背景

```css
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.gradient-bg {
  background: linear-gradient(-45deg, var(--color-primary), var(--color-secondary), var(--color-accent));
  background-size: 400% 400%;
  animation: gradientShift 12s ease infinite;
}
```

### Glow Pulse（暗色风格）

```css
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(var(--color-primary-rgb), 0.2); }
  50% { box-shadow: 0 0 40px rgba(var(--color-primary-rgb), 0.4); }
}
.glow { animation: glowPulse 3s ease-in-out infinite; }
```

### Blob 浮动（活泼风格背景）

```css
@keyframes blobMorph {
  0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
  50% { border-radius: 50% 60% 30% 60% / 30% 60% 70% 40%; }
}
.blob {
  width: 300px;
  height: 300px;
  background: var(--color-primary);
  opacity: 0.08;
  filter: blur(60px);
  animation: blobMorph 8s ease-in-out infinite;
  position: absolute;
  z-index: 0;
  pointer-events: none;
}
```

### 打字机效果

```css
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink { 50% { border-color: transparent; } }
.typewriter {
  overflow: hidden;
  white-space: nowrap;
  border-right: 3px solid var(--color-primary);
  width: fit-content;
  animation: typing 3s steps(30) 1s both, blink 0.7s step-end infinite;
}
```
