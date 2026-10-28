# 仓库材料对齐与协作交接记录

日期：2026-10-29；工作项：MAINT-20261029。维护者已授权整理、删除过时材料并记录协作过程。整理前 main 为 `b17a9b8ecfb973d53c970a55e93c1341f568e60b`，本地已跟踪文件与远程逐项一致。

## 已完成的整理

- 当前入口统一到 README → docs/STATUS → 维护指南／ADR；章节版本、图数与当前图版从正本自动核对。
- 历次规格和评审移入历史目录，补充历史状态标识、索引并修复相对链接。来源、图版原件、授权边界和验收证据继续保留。
- 课件标为独立评审稿，活动标为暂停上线；新 PDF、正式封面、真人试学与出版清权不冒称已完成。
- 当前 Pages 仅分发清单内图版与阅读代码；历史兼容脚本保留在仓库和测试中。
- 本地与 Actions 使用统一检查入口；新增状态一致性检查，明确运行阅读回归。

## 删除清单

以下 11 个文件从当前树移除，共 19,388,222 字节（约 19.4 MB）；不改写 Git 历史，仓库历史下载体积不因此消失。

| 原路径 | 原因 | 固定版本 |
|---|---|---|
| `deliverables/AI开源通识_序言_v0.2_专家评审稿.docx` | 序言 v0.2 交付已被当前 Markdown 与 Pages 替代。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/deliverables/AI开源通识_序言_v0.2_专家评审稿.docx) |
| `deliverables/AI开源通识_序言_v0.3_清爽内容评审稿.docx` | 序言 v0.3 无图 Word 已过时。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/deliverables/AI开源通识_序言_v0.3_清爽内容评审稿.docx) |
| `deliverables/AI开源通识_序言与前六章_图文评审版_2026-10-29.pdf` | 早期 127 页合并稿，不含本轮自学与图版修订；避免误认成当前打印版。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/deliverables/AI开源通识_序言与前六章_图文评审版_2026-10-29.pdf) |
| `deliverables/AI开源通识_序言与前六章_排版核验.json` | 仅对应已移除的旧 PDF，不能证明当前排版。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/deliverables/AI开源通识_序言与前六章_排版核验.json) |
| `scripts/create_preface_docx.js` | 硬编码 v0.2 正文与旧视觉，形成第二份正本。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/scripts/create_preface_docx.js) |
| `scripts/create_preface_clean_docx.js` | 固定 v0.3 文案并忽略当前插图和表格，不适用于现行序言。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/scripts/create_preface_clean_docx.js) |
| `scripts/package.json` | 仅服务已删除的旧 Word 生成脚本。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/scripts/package.json) |
| `scripts/package-lock.json` | 仅服务已删除的旧 Word 生成脚本。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/scripts/package-lock.json) |
| `site/assets/course/aios101-identity-kit-v0.1.zip` | 被已批准、校验固定的 v1.0.0 品牌包替代。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/site/assets/course/aios101-identity-kit-v0.1.zip) |
| `online/README.md` | 空壳目录且描述失效交互，开发入口统一到 site/README.md。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/online/README.md) |
| `textbook/assets/ch01/README.md` | 错误图号和待设计占位，统一由当前图版索引替代。 | [恢复来源](https://github.com/X-lab2017/AIOS101/blob/b17a9b8ecfb973d53c970a55e93c1341f568e60b/textbook/assets/ch01/README.md) |

完整改名映射和字节数见[文件清单](maintenance/2026-10-29-files.json)。21 份已有记录移动，另保留旧图版 README 与旧变更日志快照；不把历史中的数量和“当前”重新认证为现状。

恢复单个文件时在完整 Git 克隆中执行（将最后的路径替换为清单内需要恢复的文件）：

```bash
git restore --source=b17a9b8ecfb973d53c970a55e93c1341f568e60b -- path/to/file
```

恢复后先检查差异；不要将整棵历史树恢复到主分支。

## 保留的材料与理由

- 所有当前教材、图版、原始截图、提示、字体许可和品牌固定资产保留。
- 退出正文的图号及旧矢量是溯源和再生成输入，不因未发布就删除。
- 四项活动及旧数据逻辑有教学和兼容价值，未恢复到网页；62 页课件有独立用途，逐页对齐单独跟踪。
- 本地未提交的封面方案没有纳入本轮提交；正式封面尚未进入 main。

## 验证与发布

统一检查 `python scripts/check_all.py` 与 `git diff --check` 已通过：品牌 34 文件／16 份生产 SVG 及固定包不变；8 个完整单元、44 幅图、29 幅 SVG、30 份折叠结构源码一致；状态表、当前发布资产、阅读界面与旧数据逻辑均通过。文档整理中的相对链接已修复。

部署提交、Actions 与线上抽查的最终结果记录在[协作交接 Issue #2](https://github.com/X-lab2017/AIOS101/issues/2)，避免为补写部署 SHA 再触发循环发布。提交前另在只含拟提交文件的干净导出中执行相同检查。

本轮不验证教学效果、真实手机、印刷与未生成的 PDF／课件；不调整课程整体许可。
