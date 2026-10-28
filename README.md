# AIOS101

《AI 开源通识》课程与配套教材、讲义、实践活动及评价资源的协作仓库。

课程以 AI 为学习对象，以开源为认识论、方法论和实践方式，引导学习者沿“使用—理解—探究—贡献—创造”的主线，从理解 AI 走向开放协作与负责任创造。

## 从这里开始

课程建设采用规格驱动开发（SDD）：先明确目标、证据和验收条件，再生产教材、讲义、活动、评价与数字资源。

1. [课程宪法](CONSTITUTION.md)：课程定位、学习成果、十二章目录与不可偏离的质量门禁；
2. [规格体系](specs/README.md)：规格层级、标识规则、状态流转和标准开发流程；
3. [课程总规格](specs/course-spec.md)：十二章、六项学习成果和最低学习证据的对齐关系；
4. [参与建设](CONTRIBUTING.md)：人类与 AI 贡献者的协作入口；
5. [AI 协作者工作指南](AGENTS.md)：AI 工作顺序、证据硬规则与交付要求；
6. [教材序言 v0.3](textbook/preface.md)：从一次 AI 提问进入模型供应链与开源生态的清爽内容评审稿；
7. [第 1 章 v0.1](textbook/chapters/CH01-why-ai-open-source-literacy.md)：从 AI 使用经验进入 GNU、Linux、OSI 的历史，再转向 AI 开源通识的理解与创造。

当前规格和章节处于草稿或实施阶段，不代表教材内容或课程实施已经完成验收。

## 仓库结构

```text
CONSTITUTION.md             课程最高基线
AGENTS.md                   AI 协作者工作指南
CONTRIBUTING.md             贡献流程
CHANGELOG.md                版本与变更记录
specs/                      课程、序言与跨产物规范
specs/chapters/             各章开发与验收规格
textbook/preface.md         教材序言正本
textbook/chapters/          各章教材正文唯一正本
textbook/assets/            图片、地图及视觉资产索引
activities/                 探究活动、学习证据与评价规格
slides/                     配套讲义入口与派生资源
online/                     在线版配置、组件与构建入口
interactive/                交互活动配置、组件与回退资源
deliverables/               Word 等评审交付稿
scripts/check_repo.py       仓库基础结构与 Markdown 静态检查
```

在线版直接读取教材正本，交互版通过章节、活动和学习证据 ID 挂载。后续内容必须依据相应规格在明确目录中建设，不另立相互冲突的正本。

## 基础检查

安装 Python 3 后，在仓库根目录运行：

```bash
python scripts/check_repo.py
```

该命令仅使用 Python 标准库，检查必需文件、核心规格章节、CH01—CH12 的完整顺序、Markdown 行尾空白及相对链接目标。通过此检查只代表基础结构合规，不等于内容、教学或技术验收全部通过。

完整验收要求见[验收与发布规范](specs/acceptance-spec.md)，重要变更记录见[更新日志](CHANGELOG.md)。

## 在线学习资源设计评审

- [网站建设规格 v0.1](specs/website-spec.md)
- [序言与系统探索活动设计](specs/website-activities.md)
- [网站开发与 GitHub Pages 发布说明](site/README.md)
- [技术核验记录](specs/website-review-record.md)

当前在线资源为维护者设计评审版，未通过课程教学验收；已提供完整序言阅读与活动样板，第 1 章草稿已入库、待在线接入，其余章节随制作进度扩展。
