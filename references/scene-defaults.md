# Scene Defaults

每种场景的默认布局、组件和交互基线。Round 1 确认场景后加载，作为后续对话的起点。

---

## Landing Page / 产品介绍页

```yaml
layout:
  structure: 纵向多 section 叙事（Hero → Features → Social Proof → CTA）
  container: 1200px max, 居中
  section_spacing: 80-120px
  grid: 自由混排（1/2/3 列按内容切换）

components:
  必要: Hero (大标题+副标题+CTA), 导航栏, Feature 卡片, CTA 按钮, Footer
  常见: 客户 Logo 滚动条, 定价卡片, FAQ 折叠, Testimonial 卡片
  可选: 视频嵌入, 数据统计, 对比表格

interaction_baseline: L2
  - 导航: sticky, 滚动后背景模糊
  - 入场: section 级 fadeInUp + 内部 stagger
  - Hero: 2-3 层 stagger 入场
  - 卡片: hover lift + shadow
  - CTA: hover scale + 色变
  - 滚动: 进度条（可选）

typography:
  hero_size: 3.5-5rem
  section_title: 2-2.5rem
  body: 1-1.125rem
  density: 中等（标题+段落+留白交替）
```

---

## Portfolio / 作品集

```yaml
layout:
  structure: Hero + 项目网格 + 关于我 + 联系
  container: 1100-1400px
  grid: 2-3 列 masonry 或等高网格
  项目详情: 弹窗 / 新页面 / 展开

components:
  必要: 项目卡片 (封面+标题+标签), 筛选/分类, 联系方式
  常见: 技能标签, 时间线, 社交链接
  可选: 光标自定义, 项目详情页, 暗色模式切换

interaction_baseline: L2-L3
  - 项目卡片: hover 图片缩放 + 信息浮现
  - 图片: lightbox 或全屏预览
  - 滚动: reveal + 视差
  - 页面转场: 跨页动画（L3）
  - 光标: 自定义光标或磁性效果（L3）

typography:
  hero_size: 4-6rem (可以很大)
  body: 0.95-1rem
  density: 低（大量留白，图片主导）
```

---

## Blog / 内容站

```yaml
layout:
  structure: 文章列表 / 单篇文章
  container: 720-800px (窄容器，阅读最佳)
  sidebar: 可选（目录/标签/推荐）
  间距: 段落间 1.5-2em

components:
  必要: 文章卡片, 文章正文排版, 日期/标签, 分页
  常见: 目录(TOC), 代码块, 引用块, 图片灯箱
  可选: 评论区, 搜索, RSS, 暗色模式

interaction_baseline: L1
  - 入场: 轻微 fadeIn
  - 文章卡片: hover 色变或轻浮起
  - 目录: 滚动高亮当前章节
  - 代码块: 一键复制
  - 图片: 点击放大

typography:
  article_title: 2-2.5rem
  body: 1-1.0625rem, line-height 1.7-1.8
  中文额外: 字距 0.02em, 首行缩进 2em
  density: 高（文字密集，靠行高和段距呼吸）
```

---

## Dashboard / 数据面板

```yaml
layout:
  structure: 侧边栏 + 顶栏 + 内容区
  container: 全宽（侧栏 240-280px, 内容区自适应）
  grid: 密集网格（2-4 列, gap 12-16px）
  间距: 紧凑（16-24px section 间距）

components:
  必要: 侧边导航, 数据卡片, 图表容器, 表格, 筛选器
  常见: KPI 数字, 状态徽章, 面包屑, 通知, 加载骨架
  可选: 实时更新指示, 暗色模式, 可拖拽卡片

interaction_baseline: L1
  - 数据卡片: hover 边框高亮（不要 lift，影响信息密度）
  - 表格行: hover 背景色变
  - 侧栏: 可折叠, 当前项高亮
  - 加载: 骨架屏脉冲
  - 状态: 数字变化过渡动画（数字滚动）
  - 注意: 不要用 scroll reveal（信息需要立即可见）

typography:
  page_title: 1.5rem
  card_title: 0.875-1rem
  body: 0.8125-0.875rem
  数字: 1.5-2.5rem, font-weight 700-800
  density: 高（信息密集，靠网格和边框区隔）
```

---

## PPT / 课件 / 知识地图

```yaml
layout:
  structure: Hero + 分节导航 + Bento 网格内容区
  container: 1280px
  grid: 3 列 Bento (span-1/span-2/span-3 混排)
  gap: 14px
  间距: section 间 48-64px

components:
  必要: 导航标签(pill), 模块卡片, Hero 统计, 分节标题
  常见: 进度指示, 难度标签, 知识点卡片, 时间线
  可选: 目录, 下载按钮, 评估表单

interaction_baseline: L1
  - 导航: 锚点滚动 + 当前项高亮 (IntersectionObserver)
  - 卡片: hover 边框加深 + 轻阴影
  - 标签: hover 反色
  - 打印: @media print 隐藏导航, 单列排版
  - 注意: 避免滚动动画（课件需要快速浏览和打印）

typography:
  hero_title: 3-3.5rem (serif, 装饰性)
  section_title: 1.5rem (serif)
  card_title: 0.95rem (sans, bold)
  body: 0.82-0.85rem
  labels: 0.65-0.72rem, uppercase, letter-spacing
  density: 中高（信息量大但靠卡片边界组织）
```

---

## App UI / 管理后台

```yaml
layout:
  structure: 顶栏 + 侧栏（可选）+ 内容区 + 弹窗/抽屉
  container: 全宽, 内容区 max 1400px
  grid: 按功能分区, 1-3 列自适应
  间距: 中等（24-32px）

components:
  必要: 按钮(多状态), 表单(input/select/checkbox), 表格, 弹窗/抽屉
  常见: Toast 通知, 步骤条, Tabs, 下拉菜单, 分页
  可选: 拖拽, 富文本编辑, 文件上传, 骨架屏

interaction_baseline: L1-L2
  - 按钮: hover/active/disabled/loading 四态
  - 表单: focus ring, 校验反馈, 错误高亮
  - 弹窗: 背景模糊 + 内容 scaleIn
  - Toast: slideIn + 自动消失
  - 列表: 拖拽排序（如需要）
  - 过渡: 页面切换 fade（不要 slide，影响导航预期）

typography:
  page_title: 1.25-1.5rem
  body: 0.875rem
  label: 0.75rem
  density: 中等（功能优先，适度留白）
```

---

## 邮件模板

```yaml
layout:
  structure: Logo 头部 + 正文 + CTA + 页脚
  container: 600px max (邮件客户端限制)
  grid: 单列或 2 列（table-based, 非 CSS grid）
  间距: 20-30px padding

components:
  必要: 头部(Logo+标题), 正文段落, CTA 按钮, 页脚(退订链接)
  常见: 产品卡片, 图片+文字横排, 分隔线
  注意: 所有样式必须内联, 不支持 CSS class

interaction_baseline: 无（邮件不支持 JS）
  - CTA 按钮: 用 table+td 实现圆角, 内联 background-color
  - 链接: 内联 color, text-decoration
  - 图片: 必须设 width, alt text, display:block

typography:
  title: 24-28px
  body: 15-16px, line-height 1.5-1.6
  安全字体: Arial, Helvetica, Georgia, Times New Roman
  禁止: Google Fonts, 自定义字体（部分客户端不支持）
  density: 低（邮件阅读环境干扰大，需要大字号和留白）

constraints:
  - 所有样式内联（不支持 <style> 在所有客户端）
  - 布局用 <table>, 不用 flexbox/grid
  - 图片宽度不超过 580px
  - 总宽度 600px
  - 不使用 JS
  - 背景图用 VML fallback（Outlook）
```
