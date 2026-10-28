# 来源与证据登记表

> 版本：v0.1
> 用途：登记支持课程关键结论、数据、案例、图表、代码和实践的材料。不得为填满表格而登记未实际阅读的来源。

## 1. 核验状态

- **已核验**：已阅读相关原文并核对定位、版本和适用结论；
- **部分核验**：只阅读部分内容或只核验部分字段，须注明范围；
- **待核验**：仅作为线索保留，不得支撑正式发布的关键结论；
- **需复核**：来源、版本、许可或结论出现变化，需要重新检查；
- **失效／归档**：不再作为当前依据，但为历史版本保留记录。

## 2. 来源登记

| 来源 ID | 类型 | 标题／对象 | 作者／机构 | URL／出版信息 | 定位 | 发布／版本日期 | 读取日期 | 许可 | 核验状态 | 使用位置与结论 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SRC-2026-001 | 项目文档 | OpenDipper 项目中文说明 | X-lab | [固定提交](https://github.com/X-lab2017/open-dipper/blob/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/README.zh-CN.md) | 模块表、数据边界、披露与复用 | 应用 v1.16.1；提交 8fa36b5 | 2026-10-28 | 根应用许可未选定；仅作事实重述与链接 | 已核验 | 序言与 CH03：OpenDipper 的生态观测工具定位、模块、教学入口及公开可下载的边界 | 未复制图片、代码、数据或品牌素材；CH03 原图占位待补，出版复用条件待确认 |
| SRC-2026-002 | 模块契约 | Open Galaxy／开源星系契约 | X-lab | [固定提交](https://github.com/X-lab2017/open-dipper/blob/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/docs/OPEN_GALAXY.md) | Discovery and research；Data contract | 发布实现 1.5.1；提交 8fa36b5 | 2026-10-28 | 未统一授权；仅作事实重述与链接 | 已核验 | 序言与 CH03：记录关系、推断关系与软件依赖链的区别；CH03 另用于说明样本覆盖和未知项 | 上游数据快照具有独立观察期；共同贡献者或发布者路径不是软件依赖链 |
| SRC-2026-003 | 数据证据规范 | OpenShare and GOSD observed evidence | X-lab | [固定提交](https://github.com/X-lab2017/open-dipper/blob/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/docs/DATA_EVIDENCE.md) | Product selection；Versioned data path | 固定提交 8fa36b5 | 2026-10-28 | 未统一授权；仅作事实重述与链接 | 已核验 | 序言：指标口径、独立观察期、覆盖范围与缺失值原则 | 未在序言引用具体统计数值或宣称复算 |
| SRC-2026-004 | 项目发布截图 | OpenDipper 开源星系浅色实景截图及截图说明 | X-lab | [截图](https://raw.githubusercontent.com/X-lab2017/open-dipper/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/docs/assets/opendipper-1.6.0-galaxy-light-20261027.jpg)；[说明](https://github.com/X-lab2017/open-dipper/blob/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/docs/assets/README.md) | Current product screenshots；完整 1363×936 视口 | 应用 v1.6.0；截图 2026-10-27；提交 8fa36b5 | 2026-10-28 | 根应用许可未选定；本稿仅限专家评审，出版授权待复核 | 已核验 | 序言图 0-1：开源星系界面、记录关系与观察边界 | 原始 JPEG 未编辑；截图日期不等于数据观察期 |
| SRC-2026-005 | 原始历史文献 | Initial Announcement of the GNU Project | Richard Stallman／GNU Project | [GNU 初始声明](https://www.gnu.org/gnu/initial-announcement.html) | 发布日期、GNU 目标、贡献邀请及 free 含义脚注 | 初始发布 1983-09-27；网页含后续说明 | 2026-10-28 | GNU 网站文本；仅事实重述、短引与链接，不复制长段文本 | 已核验 | CH01：GNU 起点、Stallman、自由与协作问题 | 初始计划并不等同于后续实际历史 |
| SRC-2026-006 | 官方定义 | What is Free Software? | Free Software Foundation | [自由软件定义](https://www.gnu.org/philosophy/free-sw.html) | The four essential freedoms；open source 说明 | 页面持续修订；读取时版本历史至 1.169 | 2026-10-28 | 页面标注 CC BY-ND 4.0；仅事实重述与链接 | 已核验 | CH01：运行、研究修改、复制分享、分享修改版本四项自由 | 自由软件与开源的价值表述不可混同 |
| SRC-2026-007 | 历史发布说明 | Notes for linux release 0.01 | Linus Torvalds／Linux Kernel Archives | [Linux 0.01 发布说明](https://www.kernel.org/pub/linux/kernel/Historic/old-versions/RELNOTES-0.01) | Short intro；Copyrights；反馈与阅读用途 | Linux 0.01，1991 | 2026-10-28 | 历史发布说明；仅事实重述与链接，未复制源码 | 已核验 | CH01：Linux 早期公开源码、阅读、编译与反馈协作 | 早期许可不能直接套用后来的开源定义 |
| SRC-2026-008 | 官方历史 | History of the Open Source Initiative | Open Source Initiative | [OSI 历史](https://opensource.org/history) | Coining “Open Source”；Founding The Organization；Assessing Licenses | 页面创建 2006-09-19；修改 2025-06-03 | 2026-10-28 | 网站内容 CC BY 4.0；事实重述与链接 | 已核验 | CH01：1998 术语、Peterson、Raymond、Perens、OSI 与 DFSG 渊源 | 历史叙述与课程作者解释分开 |
| SRC-2026-009 | 官方定义 | The Open Source Definition | Open Source Initiative | [开放源代码定义](https://opensource.org/osd) | Introduction；Free Redistribution；Source Code；Derived Works | OSD 1.9；文本修改 2007-03-22；页面修改 2024-02-16 | 2026-10-28 | 网站内容 CC BY 4.0；事实重述与链接 | 已核验 | CH01：开源不只是源码可见，还涉及分发与修改条件 | 不在本章展开完整许可证教学 |
| SRC-2026-010 | 官方定义 | The Open Source AI Definition 1.0 | Open Source Initiative | [OSAID 1.0](https://opensource.org/ai/open-source-ai-definition) | 四项自由；Preferred form；Data Information、Code、Parameters | OSAID 1.0 | 2026-10-28 | 网站内容 CC BY 4.0；事实重述与链接 | 已核验 | CH01：AI 开放的自由及代码、数据信息、参数三类材料 | 不用该定义为具体产品作未经核查的认定 |
| SRC-2026-011 | 开放协作指南 | How to Contribute to Open Source | Open Source Guides／GitHub 及贡献者 | [贡献指南](https://opensource.guide/how-to-contribute/)；[许可](https://raw.githubusercontent.com/github/opensource.guide/main/LICENSE) | 非代码贡献；项目组成；贡献前检查；沟通、评审与后续回应 | 持续更新网页；读取日期版本 | 2026-10-28 | 内容 CC BY 4.0；事实重述与链接 | 已核验 | CH02：贡献类型、项目情境、公开沟通、评审和维护成本 | 不把指南建议写成所有项目的统一规则 |
| SRC-2026-012 | 开源项目专著 | Producing Open Source Software，2nd Edition | Karl Fogel | [版本入口](https://producingoss.com/en/index.html)；[社会基础设施](https://producingoss.com/en/social-infrastructure.html)；[技术基础设施](https://producingoss.com/en/technical-infrastructure.html) | 信息管理、协作工具、项目持续性与可分叉性 | 2.3315，2026-05-20 | 2026-10-28 | CC BY-SA 4.0；事实重述与链接 | 已核验 | CH02：协作不只是人数，项目需要记录、工具、治理与持续维护 | 只阅读所列章节，不声称核验全书 |
| SRC-2026-013 | 数字公共品标准 | Digital Public Goods Standard | Digital Public Goods Alliance | [DPG Standard](https://digitalpublicgoods.net/standard/) | 九项指标；开放许可、所有权、文档、隐私、安全与防止伤害 | 持续更新网页；读取日期版本 | 2026-10-28 | 标准 CC BY-SA 4.0；事实重述与链接 | 已核验 | CH02：公共价值不能由开放许可单独证明，还需考虑文档、隐私与风险 | 不用于给具体项目认证或构造课程评分 |
| SRC-2026-014 | 教材 | 解码开源：开源生态 60 问 | 庄表伟 | 用户提供的 2026 年 PDF 版本，共 256 页 | 第 1、5、8、35 问及前言 | 2026 年；前言署名日期 2026-05 | 2026-10-28 | 用户提供评审副本；仅作内部研读与事实重述，不复制正文 | 部分核验 | 全书背景素材库；仅在特定主题确有需要时选用具体内容，不设为各章固定延伸阅读 | 未声称核验全书；正式出版信息待版权页复核 |
| SRC-2026-015 | 教材 | 开源软件构建技术：理论与实践 | 作者信息以正式版权页为准 | 用户提供的打印版 DOCX | 第 3 章开源软件版本控制管理；第 6 章开源任务参与实践；相关导论 | 打印版，日期待版权页复核 | 2026-10-28 | 用户提供评审副本；仅作内部研读与事实重述，不复制正文 | 部分核验 | 全书技术与实践素材库；按具体知识点选用，不设为各章固定延伸阅读 | 未声称核验全书；不猜写作者与出版信息 |
| SRC-2026-016 | 真实项目文档 | DeepSeek-R1 官方仓库 README | DeepSeek-AI | [固定提交](https://github.com/deepseek-ai/DeepSeek-R1/blob/0cf78561f1d51c84a21b2190626b21116d5c68bb/README.md) | 产品与 API 入口、模型下载、训练概述、运行说明、生成建议、评测设置与结果、许可与上游许可提示 | 提交 0cf78561f1d51c84a21b2190626b21116d5c68bb | 2026-10-28 | 项目文档与 MIT License；仅事实重述与链接，不复制长段文本 | 已核验 | CH01：产品、模型、权重、代码与许可分别观察；CH03：模型资产与派生关系；CH04：后训练与蒸馏；CH05：生成配置、vLLM 运行示例、公开评测设置与证据边界 | 不用该案例替代 OSAID 判断，不推断在线产品全部开放或训练可复现；vLLM、SGLang 是运行示例；公开测评为项目自报，本书未复算 |
| SRC-2026-017 | 真实项目文档 | AIInfra README 与 LICENSE | Infrasys-AI／AIInfra 贡献者 | [固定提交](https://github.com/Infrasys-AI/AIInfra/tree/b97c0385ba07a62a717d82a0e7aed2927f12fc35) | 课程说明、资源入口、推理课程分类、仓库体积与 Releases 复用提示、Apache License 2.0 | 提交 b97c0385ba07a62a717d82a0e7aed2927f12fc35 | 2026-10-28 | 项目 Apache License 2.0；仅事实重述与链接 | 已核验 | CH02：公开材料、开放许可、复用成本与版本证据；CH05：新生导言摘要的最小评价任务输入与延伸阅读 | 固定提交是 PR #364 的合并提交；不据此评价项目全部内容质量；摘要任务不附带虚构模型输出或得分 |
| SRC-2026-018 | 真实社区记录 | AIInfra Issue #386 | AIInfra 社区参与者 YanJiaHuan | [Issue #386](https://github.com/Infrasys-AI/AIInfra/issues/386) | H100 FP8 数值疑问、项目原文位置与官方文档链接；开放状态 | 2026-05-13 创建；读取时开放 | 2026-10-28 | 公开社区记录；仅事实重述与链接，不复制个人信息 | 已核验 | CH02：Issue 可跟踪问题，但提出问题不等于证据成立或已经修复 | 技术主张属于报告者，本书未独立复算数值 |
| SRC-2026-019 | 真实社区记录 | AIInfra Pull Request #364 | AIInfra 社区参与者与维护者 | [PR #364](https://github.com/Infrasys-AI/AIInfra/pull/364) | 量化章节字节数修正、单文件差异、维护者合并及合并提交 | 2025-12-04 创建；2025-12-22 合并；提交 b97c038 | 2026-10-28 | 公开社区记录；仅事实重述与链接 | 已核验 | CH02：小范围技术文档贡献、PR 差异与合并决定 | 不虚构公开评审对话，不由一次合并推断项目整体质量 |
| SRC-2026-020 | 平台官方文档 | GitHub Issues 与 Pull Requests 文档 | GitHub | [PR 概述](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)；[Issues 快速入门](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/quickstart) | Issue 跟踪；PR 的说明、提交、差异、检查、评审与合并；Fork 工作模式 | 持续更新网页；读取日期版本 | 2026-10-28 | 官方文档；仅事实重述与链接 | 已核验 | CH02：GitHub 平台与 Issue、PR、Fork 等概念 | 平台界面和功能可能变化，操作以当期文档为准 |
| SRC-2026-021 | 平台官方文档 | AtomGit Issue 与轻量级 PR 文档 | AtomGit | [Issue 简介](https://docs.atomgit.com/docs/help/home/org_project/issue/issue_introduction/)；[轻量级 PR](https://docs.atomgit.com/docs/help/home/org_project/pullrequests/pr-lightweight) | Issue 的问题与任务跟踪；PR 变更请求、代码审查和小范围贡献 | 持续更新网页；读取日期版本 | 2026-10-28 | 官方文档；仅事实重述与链接 | 已核验 | CH02：AtomGit 的国内平台实践场景与基本协作概念 | 不将平台功能等同于项目治理或贡献质量保证 |
| SRC-2026-022 | 研究报告 | 全球开源发展报告 2026（GOSD 2026） | 已读取封面、目录和封底未标明完整作者／机构，待正式版权信息确认 | 用户提供的 PDF 完整评审版，共 158 页 | 4.1.1 Agentic AI 技术结构；4.2 AI 大模型任务全景；4.6 PyTorch 生态；5.2.1 模型派生概念 | 完整评审版，2026-10-22；各图保留独立观察窗口 | 2026-10-28 | 用户提供评审副本；仅内部研读、事实重述与章节指引，未复制图表，再使用条件待确认 | 部分核验 | CH03：技术功能分层、任务分类、生态样本和模型派生关系；明确分类不等于依赖，精选样本不等于全球普查 | 4.1 为 145 个精选项目；4.2 为 2026-10-02 快照的 96 个模型、6 类任务；4.6 为 83 条相关项目记录；本章未复算原始数据，不使用模拟地域数据；图 4-1-1、4-1-2、4-2-1、4-6-1 的原图引用与出版授权待确认 |
| SRC-2026-023 | 研究论文 | The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale | Guilherme Penedo 等／Hugging Face | [arXiv v2](https://arxiv.org/html/2406.17557v2) | 摘要、第 1—3 节、第 6 节及附录 B | arXiv:2406.17557v2，2024-10-31 | 2026-10-28 | 论文页面标注 CC BY 4.0；FineWeb 数据集为 ODC-By 1.0，并受 Common Crawl 使用条件约束 | 已核验 | CH04：96 个 Common Crawl 快照、约 15 万亿 GPT-2 token、文本提取与过滤去重流程、消融控制条件、公开材料和实验边界；图 4-3 原图占位 | 只重述已阅读内容；未下载全量数据、未重训或独立复算；不推断 DeepSeek 使用 FineWeb；原图复用需保留完整署名并复核出版呈现 |
| SRC-2026-024 | 真实项目文档 | vLLM 官方仓库 README 与 LICENSE | vLLM 项目及贡献者 | [固定 README](https://github.com/vllm-project/vllm/blob/ab0e5ef7954190de2a74a6715d1382b08f5accc4/README.md)；[固定 LICENSE](https://raw.githubusercontent.com/vllm-project/vllm/ab0e5ef7954190de2a74a6715d1382b08f5accc4/LICENSE) | About 中的推理与服务定位、PagedAttention、连续批处理、分块预填充、前缀缓存、流式输出、分布式推理与硬件支持 | 提交 ab0e5ef7954190de2a74a6715d1382b08f5accc4 | 2026-10-28 | Apache License 2.0；仅事实重述与链接，不复制长段文本 | 已核验 | CH05：模型之外的推理引擎、内存管理、请求调度、服务与硬件层；说明系统表现不能仅归因于模型 | 只阅读固定 README 和许可；未安装、部署或进行兼容与性能测试；功能清单不等于任意模型和硬件组合均已验证 |
| SRC-2026-025 | 原始研究论文 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Patrick Lewis 等 | [arXiv v4](https://arxiv.org/abs/2005.11401v4)；[HTML 全文](https://arxiv.org/html/2005.11401v4) | 摘要、第 1—2 节、第 4.5 节索引热替换、第 6 节 | arXiv:2005.11401v4，2021-04-12 | 2026-10-28 | 论文页面未显示统一开放许可；仅事实重述与链接，不复制原图或长段文本 | 已核验 | CH06：参数记忆与非参数记忆、检索器与生成器、外部索引更新与可检查性；说明 RAG 不是单一固定产品形态 | 未运行论文代码或复算结果；论文中的性能结论仅属于其特定实验，不用于给当代产品排名 |
| SRC-2026-026 | 开放教材与实验文档 | 深入理解 AI Agent：设计原理与工程实践；第 2 章与网络搜索 Agent 说明 | 李博杰及项目贡献者 | [固定第 2 章](https://github.com/bojieli/ai-agent-book/blob/dbc046eb896ac4e39aa19c7774c8bf49583b89a6/book/chapter2.md)；[固定实验说明](https://github.com/bojieli/ai-agent-book/blob/dbc046eb896ac4e39aa19c7774c8bf49583b89a6/chapter1/web-search-agent/README.md)；[LICENSE](https://raw.githubusercontent.com/bojieli/ai-agent-book/dbc046eb896ac4e39aa19c7774c8bf49583b89a6/LICENSE) | 工具定义、模型调用请求、框架执行、工具结果与再次生成；离线轨迹的证据边界、最大迭代与检查方法 | 提交 dbc046eb896ac4e39aa19c7774c8bf49583b89a6 | 2026-10-28 | 根项目 Apache License 2.0；实验说明另标 MIT；仅事实重述与链接，截图复用须保留署名与对应许可 | 已核验 | CH06：区分模型生成工具请求与外部程序真实执行；轨迹、上下文、停止条件、离线与联网证据的区别 | 本书未安装或执行该项目，未调用联网搜索；书中 canned results 和离线轨迹不能写成真实天气或搜索事实 |
| SRC-2026-027 | 官方技术规范 | Model Context Protocol 2025-06-18：Architecture、Tools 与 Security and Trust & Safety | Model Context Protocol 项目 | [架构](https://modelcontextprotocol.io/specification/2025-06-18/architecture)；[工具](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)；[安全原则](https://modelcontextprotocol.io/specification/2025-06-18)；[固定仓库 LICENSE](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/ccaf9102ec5eb656eab50ca8333ef49dcd259c26/LICENSE) | Host／Client／Server、工具定义与执行、输入输出核验、错误、人工确认、权限与隐私 | 规范版本 2025-06-18；许可快照 ccaf9102 | 2026-10-28 | 项目许可处于 MIT 向 Apache-2.0 过渡；规范按贡献适用 Apache-2.0／原 MIT，非规范文档 CC BY 4.0；仅事实重述与链接 | 已核验 | CH06：协议标准化工具连接但不替代任务授权；区分工具描述、调用请求、执行结果和错误；人工控制与最小权限 | 未实现 MCP 客户端或服务器；协议示例不是课程真实工具调用；具体产品安全能力需另行核验 |

## 3. 数据与版本补充记录

对于数据、模型、代码仓库和在线平台，应在备注或关联记录中补充：

- 统计对象、时间窗口、样本和分母；
- 数据文件、提交号、模型 ID、快照或版本；
- 获取方式、转换、去重和聚合规则；
- 实际复算或运行程度；
- 缺失、未知、模拟和未覆盖状态；
- 外部材料的依赖与各自许可。

## 4. 维护规则

- 来源 ID 永久唯一，不复用；
- 一个来源支持多个结论时，分别说明使用位置和适用范围；
- 新版本不直接覆盖旧版本证据，必要时新增记录并建立关联；
- 引用失效时保留原出版信息和可用存档；
- 正式章节验收前，关键来源不得停留在“待核验”；
- 本表是查证入口，不自动证明所有指标已经计算或所有实验已经运行。

## 前三章在线图版补充记录（2026-10-28）

16 幅图版的文件、图号、原始来源、截图日期、修改方式及第三方复用条件统一登记于 [附图索引](../textbook/assets/figures/README.md) 与 [人物参考记录](../textbook/assets/figures/portrait-sources.md)。本次为维护者授权的课程仓库与 Pages 公开评审；不将其记为正式出版清权。
