# Scroll-Story Patterns

L3 级别的"电影式" scroll 叙事招式库。参考标杆：doubao.com/about、apple.com/vision-pro、stripe.com、tome.app、readme.com、igloo.inc。

**触发条件**：以下任一满足时必走此级别，不再用"L2 reveal"兜底：
- 用户明确要求"像 doubao / apple / stripe 那样的滚动效果"
- 用户说"普通"、"单调"、"要有滚动驱动"、"要 3D"、"要电影感"
- 页面定位是"方法论、品牌、产品宣言"而非纯信息型

---

## L3 硬性要求（除 6 类基础动效外加码）

每个 L3 页面必须至少包含以下 4 种 scroll-story 模式中的 **3 种**：

| 模式 | 必备数量 |
|------|----------|
| Pin-Scrub 场景（section 固定 + 滚动驱动内容形变） | ≥ 1 |
| 容器替换（左 pin / 右 swap）叙事 | ≥ 1 |
| 汇聚/散开转场（多元素飞入飞出合并） | ≥ 1 |
| WebGL / 真 3D 签名时刻（非仅 CSS 3D） | ≥ 1 |

共同原则：**每 1-2 屏必有一个 signature moment**。单调滑动三屏以上不被允许。

---

## Pattern 1 — Card Constellation Hero（卡片星座 Hero）

**出处**：doubao.com/about 首屏
**效果**：10-15 张内容样本卡（每张代表产品能力的一个实例）在 3D 空间里以不同 Z 深度、不同旋转角度、不同动态模糊度浮动，围绕中心的文字主张。鼠标移动驱动整体视差。

### 实现模板

```css
.constellation {
  position: relative;
  perspective: 1400px;
  transform-style: preserve-3d;
  height: 100vh;
}
.star-card {
  position: absolute;
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px;
  transform-style: preserve-3d;
  will-change: transform, filter;
  transition: filter 0.5s var(--ease-cinema);
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
}
/* 每张卡通过 inline style 或 data-attr 设置独立位置:
   --x / --y / --z / --rx / --ry / --rz / --blur
*/
.star-card {
  top: calc(50% + var(--y) * 1px);
  left: calc(50% + var(--x) * 1px);
  transform:
    translate3d(-50%, -50%, var(--z, 0px))
    rotateX(var(--rx, 0deg))
    rotateY(var(--ry, 0deg))
    rotateZ(var(--rz, 0deg));
  filter: blur(var(--blur, 0px));
  opacity: calc(1 - var(--blur, 0) * 0.08);
}
```

```js
// 12 张卡随机分布（或按设计指定）
const cards = document.querySelectorAll('.star-card');

// 1. 基础浮动（每张卡各自的 idle 呼吸）
cards.forEach((c, i) => {
  gsap.to(c, {
    y: `+=${gsap.utils.random(-16, 16)}`,
    rotate: `+=${gsap.utils.random(-4, 4)}`,
    duration: gsap.utils.random(4, 7),
    ease: 'sine.inOut',
    yoyo: true, repeat: -1,
  });
});

// 2. 鼠标视差（整个 constellation 跟随）
const stage = document.querySelector('.constellation');
stage.addEventListener('pointermove', (e) => {
  const cx = window.innerWidth / 2, cy = window.innerHeight / 2;
  const dx = (e.clientX - cx) / cx;
  const dy = (e.clientY - cy) / cy;
  cards.forEach((c, i) => {
    const depth = parseFloat(c.style.getPropertyValue('--z') || 0) / 200;
    gsap.to(c, { x: dx * 20 * depth, y: dy * 20 * depth, duration: 0.8, ease: 'power3.out' });
  });
});
```

### 设计指南
- Z 轴分布：近景 (z: 0 ~ 100) 清晰不模糊、中景 (z: -200 ~ -400) 轻微模糊 2-4px、远景 (z: -500 ~ -700) 模糊 6-10px
- 旋转角度：|rx, ry, rz| ≤ 15°，超过会像碎纸
- 卡片尺寸参差（180×220 到 320×400），构成视觉节奏
- 卡片内容要"有意义"（产品样本、真实截图），避免占位符

---

## Pattern 2 — Card Collapse Transition（卡片汇聚过渡）

**出处**：doubao.com/about 从 Hero 过渡到 "文字创作能力"
**效果**：Hero 里散开的卡片，在滚动到某阈值时整体飞向中心，合并为下一 section 的单一容器。

### 实现模板

```js
gsap.timeline({
  scrollTrigger: {
    trigger: '.constellation',
    start: 'bottom 80%',
    end: 'bottom top',
    scrub: 1,
  },
})
.to('.star-card', {
  x: 0, y: 0, z: 0, rotateX: 0, rotateY: 0, rotateZ: 0,
  filter: 'blur(0px)',
  scale: 0,
  opacity: 0,
  stagger: { amount: 0.6, from: 'random' },
  ease: 'power2.in',
})
.from('.next-section .hero-panel', {
  scale: 0.7, opacity: 0, duration: 1, ease: 'power3.out',
}, '-=0.4');
```

### 设计指南
- 汇聚终点应该是下一 section 的关键容器（不要凭空消失）
- stagger 用 `from: 'random'`（更自然，避免整齐划一的波）
- 汇聚距离要够长（跨 80-100vh 滚动）才有"风吹落"的感觉

---

## Pattern 3 — Left Pin / Right Swap Narrative（左 pin / 右 swap 叙事）

**出处**：doubao 产品能力四连（撰写/绘制/知识/解答）、igloo.inc 多场景
**效果**：section pin 住，左侧标题+描述+CTA 保持位置不动，右侧容器按滚动进度切换 3-4 个场景（产品截图/动画 demo/3D 模型）。

### 实现模板

```html
<section class="pin-swap" data-scenes="4">
  <div class="pin-swap-inner">
    <div class="left">
      <h2 class="pin-title">标题 1</h2>
      <p class="pin-body">描述 1</p>
      <a class="pin-cta">立即体验</a>
    </div>
    <div class="right">
      <div class="scene scene-1">场景 1 内容</div>
      <div class="scene scene-2">场景 2 内容</div>
      <div class="scene scene-3">场景 3 内容</div>
      <div class="scene scene-4">场景 4 内容</div>
    </div>
  </div>
</section>
```

```css
.pin-swap { height: 400vh; /* 每个场景 100vh */ }
.pin-swap-inner { position: sticky; top: 0; height: 100vh; display: grid; grid-template-columns: 1fr 1.2fr; gap: 48px; align-items: center; }
.scene { position: absolute; inset: 0; opacity: 0; }
.scene:first-child { opacity: 1; }
```

```js
const scenes = gsap.utils.toArray('.scene');
const titles = [/* 各场景文案对象数组 */];

ScrollTrigger.create({
  trigger: '.pin-swap',
  start: 'top top',
  end: 'bottom bottom',
  scrub: 0.5,
  onUpdate: (self) => {
    const progress = self.progress;
    const idx = Math.min(Math.floor(progress * scenes.length), scenes.length - 1);

    // 切换场景（淡入淡出）
    scenes.forEach((s, i) => {
      gsap.to(s, { opacity: i === idx ? 1 : 0, duration: 0.4, ease: 'power2.out' });
    });

    // 切换左侧文案
    document.querySelector('.pin-title').textContent = titles[idx].title;
    document.querySelector('.pin-body').textContent = titles[idx].body;
  },
});
```

### 设计指南
- 场景切换点要让用户有"停顿"感（不能像翻书一样急促）
- 右侧场景之间的差异要显著（不同产品/不同场景），不要只改文字
- 左侧 CTA 可以不变，也可按场景变化（如改变链接目标）

---

## Pattern 4 — WebGL 3D Signature Moment（WebGL 3D 签名时刻）

**出处**：doubao 的 Mobius / apple Vision Pro 的头显 / igloo.inc 的 3D 图标
**效果**：section 居中一个 3D 物体（glass 材质、metallic、shader），随滚动旋转/变形，配合 orbital 粒子和光晕。

### 实现模板（Three.js 最小可用）

```html
<section class="webgl-scene">
  <canvas class="webgl-canvas"></canvas>
  <h2 class="webgl-title">章节标题</h2>
</section>
```

```js
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const canvas = document.querySelector('.webgl-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(canvas.clientWidth, canvas.clientHeight);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
camera.position.z = 5;

// 玻璃/iridescent 材质
const geometry = new THREE.TorusKnotGeometry(1, 0.3, 180, 32);
const material = new THREE.MeshPhysicalMaterial({
  transmission: 0.92,
  thickness: 1.5,
  roughness: 0.15,
  iridescence: 1,
  iridescenceIOR: 1.3,
  clearcoat: 1,
  color: 0xffffff,
});
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

// 环境光 + 点光源（染色）
scene.add(new THREE.HemisphereLight(0xffffff, 0x202020, 1));
const light1 = new THREE.PointLight(0x5EEAD4, 4, 20); light1.position.set(3, 3, 3); scene.add(light1);
const light2 = new THREE.PointLight(0xFB923C, 4, 20); light2.position.set(-3, -2, 3); scene.add(light2);

// ScrollTrigger 驱动旋转
gsap.to(mesh.rotation, {
  y: Math.PI * 2, x: Math.PI,
  scrollTrigger: {
    trigger: '.webgl-scene',
    start: 'top bottom', end: 'bottom top',
    scrub: 1,
  },
});

// 渲染
function tick() {
  mesh.rotation.z += 0.002; // 自转底噪
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
tick();

// Resize
new ResizeObserver(() => {
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  camera.aspect = canvas.clientWidth / canvas.clientHeight;
  camera.updateProjectionMatrix();
}).observe(canvas);
```

### 设计指南
- **单页不超过 1 个 WebGL scene**（多于 1 会撑爆 GPU，尤其移动端）
- 几何体建议：TorusKnot / Möbius 带 / Shader 球 / BoxGeometry（看风格）
- 材质：`MeshPhysicalMaterial` 的 `transmission + iridescence` 是 doubao 同款配方
- 相机 FOV 40-55°，物体距相机 3-5（太近会鱼眼失真）
- 粒子/光晕：在物体周围加 50-200 个小球（sprite），形成"尘埃"感
- 移动端降级：检测 `navigator.hardwareConcurrency < 4` 或 `matchMedia('(max-width: 640px)')`，直接换成静态大图

### 依赖体量
- Three.js core: ~150KB gzipped
- OGL（轻量替代）: ~15KB，但需要自己写 shader
- 推荐走 Three.js，因为社区材质/loader 成熟

---

## Pattern 5 — Section Title Bloom / Ghost（大标题光晕/幽灵影）

**出处**：doubao 的"研究领域"大标题
**效果**：Section 大标题后面带一个模糊、偏移、低透明度的副本，形成视觉纵深。

```css
.ghost-title {
  position: relative;
  font-size: clamp(56px, 8vw, 120px);
  font-weight: 900;
  color: var(--text-1);
}
.ghost-title::before {
  content: attr(data-ghost);
  position: absolute; left: 4px; top: 4px;
  color: var(--accent-warm);
  opacity: 0.3;
  filter: blur(8px);
  z-index: -1;
}
```

---

## Pattern 6 — Abstract Gradient Art Top（抽象渐变艺术顶）

**出处**：doubao 研究领域三卡片（语音 / 大语言模型 / 多模态）
**效果**：功能卡片上半部分是一块抽象艺术（渐变球/丝带/粒子），下半是文字。艺术部分可以是静态 PNG/SVG，也可以是 CSS mesh gradient。

```css
.art-card { background: var(--surface-1); border-radius: 16px; overflow: hidden; }
.art-top {
  aspect-ratio: 4 / 3;
  background:
    radial-gradient(circle at 30% 40%, var(--accent-cool) 0%, transparent 50%),
    radial-gradient(circle at 70% 60%, var(--accent-warm) 0%, transparent 45%),
    radial-gradient(circle at 50% 80%, #c084fc 0%, transparent 40%);
  filter: blur(0) saturate(140%);
}
.art-top.animated {
  background-size: 200% 200%;
  animation: artShift 18s ease-in-out infinite alternate;
}
@keyframes artShift {
  to { background-position: 100% 100%; }
}
```

加铆钉装饰（doubao 的卡片四角+四边都有小方块，仿照旧相纸/证件）：

```css
.art-card { position: relative; }
.art-card::before, .art-card::after,
.art-card > .rivet-tl, .art-card > .rivet-tr,
.art-card > .rivet-bl, .art-card > .rivet-br {
  content: ''; position: absolute; width: 6px; height: 6px;
  background: var(--surface-2); border: 1px solid var(--border);
  transform: rotate(45deg);
}
.art-card::before { top: 8px; left: 8px; }
.art-card::after { top: 8px; right: 8px; }
.rivet-bl { bottom: 8px; left: 8px; }
.rivet-br { bottom: 8px; right: 8px; }
```

---

## 降级与性能

| 设备条件 | 降级策略 |
|----------|----------|
| `prefers-reduced-motion: reduce` | 所有 pin-scrub 改为简单 fade；关闭 WebGL |
| `matchMedia('(max-width: 640px)')` | Constellation 降为 3-4 张静态卡；pin-swap 保留但简化为一次性入场；WebGL 换静态图 |
| `navigator.hardwareConcurrency < 4` | 关闭 WebGL，关闭 blur filter，关闭 custom cursor |
| Safari（性能偏差） | 若 FPS < 40 自动禁用 filter blur |

性能检测：

```js
const perf = {
  isMobile: matchMedia('(max-width: 640px)').matches,
  isLowCore: navigator.hardwareConcurrency < 4,
  reduceMotion: matchMedia('(prefers-reduced-motion: reduce)').matches,
  noHover: !matchMedia('(hover: hover)').matches,
};
document.documentElement.dataset.perf = JSON.stringify(perf);
// CSS 可通过 [data-perf*='"isMobile":true'] 做条件样式
```
