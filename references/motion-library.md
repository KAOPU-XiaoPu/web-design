# Motion Library — vue-bits / reactbits

L2+ 页面的动效默认从 [vue-bits](https://github.com/DavidHDev/vue-bits) 或 [reactbits](https://github.com/DavidHDev/react-bits) 选取（同作者 DavidHDev，Vue / React 双端同一套效果，MIT 许可）。**能复用就不要重写。**

落地项目是纯 HTML 时，按效果源码的技术栈判断：
- 仅 CSS 的 → 直接复制 class + keyframes
- GSAP 驱动的 → 直接复制逻辑（GSAP 本身是框架无关的）
- Three.js / OGL 驱动的 → 复制 canvas 初始化逻辑
- 深度依赖 Vue/React 生命周期的 → 抽成 `init()` / `destroy()` 对函数

---

## 硬性要求（L2+ 强制）

任何 L2 以上的页面至少包含以下 6 类动效组合，**缺一项都算未达标**：

| 类别 | 至少数量 | 落点建议 |
|------|----------|----------|
| Text Animation — Hero H1 | 1 | 首屏大标题（入场 / 持续态）|
| Text Animation — Section H2 | 1 | 章节标题（滚动触发）|
| Text Animation — Body / Label | 1 | 正文 / eyebrow / 代码行 |
| Animation — 元素级 | ≥ 1 | 按钮磁吸、卡片 hover、光标、装饰元素 |
| Component — 交互构件 | ≥ 1 | 卡片栈、画廊、菜单、3D 卡片等 |
| Background — 氛围层 | 1 | Hero 背景或 section 底层 |

**同一页面累计不少于 4 个 signature moments**。L3 页面建议 6-8 个，但不要超过 10（会躁）。

---

## 目录（截至 2026-04）

### Text Animations（24 个）

| 名称 | 一句话 | 适合 | 标签 |
|------|--------|------|------|
| ASCIIText | 文字用 ASCII 字符重新构建 | 技术感、终端风 | 重、装饰 |
| BlurText | 字符逐个模糊 → 清晰入场 | 通用入场 | 轻、优雅 |
| CircularText | 文字沿圆形路径排列 | Logo 环绕、装饰徽章 | 轻、装饰 |
| CountUp | 数字滚动到目标值 | 数据统计、KPI | 轻、功能 |
| CurvedLoop | 文字在曲线上循环流动 | 滚动 marquee、引用 | 轻、装饰 |
| DecryptedText | 字符乱码 → 解码真实字符 | 技术/密码风标语 | 中、技术 |
| FallingText | 文字像物理下坠重排 | 重点段落装饰 | 重、娱乐 |
| FuzzyText | 文字带噪点震颤 | 故障艺术 | 重、装饰 |
| GlitchText | 故障位移 + 色差 | 赛博朋克 | 重、风格化 |
| GradientText | 文字填充渐变（可流动） | 关键词、Logo | 轻、通用 |
| RotatingText | 单词循环切换（打字机替代） | Hero 动词循环 | 轻、功能 |
| ScrambleText | 字符乱码 → 稳定 | 技术/文档风 eyebrow | 轻、技术 |
| **ScrollFloat** | 随滚动浮入并保持精确位置 | **Section H2 首选** | 轻、通用 |
| **ScrollReveal** | 随滚动词/行逐个显现 | **正文段落首选** | 轻、通用 |
| ScrollVelocity | 文字速度跟滚动速度联动 | 装饰横条、视差 | 中、装饰 |
| ShinyText | 金属光泽扫过文字 | CTA、关键标语 | 轻、品牌感 |
| Shuffle | 文字字符位置洗牌 | 转场 | 中、娱乐 |
| **SplitText** | 字符/词/行逐个 stagger 入场 | **Hero H1 首选** | 轻、经典 |
| TextCursor | 光标打字效果 | 终端感、引导文案 | 轻、功能 |
| TextPressure | 字重随鼠标距离变化 | 交互性 Hero 标题 | 中、实验 |
| TextTrail | 字符留下视觉余迹 | 视差装饰 | 中、装饰 |
| TextType | 打字机逐字输入 | 代码块、命令行 | 轻、功能 |
| TrueFocus | 焦点字清晰其余模糊 | 引导读者视线 | 中、功能 |
| VariableProximity | 鼠标靠近处字体变粗 | 可变字体展示 | 中、实验 |

### Animations — 元素级（29 个）

| 名称 | 一句话 | 标签 |
|------|--------|------|
| AnimatedContent | 通用入场（fade/slide/scale） | 轻、通用 |
| Antigravity | 鼠标靠近时元素反推 | 中、实验 |
| BlobCursor | 光标变形 blob | 中、装饰 |
| ClickSpark | 点击溅出粒子 | 轻、反馈 |
| Crosshair | 十字光标 | 中、实验 |
| Cubes | 3D 立方体网格自转 | 重、装饰 |
| ElectricBorder | 边框电流光环 | 中、品牌感 |
| FadeContent | 简单淡入 | 轻、基础 |
| GhostCursor | 带拖影光标 | 轻、装饰 |
| GlareHover | 卡片 hover 时高光扫过 | 轻、品牌感 |
| GradualBlur | 渐进模糊 | 轻、过渡 |
| ImageTrail | 鼠标拖出图片尾迹 | 重、娱乐 |
| LaserFlow | 激光流动 | 重、装饰 |
| LogoLoop | 品牌 logo 无限横滚 | 轻、功能 |
| MagicRings | 装饰光环 | 中、装饰 |
| **Magnet** | 元素磁吸鼠标 | **CTA 首选**（轻）|
| MagnetLines | 磁力线装饰 | 中、装饰 |
| MetaBalls | 流体球 | 重、装饰 |
| MetallicPaint | 金属涂层光泽 | 中、品牌感 |
| Noise | 噪点纹理 | 轻、底噪 |
| OrbitImages | 图片轨道旋转 | 中、装饰 |
| PixelTrail | 像素化鼠标尾迹 | 中、风格 |
| PixelTransition | 像素化转场 | 中、转场 |
| Ribbons | 丝带飘动 | 中、装饰 |
| ShapeBlur | 形状模糊动态 | 中、装饰 |
| SplashCursor | 鼠标溅射 | 重、娱乐 |
| StarBorder | 边框流动星点 | 中、品牌感 |
| StickerPeel | 贴纸翘边 | 中、娱乐 |
| TargetCursor | 瞄准线光标 | 中、实验 |

### Components — 交互构件（30 个）

| 名称 | 一句话 | 标签 |
|------|--------|------|
| AnimatedList | 列表项动画入场 | 轻、通用 |
| BorderGlow | 边框发光追踪 | 中、品牌感 |
| BounceCards | 卡片弹性展开 | 中、趣味 |
| BubbleMenu | 气泡菜单 | 中、趣味 |
| CardNav | 卡片式导航 | 轻、通用 |
| **CardSwap** | 卡片 3D 切换堆叠 | **Hero 卡片展示首选** |
| Carousel | 基础轮播 | 轻、通用 |
| ChromaGrid | 色差网格 | 中、风格 |
| CircularGallery | 圆形画廊 | 中、装饰 |
| Counter | 动态计数 | 轻、功能 |
| DecayCard | 衰减卡片动画 | 中、装饰 |
| Dock | macOS 风停靠栏 | 轻、功能 |
| DomeGallery | 球面画廊 | 重、装饰 |
| ElasticSlider | 弹性滑动条 | 轻、功能 |
| FlowingMenu | 流动菜单 | 中、装饰 |
| FlyingPosters | 海报飞行 | 重、娱乐 |
| Folder | 文件夹动画 | 轻、趣味 |
| GlassIcons | 玻璃图标 | 轻、装饰 |
| GlassSurface | 玻璃表面 | 中、装饰 |
| GooeyNav | 胶质导航 | 中、趣味 |
| InfiniteMenu | 无限菜单 | 中、装饰 |
| **InfiniteScroll** | 无限横滚/纵滚作品条 | **Showcase 首选** |
| **MagicBento** | Bento 网格 + hover 光效 | **Feature 网格首选** |
| Masonry | 瀑布流 | 轻、通用 |
| PillNav | 胶囊导航 | 轻、通用 |
| PixelCard | 像素化卡片 | 中、风格 |
| ProfileCard | 3D 翻转名片 | 轻、趣味 |
| RollingGallery | 滚轮画廊 | 中、装饰 |
| **ScrollStack** | 滚动卡片堆叠（pin + 叠加） | **叙事卡片首选** |
| **SpotlightCard** | 鼠标跟随聚光灯卡片 | **Feature 卡片首选** |
| Stack | 卡片堆叠 | 轻、通用 |
| StaggeredMenu | Stagger 入场菜单 | 轻、通用 |
| Stepper | 步骤器 | 轻、功能 |
| **TiltedCard** | 3D 倾斜（陀螺仪 / 鼠标） | **作品展示首选** |

### Backgrounds — 氛围层（38 个）

| 名称 | 一句话 | 性能 | 标签 |
|------|--------|------|------|
| **Aurora** | 柔软极光流动 | 中（WebGL） | **编辑暗色首选** |
| Balatro | 扑克风底纹 | 中 | 风格化 |
| Ballpit | 物理小球池 | 重 | 趣味 |
| Beams | 光束扫过 | 中 | 科技 |
| ColorBends | 色彩弯折 | 中 | 艺术 |
| DarkVeil | 深色面纱 | 轻 | 编辑暗色备选 |
| Dither | 抖动像素 | 轻 | 复古 |
| DotGrid | 点阵网格 | 轻 | 极简 |
| EvilEye | 眼睛追踪 | 中 | 实验 |
| FaultyTerminal | 故障终端 | 中 | 赛博 |
| FloatingLines | 浮动线条 | 轻 | 极简 |
| Galaxy | 星系 | 中 | 科技 |
| GradientBlinds | 渐变百叶 | 轻 | 风格化 |
| Grainient | 颗粒渐变 | 轻 | 编辑风 |
| GridDistortion | 网格扭曲 | 中 | 实验 |
| GridMotion | 网格流动 | 轻 | 科技 |
| GridScan | 扫描线网格 | 中 | 赛博 |
| Hyperspeed | 超光速隧道 | 重 | 赛博 |
| Iridescence | 虹彩光泽 | 中 | 品牌感 |
| LetterGlitch | 字符故障墙 | 重 | 赛博 |
| LightPillar | 光柱 | 中 | 戏剧 |
| LightRays | 光线放射 | 中 | 戏剧 |
| Lightning | 闪电 | 中 | 戏剧 |
| LineWaves | 线条波浪 | 轻 | 极简 |
| LiquidChrome | 液态铬合金 | 中 | 品牌感 |
| LiquidEther | 液态以太 | 中 | 艺术 |
| Orb | 能量球 | 中 | 装饰 |
| Particles | 粒子系统 | 中 | 通用 |
| PixelBlast | 像素爆破 | 重 | 赛博 |
| PixelSnow | 像素雪 | 轻 | 季节 |
| Plasma | 等离子 | 中 | 艺术 |
| Prism | 棱镜色散 | 中 | 品牌感 |
| PrismaticBurst | 棱镜爆破 | 重 | 戏剧 |
| Radar | 雷达扫描 | 轻 | 科技 |
| RippleGrid | 涟漪网格 | 中 | 装饰 |
| **Silk** | 丝绸流动 | 中 | **编辑暗色/亮色通用** |
| SoftAurora | 柔和极光（轻量版） | 轻 | 编辑暗色备选 |
| Squares | 方格 | 轻 | 极简 |
| Threads | 丝线 | 轻 | 极简 |
| Waves | 波浪 | 轻 | 极简 |

---

## 按风格 × 场景的推荐组合

### Dark Editorial（hueapp / Linear 骨架类）
- Background: **Aurora** / **Silk** / **SoftAurora** / **Grainient**
- Hero H1: **SplitText** 或 **ShinyText**（关键词） + **GradientText**（关键词）
- H2: **ScrollFloat** 或 **BlurText**
- Body: **ScrollReveal**
- Animation: **Magnet**（CTA） + **GlareHover**（卡片）
- Component: **CardSwap** / **ScrollStack** / **SpotlightCard** / **MagicBento**

### Dark Tech / Cyber（cursor / warp / 赛博）
- Background: **LetterGlitch** / **Beams** / **Hyperspeed** / **FaultyTerminal**
- Hero H1: **GlitchText** / **DecryptedText** / **ShinyText**
- H2: **SplitText**
- Body: **TextType**（代码块） + **ScrambleText**（eyebrow）
- Animation: **ElectricBorder** / **ClickSpark**
- Component: **TiltedCard** / **PixelCard**

### Minimal Pure / Editorial Light
- Background: **DotGrid** / **FloatingLines** / **Grainient**
- Hero H1: **SplitText**（克制）+ **GradientText**（仅关键词）
- H2: **ScrollFloat**
- Body: **ScrollReveal**
- Animation: **Magnet**（CTA，唯一动效） + **FadeContent**
- Component: **CardNav** / **InfiniteScroll** / **Masonry**

### Playful Creative
- Background: **Iridescence** / **LiquidChrome** / **Plasma**
- Hero H1: **TextPressure** / **FallingText** / **BounceCards** 文案
- H2: **Shuffle** / **SplitText**
- Body: **TextTrail** / **ScrollReveal**
- Animation: **ClickSpark** / **BlobCursor** / **StickerPeel**
- Component: **BounceCards** / **BubbleMenu** / **GooeyNav** / **FlyingPosters**

### Chinese Elegant
- Background: **Threads** / **FloatingLines** / **Grainient**（低对比度）
- Hero H1: **BlurText**（缓慢）+ **GradientText**（赭石渐变）
- H2: **ScrollFloat**
- Body: **ScrollReveal**（行粒度，不要字粒度——中文字粒度太碎）
- Animation: **Magnet**（克制）
- Component: **CircularGallery** / **Masonry**

### Warm Professional
- Background: **Silk** / **SoftAurora** / **Grainient**
- Hero H1: **SplitText** + **GradientText**
- H2: **ScrollFloat**
- Body: **ScrollReveal**
- Animation: **Magnet** + **GlareHover**
- Component: **MagicBento** / **SpotlightCard** / **InfiniteScroll**

---

## 性能原则

- 一个页面不并存超过 **2 个重背景**（WebGL 背景只用 1 个）
- 移动端（< 640px）自动降级：重背景 → 静态渐变；3D 组件 → 2D 版本
- Cursor 相关效果仅在 `matchMedia('(hover: hover)')` 下启用
- 所有效果必须有 `prefers-reduced-motion` 降级路径
- 单页 GSAP timeline ≤ 3 个（更多会抢主线程）

## 复用规则

1. **优先直接复制**：vue-bits / reactbits 源码是 MIT，保留作者致谢就能用
2. **翻译层**：原 Vue / React 代码移植到 vanilla HTML 时，把 props 展开为 data-attr 或函数参数
3. **致谢位置**：页面 footer 或 README 加 "Motion effects inspired by / derived from [vue-bits](https://github.com/DavidHDev/vue-bits) by DavidHDev (MIT)"
