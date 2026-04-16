# 文字装饰判断规则

代码生成前，对每个文本层级运行以下判断，决定是否添加装饰样式。

## 渐变文字（gradient text）

**触发条件**（满足全部）：
- 风格 == "暗黑科技" 或 "活泼创意"
- 字号 >= 60px 或该元素是 Hero 主标题 h1

**实现**：
```css
background: linear-gradient(135deg, [主色], [强调色]);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

**禁止**：
- 极简克制风格（破坏克制感）
- 白色背景 + 字号 < 40px（可读性差）
- 正文段落 p（仅标题可用）

## 文字投影（text-shadow）

**A. 暗色背景 (bg 亮度 < 30%) + 字号 >= 80px** → subtle glow：
```css
text-shadow: 0 0 40px rgba([主色-RGB], 0.4);
```

**B. 活泼创意 + Hero 主标题** → layered drop shadow：
```css
text-shadow: 3px 3px 0 [强调色], 6px 6px 0 rgba(0,0,0,0.15);
```

**C. 温暖商务 + 衬线标题 + 深色文字** → soft shadow：
```css
text-shadow: 0 2px 8px rgba(0,0,0,0.12);
```

**禁止**：
- 极简克制风格
- 已使用渐变文字时不叠加（视觉过载）
- 正文段落 p

## 装饰性下划线 / 高亮

- Section 小标题（11~13px，letter-spacing > 3px）→ `border-bottom: 2px solid [主色]` 或 background highlight
- 链接文字 hover → underline offset 或 color transition，不加 text-shadow

## 决策表（快速参考）

| 场景 | 极简克制 | 暗黑科技 | 温暖商务 | 活泼创意 |
|------|---------|---------|---------|---------|
| Hero h1 渐变 | -- | Yes | -- | Yes |
| Hero h1 投影 | -- | glow | soft | layered |
| Section h2 渐变 | -- | 可选 | -- | Yes |
| Section h2 投影 | -- | -- | soft | 可选 |
| 正文 p 任何装饰 | -- | -- | -- | -- |
