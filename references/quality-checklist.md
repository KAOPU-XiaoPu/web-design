# 质量检查清单

Phase C 代码生成完成后，逐项自检。

## DESIGN.md 合规（必查）

- [ ] 已生成 DESIGN.md 并保存到项目目录
- [ ] DESIGN.md 包含完整 9 个章节，无空章节
- [ ] 代码中所有颜色通过 DESIGN.md 定义的 CSS 变量引用，无硬编码 hex
- [ ] 字体严格按 DESIGN.md 的 Typography Rules 使用
- [ ] 交互效果严格按 DESIGN.md 指定的档位（L1/L2/L3）实现
- [ ] 未违反 DESIGN.md 的 Do's and Don'ts 中的任何一条

## 参考网站解析（有参考 URL 时）

- [ ] 综合体验感知 + Token 提取 + 截图对照三类输入分析
- [ ] 使用脚本或 curl 抓取原始 HTML/CSS，未单纯依赖 AI 摘要
- [ ] 已数清参考站所有 section 模块
- [ ] 若有滚动联动动效，已做 motion audit
- [ ] 生成完成后对结果与参考物做过显式差异审计

## 字体

- [ ] 字体按 DESIGN.md 选取，有 Google Fonts @import URL + fallback
- [ ] 已按 text-decoration-rules.md 对 h1/h2/h3 执行装饰判断
- [ ] **场景化字号要求**（从 `scene-defaults.md` 取对应场景字号，不要一刀切）：
  - Landing / Portfolio Hero：≥ 60px、weight ≥ 700
  - Blog / 文章：Hero 32-40px，body 1-1.0625rem，行高 1.7-1.8
  - Dashboard / App UI：页面标题 1.25-1.5rem，正文 0.875rem
  - PPT / 课件：Hero 3-3.5rem（serif），正文 0.82-0.85rem
  - 邮件：标题 24-28px，正文 15-16px
- [ ] 中文内容：字体含中文字族，行高 ≥ 1.7，字距 0.02em

## 视觉系统

- [ ] 所有颜色通过 CSS 变量
- [ ] 图标使用项目库 / lucide-react / 内联 SVG；**Playful Creative 调性允许 Emoji 装饰**，其余调性禁用
- [ ] 用户素材已做适配处理；不匹配时已提醒
- [ ] 图片占位：参考站 URL / Unsplash，禁止纯色块

## 交互

- [ ] 每个可交互元素有 hover + focus 状态
- [ ] 入场动画已实现（至少 L1 级 fadeIn）
- [ ] L2+ 滚动行为已实现（reveal / 视差 / 导航变化）
- [ ] L3 特效已实现（pin / 光标 / 转场）
- [ ] L2+ 包含 prefers-reduced-motion 降级

## 响应式

- [ ] 至少适配移动端（< 600px）和桌面端
- [ ] 导航在移动端有折叠方案
- [ ] 图片和容器不溢出
