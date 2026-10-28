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
7. [第 1 章 v0.4](textbook/chapters/CH01-why-ai-open-source-literacy.md)：从 AI 使用经验进入 GNU、Linux、OSI 的历史，再转向 AI 开源通识的理解与创造；
8. [第 2 章 v0.4](textbook/chapters/CH02-open-source-mechanisms.md)：以真实仓库和社区记录解释开放、复用、协作与公共价值；
9. [第 3 章 v0.1](textbook/chapters/CH03-ai-open-source-ecosystem.md)：以资产、关系、参与者与规则建立 AI 开源生态全景；
10. [附录 A](textbook/appendices/APP-A-repository-snapshots.md)：仓库、提交号与固定版本的共同访问指南。

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
textbook/appendices/        跨章节共享的访问指南与知识支架
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

## 在线学习资源

- [网站建设规格 v0.4](specs/website-spec.md)
- [课程专属视觉识别 v1.0.0](specs/course-identity-spec.md)
- [序言与系统探索活动设计](specs/website-activities.md)
- [网站开发与 GitHub Pages 发布说明](site/README.md)
- [学习体验与活动规格 v0.4](specs/learning-experience-spec.md)
- [学习版核验记录](specs/learning-review-record.md)
- [早期原型核验记录](specs/website-review-record.md)

[进入 AIOS101 课程网站](https://www.x-lab.info/AIOS101/) · [课程视觉方案](https://www.x-lab.info/AIOS101/#/identity)

当前为 v0.4 交互学习打样，教学验收待评审。绪论、前两章和附录 A 已接入完整阅读；三个案例观察窗与四项分步活动支持笔记、草稿、人工反馈、修订快照和导出恢复。第三章 v0.1 草稿已自动接入阅读，配套活动待制作；CH04—CH12 随教材逐步上线。

公开预览发布范围与实际核验记录见 [Pages 发布记录](specs/pages-release-record.md)。

## 视觉基线与复用

[AIOS101 视觉基线 v1.0.0](brand/README.md)已固化：包含 Logo、配色与字体、X-lab 联合署名、四篇图形、离线示例和带 SHA-256 清单的资产包。后续教材、课件、网站及课程传播统一从此入口取用。
