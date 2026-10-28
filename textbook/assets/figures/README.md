# AIOS101 教材图版

**当前交付请使用[统一图号与图题索引](INDEX.md)**。它从正文与清单生成，含当前文件、插入位置及退出正文的历史图号。本文件以下为历次素材制作与发布记录，历史题名和数量不作为当前交付清单。

## 首批图版与历史位置

前三章初版正文依据：AIOS101 提交 `4b4c76f43013ac889d6d06f88ce83cabafae97c3`。以正文图号为准；旧资产索引曾有编号错位。

| 教材图号 | 文件 | 插入位置 | 来源类型 |
|---|---|---|---|
| 图 1-1 | [AIOS101_Fig-01-01_learning-positions_v01.webp](AIOS101_Fig-01-01_learning-positions_v01.webp) | 第一章／一／1 | Mermaid |
| 图 1-2 | [AIOS101_Fig-01-02_open-source-history_v02.webp](AIOS101_Fig-01-02_open-source-history_v02.webp) | 第一章／三／3 后 | Mermaid |
| 图 1-3 | [AIOS101_Fig-01-03_ai-open-materials_v01.webp](AIOS101_Fig-01-03_ai-open-materials_v01.webp) | 第一章／四／1 | Mermaid |
| 图 1-4 | [AIOS101_Fig-01-04_deepseek-readme_v01.webp](AIOS101_Fig-01-04_deepseek-readme_v01.webp) | 第一章／四／2 | 真实材料组合 |
| 图 2-1 | [AIOS101_Fig-02-01_open-source-mechanism_v01.webp](AIOS101_Fig-02-01_open-source-mechanism_v01.webp) | 第二章／一 | Mermaid |
| 图 2-2 | [AIOS101_Fig-02-02_issue-pr-workflow_v01.webp](AIOS101_Fig-02-02_issue-pr-workflow_v01.webp) | 第二章／四／3 | Mermaid |
| 图 2-3 | [AIOS101_Fig-02-03_aiinfra-evidence_v01.webp](AIOS101_Fig-02-03_aiinfra-evidence_v01.webp) | 第二章／五／2 | 真实材料组合 |
| 图 2-4 | [AIOS101_Fig-02-04_public-value-evidence_v01.webp](AIOS101_Fig-02-04_public-value-evidence_v01.webp) | 第二章／六 | Mermaid |
| 图 3-1 | [AIOS101_Fig-03-01_ecosystem-dimensions_v01.webp](AIOS101_Fig-03-01_ecosystem-dimensions_v01.webp) | 第三章／一 | Mermaid |
| 图 3-2 | [AIOS101_Fig-03-02_agent-infra-landscape_v01.webp](AIOS101_Fig-03-02_agent-infra-landscape_v01.webp) | 第三章／二／2 | GOSD 图 4-1-1 |
| 图 3-3 | [AIOS101_Fig-03-03_model-infra-landscape_v01.webp](AIOS101_Fig-03-03_model-infra-landscape_v01.webp) | 第三章／二／2 | GOSD 图 4-1-2 |
| 图 3-4 | [AIOS101_Fig-03-04_ecosystem-relations_v01.webp](AIOS101_Fig-03-04_ecosystem-relations_v01.webp) | 第三章／四 | Mermaid |
| 图 3-5 | [AIOS101_Fig-03-05_deepseek-asset-relations_v01.webp](AIOS101_Fig-03-05_deepseek-asset-relations_v01.webp) | 第三章／六 | Mermaid |
| 图 3-6 | [AIOS101_Fig-03-06_model-task-landscape_v01.webp](AIOS101_Fig-03-06_model-task-landscape_v01.webp) | 第三章／七／1 | GOSD 图 4-2-1 |
| 图 3-7 | [AIOS101_Fig-03-07_pytorch-ecosystem_v01.webp](AIOS101_Fig-03-07_pytorch-ecosystem_v01.webp) | 第三章／七／1 | GOSD 图 4-6-1 |
| 图 3-8 | [AIOS101_Fig-03-08_opendipper-open-galaxy_v01.webp](AIOS101_Fig-03-08_opendipper-open-galaxy_v01.webp) | 第三章／七／2 | 真实界面 |

## 在线图版与维护

本目录的 CH01—CH03 部分包含 16 张 WebP。保留原始像素尺寸，以有损 WebP 压缩；原 PNG 共 28,117,889 字节，WebP 共 6,143,498 字节，减少 78.2%。单图最大约 515 KiB。尺寸、字节数和章节位置见 manifest.json。

完整出版交付包另行保留，不将大型 PNG 和截图原件重复加入仓库。需要放大阅读的图另存轻量 SVG；其中的项目图标可能是压缩位图，图中文字与结构仍为矢量。9 份 Mermaid 源码保留在 mermaid/，正文通过折叠区保留相同源码及文字关系回退。修改结构时同步修改正文和对应 .mmd，并重新核对成图。

已获维护者授权上传本仓库及 Pages 公开评审。此授权用于本轮课程图文预览，不表示第三方素材获得新的通用许可或正式出版清权。图 1-2 为原创人物插画，肖像参考、署名与未决条件见 [portrait-sources.md](portrait-sources.md)；原照片不随仓库分发。其余第三方截图和项目标识保留原有权利。本目录不覆盖它们的许可。

## 来源与边界

- DeepSeek: https://github.com/deepseek-ai/DeepSeek-R1/blob/0cf78561f1d51c84a21b2190626b21116d5c68bb/README.md 。固定 README 不冻结外部模型文件。
- AIInfra: https://github.com/Infrasys-AI/AIInfra/issues/386 与 https://github.com/Infrasys-AI/AIInfra/pull/364/files 。两条独立记录，不是同一修复链。
- GOSD: https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/04/ 。原图 4-1-1、4-1-2、4-2-1、4-6-1 分别对应教材图 3-2、3-3、3-6、3-7；分类不是依赖，下载量不是能力排名。保留原布局与项目标识，离线字体改为 Noto Sans CJK SC，增加教材图题和来源。
- OpenDipper: https://www.x-lab.info/open-dipper/ 。截图 2026-10-28，模型数据日期 2026-08-05，当前界面不冒充正文引用的旧提交版本。

六幅概念插画采用 AI 辅助绘制，三幅精确关系图采用矢量排版，七幅证据图组合真实截图或报告原图。所有截图仅裁切、编排及压缩，不重写其中事实。

## 第四至第六章：28 幅新图

正文基线：`3965a64c939e945f5245184e3e5bcc51bcb823ca`；第四章 9 幅、第五章 9 幅、第六章 10 幅。2026-10-28 初版网页图共 3,225,708 字节；相对本轮 PNG 导出 21,436,738 字节减少 85.0%。图像宽 1600 像素，正文显示宽度 700—780px、保持自然比例，点击可查看完整图。

22 份可编辑矢量图位于 vector/，对应 Mermaid 在 mermaid/；FineWeb 原始 Figure 9 矢量图也保留。密集截图和高分辨率 PNG 不重复入库。完整来源、固定版本、许可与变更说明见 [本轮来源记录](ch04-ch06-sources.md)。

| 图号 | 图题 | 在线图 | 矢量源 |
|---|---|---|---|
| 4-1 | 模型形成的基本要素 | [WebP](AIOS101_Fig-04-01_v02.webp) | [SVG](vector/AIOS101_Fig-04-01_v02.svg) |
| 4-2 | FineWeb 论文报告的主要数据处理链 | [WebP](AIOS101_Fig-04-02_v01.webp) | [SVG](vector/AIOS101_Fig-04-02_v01.svg) |
| 4-3 | FineWeb 论文 v2 图 9 原图 | [WebP](AIOS101_Fig-04-03_v01.webp) | 真实材料组合 |
| 4-4 | 分词、下一 token 候选分布与训练目标 | [WebP](AIOS101_Fig-04-04_v01.webp) | [SVG](vector/AIOS101_Fig-04-04_v01.svg) |
| 4-5 | 一次训练迭代的基本循环 | [WebP](AIOS101_Fig-04-05_v01.webp) | [SVG](vector/AIOS101_Fig-04-05_v01.svg) |
| 4-6 | 批次、迭代、训练轮次与检查点 | [WebP](AIOS101_Fig-04-06_v02.webp) | [SVG](vector/AIOS101_Fig-04-06_v02.svg) |
| 4-7 | DeepSeek-R1 固定 README 公开的形成路径 | [WebP](AIOS101_Fig-04-07_v01.webp) | [SVG](vector/AIOS101_Fig-04-07_v01.svg) |
| 4-8 | DeepSeek-R1 形成路径的原始证据 | [WebP](AIOS101_Fig-04-08_v01.webp) | 真实材料组合 |
| 4-9 | 训练、验证、测试及近重复泄漏的边界 | [WebP](AIOS101_Fig-04-09_v01.webp) | [SVG](vector/AIOS101_Fig-04-09_v01.svg) |
| 5-1 | 上下文容量与最大生成长度 | [WebP](AIOS101_Fig-05-01_v01.webp) | [SVG](vector/AIOS101_Fig-05-01_v01.svg) |
| 5-2 | 语言模型推理的最小生成循环 | [WebP](AIOS101_Fig-05-02_v01.webp) | [SVG](vector/AIOS101_Fig-05-02_v01.svg) |
| 5-3 | 生成 top-k 与 top-p 的简化对照 | [WebP](AIOS101_Fig-05-03_v02.webp) | [SVG](vector/AIOS101_Fig-05-03_v02.svg) |
| 5-4 | 从候选分布到输出结束的主要生成条件 | [WebP](AIOS101_Fig-05-04_v01.webp) | [SVG](vector/AIOS101_Fig-05-04_v01.svg) |
| 5-5 | DeepSeek-R1 的生成与测试建议 | [WebP](AIOS101_Fig-05-05_v01.webp) | 真实材料组合 |
| 5-6 | 模型推理的系统分层 | [WebP](AIOS101_Fig-05-06_v02.webp) | [SVG](vector/AIOS101_Fig-05-06_v02.svg) |
| 5-7 | 单个请求的延迟与整个服务的吞吐 | [WebP](AIOS101_Fig-05-07_v01.webp) | [SVG](vector/AIOS101_Fig-05-07_v01.svg) |
| 5-8 | 最小评价的证据链 | [WebP](AIOS101_Fig-05-08_v02.webp) | [SVG](vector/AIOS101_Fig-05-08_v02.svg) |
| 5-9 | DeepSeek-R1 的评测设置与主评测表 | [WebP](AIOS101_Fig-05-09_v02.webp) | 真实材料组合 |
| 6-1 | 从模型到任务系统的基本组成 | [WebP](AIOS101_Fig-06-01_v02.webp) | [SVG](vector/AIOS101_Fig-06-01_v02.svg) |
| 6-2 | 长文档切分、元数据与检索 | [WebP](AIOS101_Fig-06-02_v01.webp) | [SVG](vector/AIOS101_Fig-06-02_v01.svg) |
| 6-3 | 查询与文档片段的语义近邻 | [WebP](AIOS101_Fig-06-03_v02.webp) | [SVG](vector/AIOS101_Fig-06-03_v02.svg) |
| 6-4 | 检索增强生成的基本流程 | [WebP](AIOS101_Fig-06-04_v01.webp) | [SVG](vector/AIOS101_Fig-06-04_v01.svg) |
| 6-5 | 工具调用的最小闭环 | [WebP](AIOS101_Fig-06-05_v01.webp) | [SVG](vector/AIOS101_Fig-06-05_v01.svg) |
| 6-6 | 一次工具调用的消息与执行角色 | [WebP](AIOS101_Fig-06-06_v02.webp) | [SVG](vector/AIOS101_Fig-06-06_v02.svg) |
| 6-7 | 智能体的基本任务循环 | [WebP](AIOS101_Fig-06-07_v02.webp) | [SVG](vector/AIOS101_Fig-06-07_v02.svg) |
| 6-8 | 新生导览模拟轨迹的角色与时序 | [WebP](AIOS101_Fig-06-08_v01.webp) | [SVG](vector/AIOS101_Fig-06-08_v01.svg) |
| 6-9 | MCP 2025-06-18 工具规范与安全原则局部截图 | [WebP](AIOS101_Fig-06-09_v01.webp) | 真实材料组合 |
| 6-10 | 人机协作中的关键检查点 | [WebP](AIOS101_Fig-06-10_v02.webp) | [SVG](vector/AIOS101_Fig-06-10_v02.svg) |

## 前六章图文精审（2026-10-29）

当前图号、版本、图题、替代文本、显示宽度和来源以 [manifest.json](manifest.json) 为准。11 幅图版修订，另复用第三章 2 份轻量关系图矢量源；大图页支持原尺寸和两倍查看。旧版矢量保留用于重现修订过程，线上仅选取清单中的当前版本。详见[评审记录](https://github.com/X-lab2017/AIOS101/blob/main/docs/first-six-review-2026-10-29.md)。

同日续办：图 3-2、3-3、3-6、3-7 补齐轻量矢量大图，矢量查看总数由 25 增至 29。四图合计从 2,572,775 字节减至 886,013 字节（减少 65.6%），正文 WebP 保持不变。压缩合并重复样式，并将部分图标转为最多原显示尺寸四倍的 WebP；文字、分组、数值与几何属性逐项核对保持一致。原图采样与导出日期、第三方标识权利不变。

复现脚本：`scripts/figures/optimize_gosd.py`（仓库根目录运行）；原始导出的文件名、SHA-256 与体积记录见 [gosd-vector-optimization.json](sources/gosd-vector-optimization.json)。
