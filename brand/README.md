# AIOS101 视觉基线 · Open Folio / 开卷

**当前基线：v1.0.0 · 已批准 · 2026-10-28 · 出品方：X-lab AI**

维护者认可已上线的课程视觉，并明确要求固化为基线、存入仓库供后续复用。本基线覆盖课程标志、配色、字体、四篇图形和 X-lab 联合署名；不改变课程教材及教学验收状态。

这是 AIOS101 后续网站、教材、课件、任务单、视频与社交传播的视觉起点。资产正本继续放在 `site/assets/`；此目录提供统一规则与版本入口，不另建可独立修改的 Logo 副本。

## 1. 快速取用

| 用途 | 使用文件 |
|---|---|
| 浅色背景的完整课程标志 | [logo-light.svg](../site/assets/course/logo-light.svg) |
| 深色背景的完整课程标志 | [logo-dark.svg](../site/assets/course/logo-dark.svg) |
| 单色印刷或反白 | [logo-black.svg](../site/assets/course/logo-black.svg)、[logo-white.svg](../site/assets/course/logo-white.svg) |
| 独立图形标 | `site/assets/course/mark-{light,dark,black,white}.svg` |
| 小尺寸浏览器图标 | [favicon.svg](../site/assets/course/favicon.svg) |
| 头像与社交封面 | [avatar.svg](../site/assets/course/avatar.svg)、[social-card.svg](../site/assets/course/social-card.svg) |
| 四篇封面 | `site/assets/course/cover-part-1.svg` 至 `cover-part-4.svg` |
| 数字设计参数 | [tokens.json](../site/assets/course/tokens.json)、[tokens.css](tokens.css) |
| X-lab 出品方署名 | [浅色](../site/assets/logo-light.svg)、[深色](../site/assets/logo-dark.svg)；正式页脚可用 `full-logo-*.svg` |
| 可直接打开的组合示例 | [examples/cobrand.html](examples/cobrand.html) |
| 固定版本清单 | [releases/v1.0.0.manifest.json](releases/v1.0.0.manifest.json) |

[下载 v1.0.0 完整资产包](https://www.x-lab.info/AIOS101/assets/course/aios101-identity-kit-v1.0.0.zip) · [在线视觉页](https://www.x-lab.info/AIOS101/#/identity) · [详细视觉规格](https://github.com/X-lab2017/AIOS101/blob/main/specs/course-identity-spec.md)

解压后打开 `brand/examples/cobrand.html` 即可离线查看组合示例。复制资产时同时保留 `site/assets/NOTICE.md`、字体 OFL 和图标 MIT 许可文件。

## 2. 不变的识别规则

- 主标志是 AIOS101 图形标、字标及“AI 开源通识”；X-lab AI 是出品方署名。
- 图形、字体轮廓、比例及规定色值按母版使用；不要重新描摹、加阴影或任意渐变。
- 两枚标志各自保留净空，不合成一个新标志，不改色或移动 X-lab 的 AI 上标。
- 图形标四周净空至少为标志宽度的 1/8，建议不小于 32 px；24 px 及以下使用 favicon。
- 横版课程标志常规宽度至少 220 px；紧凑手机导航允许 168–219 px，须核验辨识度，不能用于正文封面和主标题署名。
- 浅底、深底、单黑和反白按承载面选用对应 SVG；不以 CSS 滤镜反相。
- 联合署名建议课程标志占主位，X-lab 宽度约为课程标志的 40%–65%；需要紧凑排版时上下排列。缩小到无法辨识时，将出品方完整署名放在页脚或尾页。
- `identity-board.svg` 是早期 v0.1 设计评审板，保留作历史过程记录；不列入 v1.0.0 生产资产包。

## 3. 颜色与字体

| 角色 | 色值 | 使用 |
|---|---|---|
| 暖纸白 | `#F6F3EB` | 阅读背景 |
| 深墨蓝 | `#1D2433` | 正文、深色承载面 |
| 开卷靛蓝 | `#5146D9` | 主色与主要操作 |
| 问题珊瑚橙 | `#F27A59` | 问题方块、插图与少量强调 |
| 纸页浅紫 | `#E7E3FC` | 折面与辅助图形 |
| 协作青绿 | `#3F958D` | 共同创造篇的辅助图形 |

小号正文使用语义颜色：浅底文字 `#1D2433`、次要文字 `#656577`、链接 `#4438B7`；深色背景 `#171B27`、文字 `#F5F2ED`、次要文字 `#B7B8CA`、链接 `#C1B5FF`。完整明暗参数见 tokens；装饰色不直接当作正文色。状态同时提供文字或图标。

英文与数字使用 Space Grotesk；中文网页采用系统无衬线字体。固定字标及封面文字已经转为路径，无需安装字体即可显示。正文建议 16 px、行高 1.8–2.1；辅助信息不代替正文。PPT 与印刷资料须按实际投影或成品尺寸核验，不直接照搬网页像素。

## 4. 跨载体复用

| 载体 | 复用方式 | 必须保留 |
|---|---|---|
| 网站 | 使用语义 tokens、对应主题 Logo、联合署名示例 | 小屏与键盘可用、出品方署名 |
| 教材封面 | 复用课程字标与所属篇封面图形，可调整版式尺寸 | 课程名、篇章/章号、版本与 X-lab 出品 |
| 课件 | 暖纸底、深墨正文、靛蓝强调；封面和尾页完整署名 | 页码、章节 ID、图表来源；按课堂投影校验字号 |
| 活动任务单 | 简化标志，保留黑白可读版本 | 活动 ID、任务标题、来源和修订信息 |
| 视频/社交 | 头像或 social-card 作起点，按画幅重新排版 | 不裁切标志、字幕安全区、X-lab 署名 |

四篇分别使用“打开、拆解、对齐、汇合”的图形动作，对应“认识开源、理解 AI、探究证据、共同创造”。这些图形是结构示意，不能用于冒充实测数据。

## 5. 文件与版本管理

当前基线指针在 [baseline.json](baseline.json)。每个版本包含一份不可覆盖的清单和版本命名的 ZIP；清单记录生产资产的 SHA-256、字节数、压缩包路径和采用来源。

```bash
# 校验当前资产、固定清单与资产包
python scripts/package_course_brand.py --check

# 创建新版本时：先更新规格、baseline.json 与 tokens 的版本及版本路径，再生成新清单及资产包
python scripts/package_course_brand.py --build
```

同版本内容不同会拒绝重打包。历史 ZIP 和清单保留，引用长期材料时使用固定版本；`main` 表示当前维护状态。视觉改动与网站、教材版本分开编号。

- 修正说明或打包错误：补丁版本，例如 1.0.1。
- 增加兼容模板或辅助资产：次版本，例如 1.1.0。
- 修改 Logo 轮廓、主色、品牌层级或核心字体：主版本，经维护者确认后发布。
- 日常生产只取用既有 SVG；需要重建轮廓时运行 `scripts/generate_course_brand.py`，采用原规格固定的字体来源，核验差异后再建立新基线。

每份派生交付物记录“AIOS101 Visual Baseline v1.0.0”、使用日期、是否调整版式及源文件路径。后续新设计优先扩展模板，不覆盖母版。

## 6. 来源和使用范围

本次授权明确覆盖 AIOS101 课程及其配套资源的复用。它不自动授予第三方将课程或 X-lab 标志用于其他品牌、商品或背书的权利；统一对外授权仍由维护者另定。字体与图标分别保留现有许可，详见 [素材说明](../site/assets/NOTICE.md)。

本基线属于已认可的数字视觉方案。印刷打样、CMYK 转换、完整无障碍审计与商标可注册性未验证；这些事项不影响按已核验方式复用网页与数字资产。
