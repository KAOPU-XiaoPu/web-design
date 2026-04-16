# Style Seeds

关键词 → 初始 Token 映射。Round 2 中用于快速匹配用户风格方向。

每个种子提供：色板、字体组合、圆角/阴影基调、推荐动效档位。用户确认后再细化为完整 Token。

---

## 1. 奶油编辑 (Cream Editorial)

**关键词**：温暖、编辑感、杂志、克制、纸质感
**气质**：像一本排版精良的杂志在屏幕上展开

```
色板:
  背景 #ECE7DE (暖奶油)    表面 #FFFFFF
  边框 #D5D0C7 (暖灰)      强边框 #2A2A2A
  文字 #1A1A1A / #6B6560    强调 #E8682A (橙)
字体:
  heading: Playfair Display (serif, 900)
  body: DM Sans (sans, 400-700)
  mono: JetBrains Mono
圆角: 16px    阴影: 仅 hover    档位: L1
```

---

## 2. 暗黑科技 (Dark Tech)

**关键词**：深邃、霓虹、未来、科技、赛博
**气质**：深空站控制台，信息在黑暗中发光

```
色板:
  背景 #0B0B0F             表面 rgba(255,255,255,0.03)
  边框 rgba(255,255,255,0.08)
  文字 #F0F0F0 / #8B8B8B    主色 #00D4FF    辅色 #8B5CF6
字体:
  heading: Space Grotesk (sans, 700)
  body: Inter (sans, 400-600)
  mono: Fira Code
圆角: 12px    阴影: glow    档位: L2-L3
特殊: Glassmorphism, 渐变流动背景
```

---

## 3. 极简克制 (Minimal Pure)

**关键词**：干净、留白、精确、安静、高级
**气质**：美术馆白墙上的一行字

```
色板:
  背景 #FAFAFA             表面 #FFFFFF
  边框 #E8E8E8
  文字 #1A1A1A / #666666    强调 #0066FF (仅链接)
字体:
  heading: Instrument Serif (serif, 400)
  body: DM Sans (sans, 400-500)
圆角: 8px    阴影: 极轻    档位: L1
特殊: 大字号对比建立层次，禁止装饰
```

---

## 4. 温暖商务 (Warm Professional)

**关键词**：专业、信任、圆润、友好、成熟
**气质**：一家让人放心的公司

```
色板:
  背景 #FFFFFF             表面 #F8FAFC
  边框 #E2E8F0
  文字 #1E293B / #475569    主色 #2563EB    辅色 #F59E0B
字体:
  heading: Plus Jakarta Sans (sans, 700-800)
  body: Plus Jakarta Sans (sans, 400-500)
圆角: 12px    阴影: 柔和层叠    档位: L1-L2
```

---

## 5. 活泼创意 (Playful Creative)

**关键词**：大胆、有趣、年轻、跳跃、手写
**气质**：设计师朋友的生日派对邀请

```
色板:
  背景 #FFF8F0             表面 #FFFFFF
  边框 #FFE0CC
  文字 #2D2D2D / #666666    主色 #FF3366    辅色 #FFD700    三色 #00CC88
字体:
  heading: Sora (sans, 700-800)
  body: Nunito (sans, 400-600)
  accent: Caveat (cursive, 手写装饰)
圆角: 16-24px (偏大)    阴影: 带色    档位: L2-L3
特殊: blob 装饰, 手写注释, 弹性动画
```

---

## 6. 中文优雅 (Chinese Elegant)

**关键词**：文墨、东方、内敛、书卷气、留白
**气质**：一封用宣纸写的信

```
色板:
  背景 #FAF8F5             表面 #FFFFFF
  边框 #E8E0D8
  文字 #2C2C2C / #5C5C5C    主色 #C45C3C (赭石)    辅色 #2C5F6E
字体:
  heading: Noto Serif SC (宋体, 700)
  body: Noto Sans SC (黑体, 400-500)
  accent: LXGW WenKai (楷体, 装饰)
圆角: 4px (极小)    阴影: 极轻    档位: L1
特殊: 行高1.8+, 字距0.02em, 容器800px, 首行缩进2em
```

---

## 7. 赛博朋克 (Cyberpunk)

**关键词**：故障、网格、刺眼、地下、数据流
**气质**：黑客终端里跑着的霓虹数据

```
色板:
  背景 #0A0A0A             表面 #111111
  边框 #222222
  文字 #00FF41 / #888888    主色 #FF0080    辅色 #00FFFF
字体:
  heading: Orbitron (sans, 700-900)
  body: IBM Plex Mono (mono, 400)
圆角: 0px (全直角)    阴影: 霓虹 glow    档位: L3
特殊: glitch 效果, scanline, 数据流动画, 打字机
```

---

## 8. 自然有机 (Organic Natural)

**关键词**：泥土、手作、柔和、呼吸、可持续
**气质**：乡间集市上的手工肥皂包装

```
色板:
  背景 #F5F0EB             表面 #FEFCF9
  边框 #DDD5CA
  文字 #3D3228 / #7A6E60    主色 #5B8C5A (苔绿)    辅色 #C4956A (陶土)
字体:
  heading: Fraunces (serif, 600-700, optical size)
  body: Source Sans 3 (sans, 400-500)
圆角: 20px+ (偏圆)    阴影: 暖色极柔    档位: L1-L2
特殊: 手绘纹理背景, 不规则边缘, 柔和渐变
```

---

## 9. 瑞士设计 (Swiss Grid)

**关键词**：网格、规则、理性、黑白、红色
**气质**：包豪斯学校走廊的海报

```
色板:
  背景 #FFFFFF             表面 #F5F5F5
  边框 #000000 (实线)
  文字 #000000 / #555555    强调 #FF0000 (仅点缀)
字体:
  heading: Helvetica Neue / Inter (sans, 700)
  body: Helvetica Neue / Inter (sans, 400)
圆角: 0px    阴影: 无    档位: L1
特殊: 严格网格, 粗体规则, 大量负空间, 不对称构图
```

---

## 10. 玻璃拟态 (Glassmorphism)

**关键词**：透明、模糊、光影、层叠、梦幻
**气质**：阳光穿过磨砂玻璃落在桌面上

```
色板:
  背景 线性渐变 #667eea → #764ba2
  表面 rgba(255,255,255,0.15)
  边框 rgba(255,255,255,0.2)
  文字 #FFFFFF / rgba(255,255,255,0.7)
字体:
  heading: Outfit (sans, 600-700)
  body: Inter (sans, 400-500)
圆角: 16px    阴影: 大面积柔光    档位: L2
特殊: backdrop-filter: blur(12px), 半透明层叠, 光效动画
```

---

## 种子混搭规则

用户经常不会完全匹配某一个种子。常见混搭：

- "暗黑但克制" → 暗黑科技的色板 + 极简克制的动效档位和装饰规则
- "温暖但有趣" → 温暖商务的色调 + 活泼创意的圆角和动画
- "中文 + 科技感" → 中文优雅的字体 + 暗黑科技的色板
- "瑞士但现代" → 瑞士设计的网格和黑白 + 更大圆角 + L2 动效

混搭时以**色板和字体**从一个种子取，**动效和装饰规则**从另一个取。不要混搭两套色板。
