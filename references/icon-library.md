# Lucide-React 图标分类速查表

artifact 环境内置 lucide-react@0.383.0，可直接 `import { IconName } from "lucide-react"` 使用。
所有图标为24x24 SVG，支持 `size`、`color`、`strokeWidth` 属性。

## 导航类
| 用途 | 图标名 | 导入 |
|------|--------|------|
| 菜单 | Menu, AlignJustify | `import { Menu } from "lucide-react"` |
| 关闭 | X, XCircle | `import { X } from "lucide-react"` |
| 返回 | ArrowLeft, ChevronLeft | `import { ArrowLeft } from "lucide-react"` |
| 前进 | ArrowRight, ChevronRight | `import { ArrowRight } from "lucide-react"` |
| 上方 | ArrowUp, ChevronUp | `import { ArrowUp } from "lucide-react"` |
| 下方 | ArrowDown, ChevronDown | `import { ArrowDown } from "lucide-react"` |
| 首页 | Home | `import { Home } from "lucide-react"` |
| 外链 | ExternalLink, ArrowUpRight | `import { ExternalLink } from "lucide-react"` |
| 搜索 | Search | `import { Search } from "lucide-react"` |

## 社交媒体
| 用途 | 图标名 | 导入 |
|------|--------|------|
| GitHub | Github | `import { Github } from "lucide-react"` |
| Twitter/X | Twitter | `import { Twitter } from "lucide-react"` |
| LinkedIn | Linkedin | `import { Linkedin } from "lucide-react"` |
| YouTube | Youtube | `import { Youtube } from "lucide-react"` |
| Instagram | Instagram | `import { Instagram } from "lucide-react"` |
| 邮件 | Mail, MailOpen | `import { Mail } from "lucide-react"` |
| 链接 | Link, Link2 | `import { Link } from "lucide-react"` |
| 分享 | Share2 | `import { Share2 } from "lucide-react"` |

## 内容/文档
| 用途 | 图标名 |
|------|--------|
| 文件 | File, FileText, FilePlus |
| 文件夹 | Folder, FolderOpen |
| 图片 | Image, ImagePlus |
| 视频 | Video, Play, Pause |
| 音频 | Music, Volume2 |
| 下载 | Download |
| 上传 | Upload |
| 复制 | Copy, Clipboard |
| 编辑 | Pencil, PenLine, Edit |
| 删除 | Trash2 |

## 用户/个人
| 用途 | 图标名 |
|------|--------|
| 用户 | User, UserCircle |
| 用户组 | Users |
| 头像 | CircleUser |
| 位置 | MapPin |
| 电话 | Phone |
| 日历 | Calendar |
| 时钟 | Clock |
| 生日 | Cake |

## 技能/技术
| 用途 | 图标名 |
|------|--------|
| 代码 | Code, Code2, Terminal |
| 数据库 | Database |
| 服务器 | Server |
| 云端 | Cloud |
| 设置 | Settings, Cog |
| 工具 | Wrench, Hammer |
| 图层 | Layers |
| 组件 | Component, Puzzle |
| CPU | Cpu |
| 闪电/快速 | Zap |
| 框架 | LayoutGrid, Grid3x3 |
| API | Webhook |
| 安全 | Shield, Lock |

## 状态/反馈
| 用途 | 图标名 |
|------|--------|
| 成功 | Check, CheckCircle |
| 警告 | AlertTriangle |
| 错误 | AlertCircle, XCircle |
| 信息 | Info |
| 加载 | Loader2 (可加animate-spin) |
| 星标 | Star, StarHalf |
| 心形 | Heart |
| 点赞 | ThumbsUp |

## 装饰/布局
| 用途 | 图标名 |
|------|--------|
| 太阳(亮色模式) | Sun |
| 月亮(暗色模式) | Moon |
| 引号 | Quote |
| 火焰 | Flame |
| 火箭 | Rocket |
| 奖杯 | Trophy |
| 目标 | Target |
| 灯泡 | Lightbulb |
| 书本 | BookOpen |
| 毕业帽 | GraduationCap |
| 公文包 | Briefcase |
| 建筑 | Building |

## 使用示例

```jsx
import { Github, Mail, ArrowUpRight, Moon, Sun } from "lucide-react";

// 基本用法
<Github size={20} />

// 自定义颜色和描边
<Mail size={24} color="var(--color-primary)" strokeWidth={1.5} />

// 配合按钮
<button className="flex items-center gap-2">
  <ArrowUpRight size={16} />
  View Project
</button>

// 主题切换图标
{isDark ? <Sun size={20} /> : <Moon size={20} />}
```

## 注意事项

1. 始终从 lucide-react 导入，不要用 `<svg>` 手写或 Emoji 替代
2. 社交图标如果 lucide 没有（如微信、微博），使用 SVG 内联：在 `references/` 目录下无预置，需代码中手写简化SVG path
3. `size` 属性接受 number（px），常用值：16（小按钮内）、20（普通）、24（标准）、32（大图标）、48（装饰）
4. `strokeWidth` 默认 2，细线设 1.5，粗线设 2.5
5. `className` 可传入 Tailwind 类，如 `className="animate-spin"` 做旋转加载
