# DESIGN.md Template

Phase B 输出 DESIGN.md 时按此模板生成。9 个标准章节，每个都必须有实质内容。

---

## 模板

```markdown
# DESIGN.md

> {{一句话设计宣言}}

## 1. Visual Theme & Atmosphere

**Style**: {{风格名称}}
**Keywords**: {{5-8 个设计关键词}}
**Tone**: {{调性描述}} — NOT {{反面关键词}}
**Feel**: {{一句感性描述，用比喻}}

**Interaction Tier**: {{L1 精致静态 / L2 流畅交互 / L3 沉浸体验}}
**Dependencies**: {{CSS only / GSAP + ScrollTrigger / GSAP + ScrollTrigger + Lenis}}

## 2. Color Palette & Roles

```css
:root {
  /* Backgrounds */
  --bg: {{主背景}};                          /* 页面背景 */
  --surface: {{表面}};                       /* 卡片/容器 */
  --surface-alt: {{次级表面}};               /* 交替 section */
  --surface-hover: {{表面 hover}};           /* 悬停态表面 */

  /* Borders */
  --border: {{边框}};                        /* 默认边框 */
  --border-hover: {{边框 hover}};            /* 悬停边框 */

  /* Text */
  --text: {{主文字}};                        /* 标题、重要文字 */
  --text-secondary: {{次文字}};              /* 正文、描述 */
  --text-tertiary: {{三级文字}};             /* 标签、辅助信息 */

  /* Accent */
  --accent: {{主强调色}};                    /* CTA、链接、活跃态 */
  --accent-hover: {{强调色 hover}};

  /* RGB variants for rgba() */
  --bg-rgb: {{r,g,b}};
  --accent-rgb: {{r,g,b}};

  /* Semantic */
  --success: {{成功色}};
  --error: {{错误色}};
  --warning: {{警告色}};
}
```

**Color Rules:**
- {{规则 1，如"所有颜色通过 CSS 变量引用，禁止硬编码 hex"}}
- {{规则 2，如"同一 section 内只用一个强调色"}}
- {{规则 3}}

## 3. Typography Rules

**Font Stack:**
```css
@import url('{{Google Fonts URL}}');
```

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
| Hero H1 | {{font}} | {{size}} | {{weight}} | {{lh}} | {{ls}} |
| Section H2 | {{font}} | {{size}} | {{weight}} | {{lh}} | {{ls}} |
| H3 | {{font}} | {{size}} | {{weight}} | {{lh}} | — |
| Body | {{font}} | {{size}} | {{weight}} | {{lh}} | — |
| Label | {{font}} | {{size}} | {{weight}} | {{lh}} | {{ls}} |
| Mono/Code | {{font}} | {{size}} | {{weight}} | {{lh}} | — |

**Typography Rules:**
- {{规则，如"Heading weight ≥ 700"}}
- **NEVER use**: {{禁止字体列表}}

**Text Decoration:**
- {{按 text-decoration-rules.md 决策表判断后的结果，如"Hero h1: 无渐变、无投影（克制风格）"}}

## 4. Component Stylings

### Buttons
```css
{{完整 CSS，含 default / hover / active / focus / disabled}}
```

### Cards
```css
{{完整 CSS，含 default / hover / focus}}
```

### Navigation
```css
{{完整 CSS，含 scrolled 状态（如有）}}
```

### Links
```css
{{完整 CSS，含 hover 动画}}
```

### Tags / Badges
```css
{{完整 CSS}}
```

### {{其他场景需要的组件}}

## 5. Layout Principles

**Container:**
- Max width: {{width}}
- Padding: {{padding}}
- Narrow variant (text-heavy): {{width}}

**Spacing Scale:**
- Section padding: {{value}}
- Component gap: {{value}}
- Card internal padding: {{value}}

**Grid:**
```css
{{网格 CSS}}
```

## 6. Depth & Elevation

| Level | Treatment | Use |
|-------|-----------|-----|
| Flat | {{无阴影}} | {{场景}} |
| Subtle | {{轻阴影}} | {{场景}} |
| Elevated | {{中阴影}} | {{场景}} |
| {{更多层级}} | | |

## 7. Animation & Interaction

**Motion Philosophy**: {{一句话，如"克制优雅，只用 opacity 和 transform"}}
**Tier**: {{L1/L2/L3}}

### Dependencies
```html
{{CDN 链接（如有）}}
```

### Base Setup
```js
{{GSAP/Lenis 初始化代码（如有）}}
```

### Entrance Animation
```css
{{入场动画 keyframes + 类名}}
```

### Scroll Behavior
```js
{{滚动 reveal / 视差 / pin 代码}}
```

### Hover & Focus States
```css
{{所有可交互元素的 hover/focus 规则}}
```

### Special Effects
{{按需包含：光标跟随 / 页面转场 / 文字 reveal / 视差 / 其他}}

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  {{降级规则}}
}
```

## 8. Do's and Don'ts

### Do
- {{正面规则，至少 5 条}}

### Don't
- {{禁止项，至少 8 条，用 ❌ 前缀}}

## 9. Responsive Behavior

**Breakpoints:**
| Name | Width | Key Changes |
|------|-------|-------------|
| Desktop | > {{bp}} | {{布局}} |
| Tablet | {{bp}}-{{bp}} | {{布局}} |
| Mobile | < {{bp}} | {{布局}} |

**Touch Targets:** minimum {{size}}
**Collapsing Strategy:** {{折叠规则}}

```css
{{响应式 CSS}}
```
```

---

## 生成指导

生成 DESIGN.md 时遵循以下规则：

1. **每个章节都要有实质内容**，不能只写标题占位
2. **所有 CSS 必须可运行**，不是伪代码
3. **组件必须包含所有状态**（default / hover / active / focus / disabled）
4. **Animation 章节不能为空**，至少包含入场和 hover
5. **Do's and Don'ts 是核心章节**——Anti-Patterns 比正面建议更能约束 AI 行为
6. **L2+ 必须包含 Reduced Motion 降级**
7. **颜色全部定义为 CSS 变量**，组件中禁止硬编码 hex
8. **字体必须有 Google Fonts @import URL + fallback**
9. **响应式至少覆盖 Desktop + Mobile**
10. **文件保存为 DESIGN.md 到项目根目录**
