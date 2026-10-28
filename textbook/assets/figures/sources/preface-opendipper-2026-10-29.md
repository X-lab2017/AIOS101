# 序言 OpenDipper 双图来源与制作记录

日期：2026-10-29。维护者提供两张 OpenDipper 截图，明确授权在本课程中加工、入文、提交仓库并发布 Pages 供评审。

| 图号 | 图题 | 输入附件 | 保留的原图 |
|---|---|---|---|
| 0-4 | OpenDipper 全球观测：从分布追问口径 | image(20261028-230617).png | [无损 WebP](OpenDipper_global_user-snapshot_2026-10-29.webp) |
| 0-5 | OpenDipper 开源星系：从连线追问证据 | image(20261028-230625).png | [无损 WebP](OpenDipper_galaxy_user-snapshot_2026-10-29.webp) |

附件提供日期为 2026-10-29，不据文件名推断精确捕获时刻、应用版本或所有数据的观察期。图 0-4 原图为 2048 × 1280，图 0-5 原图为 2048 × 1272。原始 PNG 的 SHA-256、无损 WebP 的 SHA-256 与文件体积见[制作清单](preface-opendipper-manifest.json)。两份 WebP 解码后 RGB 像素与所供 PNG 完全一致。

## 核验依据

阅读 OpenDipper 固定提交 `dcfcb8367ed8d883613e854cc36cd3c718e94df5` 的以下材料：

- [项目 README](https://github.com/X-lab2017/open-dipper/blob/dcfcb8367ed8d883613e854cc36cd3c718e94df5/README.md)：全球观测、开源星系及各自范围；实际读取 main 后核对同一提交。
- [Open Galaxy 契约](https://github.com/X-lab2017/open-dipper/blob/dcfcb8367ed8d883613e854cc36cd3c718e94df5/docs/OPEN_GALAXY.md)：代码侧为选定仓库及共同贡献者关联，模型侧包含模型、数据集及 Space；两网分别归一化；记录关系与推断关系区分；几何位置与边强度不是通用质量得分。
- [数据证据说明](https://github.com/X-lab2017/open-dipper/blob/dcfcb8367ed8d883613e854cc36cd3c718e94df5/docs/DATA_EVIDENCE.md)：不同指标拥有独立观察期与覆盖范围，缺失不是零；地图显示遵循原项目规则。

本轮只核对界面含义和阅读边界，没有重新采集、独立复算截图数值，没有验证每个模型名称、每条连线或源数据记录。第一幅包含“模拟”标记，已原样保留并在正文提醒；第二幅节点名称、位置、图例与关系全部来自原截图。

## 加工方式

内置 image_gen 仅生成外围纸张、铅笔线框、胶带、圆规或放大镜装帧，不生成地图、数据、节点或关系。两种装帧分别采用观测手册和星图档案的轻量隐喻。提示词保存在[绘图记录](preface-opendipper-prompts.json)。

图题与三个读图步骤由 `scripts/figures/preface_opendipper.py` 以确定的矢量文字排版；完整原截图按原始宽高比置入，未裁剪或遮盖内容。正文图以 WebP quality 92 发布（分别约 317 KiB、355 KiB）；放大页使用嵌入无损截图的独立 SVG，并可直接查看原始截图。两幅图均使用“图 0-4／图 0-5”的规范编号，未复用已退休的 0-1、0-2。

授权基于本轮维护者的明确课程复用指令，不改变 OpenDipper 或其地图、数据与品牌的通用许可。未声明第三方可任意再分发或正式出版清权已完成。
