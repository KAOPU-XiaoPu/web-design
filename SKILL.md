---
name: web-design
description: Web 视觉设计 SKILL。输入 PRD / 参考 URL / 截图 / 关键词（任意组合），先产出一份标准化 DESIGN.md 设计规范，用户确认后据此生成 UI/UX、视觉、动效、响应式全部达标的 web 代码。专攻 web 端：Landing Page、Portfolio、产品页、博客、个人站、SaaS 介绍页等。当用户说"帮我做个网站""设计一个页面""参考 XX 做一个""把这个截图/PRD 做成网页""做一个 landing page""出一份 design 规范"时触发。不用于后端、数据库、纯逻辑 bug 修复。
---

# Web Design

Web 端视觉设计 SKILL。两阶段工作流：**先出规范（DESIGN.md），再出代码。**

DESIGN.md 是显式文件产物，保存到项目目录，可跨项目复用、可手动修改、可给其他工具消费。

## 核心流程

```
Phase A  理解需求（灵活输入）──→  Phase B  输出 DESIGN.md（用户确认）──→  Phase C  生成项目代码
```

**启动时先检测**（按优先级）：
1. 项目里已经有 DESIGN.md 了吗？→ 有则沿用/修改/重建
2. 项目里有 PRD.md 吗？→ 有则进入 A4（PRD 驱动流程）
3. 都没有 → 正常走 Phase A

---

## Phase A: 理解需求

输入是灵活的，以下任意组合都行，不要强制用户走固定路径：

| 输入 | 处理方式 |
|------|---------|
| **参考 URL** | 抓取 HTML+CSS，提取 Token，motion audit |
| **截图 / 设计稿** | 从视觉提取气质、色温、密度、字体风格 |
| **关键词 / 描述** | "暗色克制衬线风格" → 从 style-seeds 匹配 Token |
| **品牌名** | "做成类似 Linear 的" → 先查 `references/design-systems/`，有则直接读取；无则抓取该网站 |
| **混合** | "参考这个 URL 但配色要暖一些" → 提取 + 覆盖 |
| **PRD 文档** | 读取 PRD.md 的产品定位、页面结构、设计交接区 → 分析竞品风格 → 推导设计方向 |

### A1. URL 分析（有参考 URL 时）

**意图判断**：参考（提取设计语言，做独立新页面）vs 复刻（用户明确说"复刻/clone"）。

**抓取流程**（按优先级尝试）：

1. **首选：Playwright 爬虫**（真实浏览器，能绕反爬、渲染 SPA、模拟滚动）
   ```bash
   python3 scripts/crawl_website.py --url [URL] --output ./crawl-output --scroll-delay 600
   ```
   输出：每屏视口截图 + tokens.json + structure.json + styles.css
   
2. **备选：Token 提取脚本**（轻量，适合简单静态站）
   ```bash
   python3 scripts/extract_design_tokens.py --url [URL] --format json
   ```

3. **降级：手动 curl**（脚本都不可用时）
   ```bash
   curl -Ls [URL]
   ```

综合三类输入判断：实际体验（氛围节奏）> 截图（局部气质）> Token 数值（精确参数）。Playwright 爬虫的视口截图可直接作为"体验"和"截图"两类输入。

**Motion Audit**（参考站有滚动联动动效时必做）：
- 触发信号：动效跟随滚动连续变化 / 模块间有 stagger-pin-parallax / 引用 GSAP-Lenis 等
- 记录每个动效区块的 trigger、driver、elements、effect、timing

**降级链路**：
- Playwright 爬虫失败 → 查 `references/design-systems/` 有无该品牌预置文件（58 个品牌）
- 预置文件也无 → `extract_design_tokens.py` 尝试静态提取
- 静态提取也失败 → 手动 curl CSS
- 全部失败 → 要求用户提供截图，从视觉手动建 Token

### A2. 对话引导（无参考物时）

快速锁定风格方向，不要机械走问答清单：

**核心问题**（按需选问，不全问）：
- 亮色 vs 暗色？
- 衬线 vs 无衬线？
- 克制留白 vs 丰富饱满？
- 强调色偏好？
- 有没有喜欢的网站或风格参考？

从 `references/style-seeds.md` 匹配最近似的种子（10 种预设方向），展示给用户确认或混搭。

用户提到具体品牌时，查阅 `references/design-systems/INDEX.md` 按类别检索，按需读取对应品牌文件（58 个真实网站设计规范，每个 ~300 行）。品牌文件只含静态设计系统，动效仍需按交互档位补充。

### A3. 交互档位确认（不可跳过）

| 档位 | 体验感 |
|------|--------|
| **L1** 精致静态 | 优雅 hover + 柔和入场 |
| **L2** 流畅交互 | 滚动 reveal、视差、导航变化 |
| **L3** 沉浸体验 | 滚动驱动时间线、pin、光标跟随、转场 |

L2 追问：reveal 风格（fadeInUp/scaleIn）、视差、导航变化
L3 追问：section pin、光标效果、转场、是否允许 GSAP/ScrollTrigger/Lenis

查阅 `references/interaction-patterns.md` 获取对应档位的完整代码。

### A4. PRD 驱动（检测到项目级规范文件时）

**启动时自动扫描项目根目录**，按优先级：
1. `PRD.md` / `prd.md`
2. `SPEC.md` / `spec.md`
3. `README.md` 或任何 `.md` — 若含「产品定位 / Target Users / Pages / 核心页面」等关键字段

**不绑定特定工具或模板**。只要能从文档里抽到下列字段，就足以作为设计输入：

| 字段（中/英别名） | 用途 |
|-------------------|------|
| 产品名称 / Product / Name | Hero 文案 |
| 一句话定位 / Tagline / Pitch | Hero 副标题、定调 |
| 目标用户 / Target Users / Audience | 色彩温度、字体风格决策 |
| 核心页面 / Pages / Screens | Phase C 生成清单 |
| 竞品 / Competitors / References | Phase A 风格参考起点 |
| 技术栈 / Tech Stack | Phase C 代码生成方案 |
| 设计交接 / Design Notes / 调性 | 直接继承的硬约束 |

**竞品风格分析**：
- PRD 提到竞品 → 优先查 `references/design-systems/` 是否已有预置
- 有预置 → 读取该品牌规范作为起点
- 无预置 → 调用 `scripts/crawl_website.py` 抓取提取
- PRD 没提 → 按产品类型 + 调性从 `references/style-seeds.md` 匹配最近种子

**提取不到关键字段时**：不要瞎猜，回到对话引导（A2）补齐。

**与用户确认**（示例）：
> 我从 `{文件名}` 读到了：
> - 产品：{名称} — {一句话定位}
> - 目标用户：{画像}
> - 参考竞品：{列表 或 "无"}
> - 建议的风格方向：{1-2 个候选，各附一句理由}
>
> 这个方向对吗？

确认后进入 A3（交互档位），然后 Phase B。

---

## Phase B: 输出 DESIGN.md（必走）

**必须生成 DESIGN.md 文件。** 按 `references/design-md-template.md` 模板输出 9 个章节：

1. **Visual Theme & Atmosphere** — 设计哲学、氛围关键词、一句话定调
2. **Color Palette & Roles** — 完整 CSS 变量定义（含 RGB 辅助值）
3. **Typography Rules** — 字体族、Google Fonts URL、字号层级表、禁止字体
4. **Component Stylings** — 按钮/卡片/导航/链接/标签等完整 CSS（含所有状态）
5. **Layout Principles** — 网格、间距梯度、容器宽度
6. **Depth & Elevation** — 阴影体系
7. **Animation & Interaction** — 动效档位、入场/滚动/悬停/特效的完整代码
8. **Do's and Don'ts** — 设计护栏、Anti-Patterns（至少 8 条）
9. **Responsive Behavior** — 断点、触摸目标、折叠策略

**文字装饰规则**：生成 Color Palette 和 Typography 后，按 `references/text-decoration-rules.md` 决策表对标题逐级判断是否添加渐变/投影。

**展示摘要给用户确认**，确认后保存 DESIGN.md 到项目目录，再进入 Phase C。

---

## Phase C: 生成项目代码（必走）

### C1. 确认场景 + 收集内容

问用户做什么页面，收集具体内容。查阅 `references/scene-defaults.md` 获取该场景的布局和组件基线。

**常见场景的内容需求**：

| 场景 | 需要收集 |
|------|---------|
| Landing Page | 标题、副标题、Feature 列表、CTA、Social proof |
| 个人站 / Portfolio | 名字、头衔、项目列表、关于、联系方式、博客列表 |
| Blog | 名称、文章列表/内容、作者信息、分类标签 |
| 产品页 | 产品名、卖点、功能截图、定价、FAQ |

用户信息不全时主动问；用户说"你先做，内容我后面填"则用合理的占位内容。

### C2. 设计框架 + 生成代码

1. **检查项目环境**：框架、路由、样式方案、现有组件和 assets
2. **框架决策**：有项目 → 沿用；无项目 → 最小可行方案
3. **严格按 DESIGN.md 生成**：
   - 所有颜色通过 CSS 变量引用
   - 字体按 DESIGN.md 定义使用
   - 交互按 DESIGN.md 指定档位实现
   - 不违反 Do's and Don'ts
4. **图片策略**：用户素材 > 项目 assets > 参考站 URL 占位 > Unsplash
5. **图标策略**：项目现有库 > lucide-react > 内联 SVG（参考 `references/icon-library.md`）

### C3. 审计

- **DESIGN.md 合规检查**：代码是否严格遵循规范
- **参考物差异审计**（有参考时）：Token / 版式 / 字体 / 交互 / 素材逐项比对
- **响应式验证**：至少移动端 + 桌面端
- **质量清单**：读 `references/quality-checklist.md` 逐项自检

---

## 首页爆点原则（Landing Page 专属）

一个 Web 平台最重要的是**落地页（首页）**。其他页面保持规范、风格统一即可，唯有首页必须满足下面两条硬性原则，不可妥协。

### 原则一：3 个「卧槽」爆点 + 1 个巧思

爆点位置**固定**，每个位置必须有一个让用户"卧槽"的视觉冲击：

| # | 位置 | 要求 | 典型招式 |
|---|------|------|---------|
| **1** | **首屏 / Hero** | 加载瞬间就被动态/3D/巨型渐变震住 | 卡片星座爆发、WebGL 3D 物体、巨型标题 mask reveal、鼠标跟随光斑、3D 卡片堆 |
| **2** | **首次滑动** | 离开首屏的第一个 section 必须有"钩子"继续吸引 | 宣言横滚带（大字 marquee）、数字爆发、分屏切割、卡片汇聚转场、全屏视频 |
| **3** | **列表 / 阵列 / 枚举 / 展示区** | 不能是普通等大 grid | Bento 不等大布局、SpotlightCard hover 跟踪光、3D 倾斜卡片、抽象艺术顶 |

**1 个巧思设计点**：一处"不注意就错过、一注意到就笑"的细节。候选：
- 交互反馈微动画（复制后的 sparkle + tooltip）
- 彩蛋（Konami / Ctrl+K 命令面板）
- Meta 梗（关键词 hover 弹 "这就是本页用到的规范 →"）
- 滚动到底的小惊喜（如"你看到这里了，谢谢"）

### 原则二：流畅 · 滑动无阻（不可破）

以下是性能红线，与爆点设计**同等优先级**。爆点炸裂但卡顿 = 零分。

- **3D / WebGL**：全页最多 1 处，且必须 IntersectionObserver 不可见时暂停
- **`filter: blur()` on moving elements**：禁止。用 opacity + scale 做景深代替
- **`backdrop-filter: blur()`**：值 ≤ 14px，且不覆盖大面积滚动区
- **Lenis / scroll-jacking**：仅当 pin-scrub 真正必要时启用；普通页面用原生 `scroll-behavior: smooth`
- **ScrollTrigger pin**：单页 ≤ 2 处（doubao 级叙事才解锁）
- **pointermove 监听**：必须 rAF 节流
- **Custom cursor 全局替换**：仅在气质强烈的设计类/工具类站点用，普通 SaaS 禁用

### 实现建议（性能友好的爆点配方）

这些组合实测在中等配置设备可达 60fps：

| 爆点 | 实现 | 性能成本 |
|------|------|---------|
| **鼠标聚光灯** | CSS var `--mx/--my` + `radial-gradient(at var(--mx) var(--my))` | ⭐ 极低（单次 repaint）|
| **卡片爆发入场** | GSAP 一次性 timeline（load 时 stagger 1.5s，结束即释放）| ⭐⭐ 低（仅 1 次）|
| **宣言横滚带** | 纯 CSS `transform: translateX` keyframes | ⭐ 极低 |
| **SpotlightCard** | 每张卡 `--mx/--my` + `::before` radial-gradient（rAF 节流）| ⭐⭐ 低 |
| **大字 mask reveal** | 纯 CSS `clip-path` 一次性动画 | ⭐ 极低 |
| **关键字渐变流动** | `background-position` 动画 | ⭐ 极低 |

避免的反面组合：
- ❌ 12+ 元素同时带 `filter: blur()` + `will-change`（GPU 内存爆）
- ❌ Lenis + 多个 pin-scrub + WebGL（主线程堵死）
- ❌ Three.js 常驻渲染不暂停（即使离开视窗也吃 FPS）

---

## 100 分质量底线（硬性验收）

DESIGN.md + 生成代码必须**同时**满足以下全部条件，任何一条不满足都算未完成。完整细项见 `references/quality-checklist.md`，这里是最核心的红线：

### DESIGN.md 红线
- 9 个章节都有实质内容，不是模板占位
- 每个组件样式包含 default / hover / active / focus / disabled **全部状态**
- 所有颜色定义为 CSS 变量，含 RGB 辅助值（便于 rgba）
- 字体有 `@import` URL + fallback stack
- 动效档位明确（L1/L2/L3），对应依赖声明完整
- Do's and Don'ts ≥ 8 条，其中 Don'ts ≥ 5 条
- L2+ 必须包含 `prefers-reduced-motion` 降级
- 响应式至少覆盖 Desktop + Mobile

### 代码红线
- 所有颜色通过 CSS 变量引用，**零硬编码 hex**
- 字体严格按 DESIGN.md 的 Typography Rules 实现
- 每个可交互元素有 hover + focus 态
- 入场动画已实现（至少 L1 级 fadeIn）
- L2+ 实现滚动 reveal + 导航滚动态 + 视差
- L3 实现 pin / 光标跟随 / 转场
- 图片**禁用纯色块占位**（参考站 URL / Unsplash / 用户素材）
- 图标用项目库 / lucide-react / 内联 SVG（Playful 调性外禁 Emoji）
- 未违反 DESIGN.md Do's and Don'ts 中的任何一条
- 移动端 ≤ 600px 无横向溢出，触摸目标 ≥ 44×44px

### 签名动效红线（L2+ 强制，L3 加倍）

**任何 L2 及以上页面必须包含以下 6 类动效，缺一不可**。优先从 [vue-bits / reactbits](https://github.com/DavidHDev/vue-bits) 目录挑（查 `references/motion-library.md`），能复用源码就不要自己写。

| 类别 | 数量 | 落点 |
|------|------|------|
| Text Animation — Hero H1 | ≥ 1 | 大标题入场或持续态（如 SplitText / ShinyText / GradientText） |
| Text Animation — Section H2 | ≥ 1 | 章节标题滚动触发（如 ScrollFloat / BlurText） |
| Text Animation — Body / Label | ≥ 1 | 正文、eyebrow、代码块（如 ScrollReveal / TextType / ScrambleText） |
| Animation — 元素级 | ≥ 1 | CTA 磁吸 / 卡片 hover / 光标 / 点击反馈（如 Magnet / GlareHover / ClickSpark） |
| Component — 交互构件 | ≥ 1 | 卡片栈 / 画廊 / 导航 / 3D 卡片（如 CardSwap / ScrollStack / SpotlightCard / MagicBento） |
| Background — 氛围层 | ≥ 1 | Hero 或全局背景（如 Aurora / Silk / Grainient / Threads） |

**L3 级别的累计 signature moments ≥ 6 个**，但一页不超过 10 个（会躁）。

### L3 电影级 scroll-story 硬性加码

L3 页面（用户说"像 doubao / apple / stripe 那样"、"要有 3D"、"普通"、"要电影感"等）除上述 6 类动效外，**必须再至少覆盖 3/4 的 scroll-story 模式**，详细模板见 `references/scroll-story-patterns.md`：

| 模式 | 必备 | 说明 |
|------|------|------|
| Pin-Scrub 场景 | ≥ 1 | section pin + 滚动驱动内容形变/时间线 |
| 左 pin / 右 swap 容器替换 | ≥ 1 | 左侧标题固定、右侧容器按滚动切换多场景（doubao 产品四连同款） |
| 汇聚/散开转场 | ≥ 1 | 多元素从散落飞向合并 或 反之（doubao hero→次屏同款） |
| WebGL / 真 3D 签名时刻 | ≥ 1 | Three.js / OGL / Babylon，不能只用 CSS 3D 充数 |

**黄金判据**：**每 1-2 屏必有一个 signature moment**。连续三屏只有 fade reveal 就不合格。

**性能底线**：
- 单页 WebGL scene ≤ 1 个
- 移动端自动降级（见 scroll-story-patterns.md 性能章节）
- `prefers-reduced-motion` 必须有完整降级路径

**风格适配**：严格参照 `references/motion-library.md` 的「按风格 × 场景推荐组合」——Dark Editorial 不要用 GlitchText，Playful 不要用 Aurora，调性一致比酷炫重要。

**性能底线**：
- 单页重背景（WebGL）≤ 1 个
- 移动端自动降级：重背景 → 静态渐变；3D 组件 → 2D
- Cursor 效果仅在 `matchMedia('(hover: hover)')` 下启用
- 所有效果必须有 `prefers-reduced-motion` 降级路径

**致谢**：使用 vue-bits / reactbits 源码时，在页面 footer 或 README 注明 "Motion effects derived from [vue-bits](https://github.com/DavidHDev/vue-bits) by DavidHDev (MIT)"。

### 参考物对齐审计（有参考时）
- 已数清参考站 section 数量
- 色板 / 字体 / 间距与参考数值对齐（或明确说明故意偏离的设计理由）
- 参考站有滚动动效 → 必做 motion audit 并实现对应档位
- 生成后显式做一次差异审计：列出哪些对齐、哪些故意不同

**审计不是可选步骤**。Phase C 代码写完必须逐条过一遍，未过的就地修。

---

## 技术栈原则

- **框架**：沿用项目已有栈；无则最小可行方案（静态 HTML 或 Vite）
- **样式**：沿用已有方案；不强行引入新依赖
- **组件**：有库复用；无库手写语义化组件
- **动画**：CSS 优先；L2 可用 IntersectionObserver；L3 允许 GSAP/ScrollTrigger/Lenis
- **图片**：禁止纯色块占位；占位图在代码顶部 `const IMG` 统一管理

---

## 语言规则

**默认跟随输入语言**，不强塞：

| 输入信号 | 默认生成语言 |
|----------|--------------|
| 参考 URL / 截图 / PRD 为中文 | 中文 |
| 参考 URL / 截图 / PRD 为英文 | 英文 |
| 用户对话语言 | 作为兜底判定 |

**多语言切换按需加**：
- 仅当用户明确要求，或 PRD 说明产品面向多市场时才加 i18n
- **不要默认往每个页面塞 locale 对象和语言切换器**——单语言产品里这是噪音
- 需要 i18n 时：
  - 文案集中到独立 locale 对象（`const messages = { zh: {...}, en: {...} }`），组件内 `t('hero.title')` 引用
  - 切换即时生效，不要刷新
  - 简单项目：顶层 locale + React state；Next.js：`next-intl` / `i18next`；纯 HTML：`<select>` + `data-lang`

**中文页面专属要求**（生成中文内容时必守）：
- 中文字体用 Noto Sans SC / Noto Serif SC / LXGW WenKai 等中文字族，禁止只配英文字体让系统回退
- 行高 ≥ 1.7，字距 `letter-spacing: 0.02em`
- 正文字号 ≥ 15px，长篇阅读 ≥ 16px
- 中英混排：中文字族在前，英文字族（Inter / DM Sans）作为 fallback，靠 `font-family` 链接入

---

## 参考文件索引

| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `references/design-md-template.md` | DESIGN.md 输出模板（9 章节） | Phase B |
| `references/interaction-patterns.md` | L1/L2/L3 三档交互代码库 | Phase A + B |
| `references/motion-library.md` | vue-bits/reactbits 效果目录 + 按风格推荐组合 | Phase B（选型）+ Phase C（落地） |
| `references/scroll-story-patterns.md` | L3 电影级 scroll-story 招式库（卡片星座 / 左pin右swap / 汇聚转场 / WebGL 签名） | Phase B（L3 判定后）+ Phase C |
| `references/style-seeds.md` | 10 种风格种子 → Token 映射 | Phase A 对话时 |
| `references/scene-defaults.md` | 7 种场景的布局/组件/交互基线 | Phase C |
| `references/text-decoration-rules.md` | 文字渐变/投影决策表 | Phase B |
| `references/icon-library.md` | lucide-react 图标速查 | Phase C |
| `references/quality-checklist.md` | 质量检查清单 | Phase C 审计 |
| `references/design-systems/INDEX.md` | 58 个品牌设计系统索引 | Phase A 用户提到品牌时 |
| `references/design-systems/{name}.md` | 单个品牌完整设计规范 | 按需读取，禁止全量加载 |
| `scripts/crawl_website.py` | Playwright 爬虫（截图 + Token + 结构） | Phase A 首选 |
| `scripts/extract_design_tokens.py` | 轻量 Token 提取（静态站备选） | Phase A 备选 |
| `scripts/fetch_unsplash_images.py` | 占位图候选 URL | Phase C |
