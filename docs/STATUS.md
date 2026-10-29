# 当前状态与协作交接

更新日期：2026-10-29。维护者：Will（王伟）。本页是仓库现状与后续接手入口；教学方向以[课程宪法](../CONSTITUTION.md)为准。

## 当前可用范围

- [Pages](https://www.x-lab.info/AIOS101/)：序言、CH01—CH06、附录 A 与关于本教材可完整阅读，处于自学图文评审阶段。
- 四篇十二章蓝图完整；CH07—CH12 正文尚未进入主分支。
- 当前公开体验为安静阅读：正文、目录、检索、字号、深浅主题、图片放大与固定版本来源。旧工坊、手账和活动路由回退到目录或对应正文。
- Open Folio / VIS-AIOS101 v1.0.0 是已批准的数字视觉基线。教材版本独立于品牌版本；英文界面不等于已有英文教材。

<!-- BEGIN GENERATED BASELINE -->

## 正本版本与图版（自动核对）

| 单元 | 正文版本 | 当前图数 | 唯一正本 |
|---|---|---|---|
| PREFACE | v0.7 | 3 | [preface.md](../textbook/preface.md) |
| CH01 | v0.8 | 4 | [CH01-why-ai-open-source-literacy.md](../textbook/chapters/CH01-why-ai-open-source-literacy.md) |
| CH02 | v0.8 | 4 | [CH02-open-source-mechanisms.md](../textbook/chapters/CH02-open-source-mechanisms.md) |
| CH03 | v0.5 | 8 | [CH03-ai-open-source-ecosystem.md](../textbook/chapters/CH03-ai-open-source-ecosystem.md) |
| CH04 | v0.5 | 8 | [CH04-data-to-models.md](../textbook/chapters/CH04-data-to-models.md) |
| CH05 | v0.6 | 8 | [CH05-training-to-inference.md](../textbook/chapters/CH05-training-to-inference.md) |
| CH06 | v0.5 | 9 | [CH06-model-to-agents.md](../textbook/chapters/CH06-model-to-agents.md) |
| APP-A | v0.2 | 0 | [APP-A-repository-snapshots.md](../textbook/appendices/APP-A-repository-snapshots.md) |
| ABOUT | v0.1 | 0 | [about.md](../textbook/about.md) |

合计 **9 个阅读单元、44 幅正文图、29 幅 SVG 放大版、30 份折叠 Mermaid 源码**。

<!-- END GENERATED BASELINE -->

以上表格由 `python scripts/sync_status.py --write` 从正本和图版清单生成；CI 检查它是否过时。图号与图题完整列表见[图版索引](../textbook/assets/figures/INDEX.md)。

本轮在线阅读路径与关于页的范围、验证和发布证据见[阅读体验记录](reading-path-review-2026-10-29.md)。

## 最近已核验的内容发布

- 序言 OpenDipper 双图及字号修正：提交 [`b17a9b8`](https://github.com/X-lab2017/AIOS101/commit/b17a9b8ecfb973d53c970a55e93c1341f568e60b)，[Pages #49](https://github.com/X-lab2017/AIOS101/actions/runs/40787715014) 成功。
- 两张真实截图保留原始像素，手绘处理用于外围装帧；正文提供导读、图注与原图入口。细节见[交付记录](history/preface-opendipper-review-2026-10-29.md)。
- 本轮材料整理及发布证据见[维护记录](repository-maintenance-2026-10-29.md)。后续提交的实际部署结果以 [Actions](https://github.com/X-lab2017/AIOS101/actions/workflows/course-pages.yml) 为准，不能把这里列举的成功运行当作所有后续提交的证明。

## 尚待推进的工作

| 工作 | 当前事实与完成条件 |
|---|---|
| 前半本内容与图文评审 | 编辑和工程检查已执行，等待维护者反馈；真人自学、实体设备、完整无障碍和印刷打样尚未验证 |
| 封面与新 PDF | 封面仍在设计评审，当前主分支没有正式封面；最新图文尚未重出打印版。先确定图文与封面，再生成、逐页检查并标注源提交 |
| 3 小时课件 | `slides/AIOS101-3h/` 保留 62 页独立评审稿，含已退出正文的图 6-9；不能声称与当前教材同步 |
| 第七至十二章 | 依据宪法逐章建立规格和正文，继续低门槛、自学与证据优先的写法 |
| 活动与教学实施 | 前两章已有四组学生、教师材料；网页活动暂停。课程学时、考核、班级与环境仍按课程总规格逐项确定 |
| 发布许可 | 课程整体许可与正式出版素材条件仍待维护者确定；现有来源、署名和第三方权利不能被整理覆盖 |

后续任务在[协作交接 Issue #2](https://github.com/X-lab2017/AIOS101/issues/2)中认领；一次聚焦一章或一个明确问题，不重复创建已存在任务。

## 接手时必须知道

1. 先读[关键决策](decisions/ADR-0001-reading-and-evidence-baseline.md)和[维护指南](content-iteration-guide.md)，再核对工作区、远程 main、相关 Issue 与最近工作流。
2. Markdown 正文、图版清单与品牌资产各有唯一正本。不要编辑 `dist/`，不要从旧 PDF、旧课件或历史截图反向覆盖正文。
3. 删除、归档与改名的完整清单见[文件记录](maintenance/2026-10-29-files.json)。保留 Git 历史，不强推、不覆盖他人变更。
4. 生成素材须记录输入、提示、来源与边界；来源文件、可复算脚本与原始证据不能只存在对话或临时目录。
5. 所有“完成”声明限定到实际检查；网站可访问、内容评审、教学效果与出版清权分别记录。
