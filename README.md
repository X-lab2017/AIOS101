# AIOS101 · AI 开源通识

X-lab 出品，面向所有学科大学生的 AI 与开源通识课程。以 AI 为学习对象，以开源为认识论、方法论和实践方式，沿“使用—理解—探究—贡献—创造”展开。

**[在线阅读](https://www.x-lab.info/AIOS101/) · [教材目录](textbook/README.md) · [当前状态与交接](docs/STATUS.md) · [参与建设](CONTRIBUTING.md)**

序言、前六章与附录 A 已形成公开的自学图文评审版。后六章仍按四篇十二章蓝图建设；公开阅读与工程检查通过，不等于整门课程已通过教学或出版验收。

## 新协作者从这里开始

1. 阅读[课程宪法](CONSTITUTION.md)、[规格体系](specs/README.md)和[课程总规格](specs/course-spec.md)，理解课程定位与学习成果。
2. 查看[当前状态](docs/STATUS.md)与[关键决策](docs/decisions/ADR-0001-reading-and-evidence-baseline.md)，确认当前版本、未决事项及已暂停功能。
3. 按[内容迭代指南](docs/content-iteration-guide.md)找到唯一正本，修改相关规格、教材或图版。
4. 运行统一检查，记录验证范围，再按已有授权提交或发起 PR；AI 协作者还须遵守 [AGENTS.md](AGENTS.md)。

```bash
python scripts/check_all.py
```

常规检查使用 Python 与 Node.js，无第三方构建依赖。图版再生成与 PDF 排版需要的额外环境见[脚本说明](scripts/README.md)。

## 正本与目录

| 入口 | 职责 |
|---|---|
| [CONSTITUTION.md](CONSTITUTION.md) | 课程最高基线 |
| [specs/](specs/README.md) | 课程、章节、活动、证据、展现和验收规范 |
| [textbook/](textbook/README.md) | 序言、章节和附录的唯一正文 |
| [textbook/assets/figures/](textbook/assets/figures/README.md) | 当前图版清单、统一图号、矢量源、截图来源和保留的历史图号 |
| [brand/](brand/CURRENT.md) | 已批准的 Open Folio v1.0.0 品牌与 X-lab 联合署名 |
| [site/](site/README.md) | 当前图文阅读网站源码，构建结果不手改 |
| [activities/](activities/README.md) | 活动规格与学生、教师材料，独立于正文阅读 |
| [interactive/](interactive/README.md) | 暂停上线的交互需求和兼容性材料 |
| [slides/](slides/README.md) | 独立授课评审稿，尚未与最新图文逐页对齐 |
| [docs/](docs/README.md) | 当前状态、维护指南、决策和历史验收证据 |
| [deliverables/](deliverables/README.md) | 导出约定，不保留容易被误认为最新版的过时二进制 |

## 阅读与视觉基线

当前网站聚焦完整正文、目录、字号、主题、章节导航和图片放大。已撤下已读标记、页边手账、想法按钮、工坊与活动表单；后续有明确学习需要时再设计。界面提供中英切换，教材尚无审定英文译本。

插图采用有明确教学用途的科技出版插画：概念可用手绘隐喻，精确数字与关系用可校验排版，真实证据保持原始材料。图号、图题与插入位置以[当前图版索引](textbook/assets/figures/INDEX.md)为准。视觉资产从[品牌基线](brand/CURRENT.md)复用。

[更新日志](CHANGELOG.md)记录重要变化；[历史记录索引](docs/history/README.md)保留过去轮次的决定、发布证据与恢复入口，不作为当前功能清单。
