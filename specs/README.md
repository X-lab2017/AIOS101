# AIOS101 规格体系

## 1. 目的

本目录将[课程宪法](../CONSTITUTION.md)转化为可执行、可检查、可验收的开发规格。教材、讲义、实验、图表、网站、评价工具及其他产物均须能够追溯到相应规格。

规范用语：

- **必须**：发布前的强制条件，不满足即不能验收；
- **应**：原则上需要满足，例外必须记录理由；
- **可**：根据教学目标与实施条件选择。

## 2. 规格层级

| 层级 | 文件 | 回答的问题 | 主要下游产物 |
|---|---|---|---|
| 宪法 | `CONSTITUTION.md` | 为什么建设这门课，什么不能偏离 | 全部规格与产物 |
| 课程规格 | `specs/course-spec.md` | 教什么、学到什么、如何形成课程证据 | 章节规格、评价体系、综合项目 |
| 导入规格 | `specs/preface-spec.md` | 如何为全体学习者建立课程问题、全书地图与学习预期 | 教材序言、课程导入 |
| 章节规格 | `specs/chapter-spec-template.md` | 每章如何对齐成果并组织学习 | 教材、讲义、章节活动、章节评价 |
| 活动规格 | `specs/activity-spec-template.md` | 实践如何做、留下什么、如何评价 | 实验、数据任务、贡献任务、活动量规 |
| 支撑规范 | 内容、评价、展现等规范 | 各类产物共同遵守什么标准 | 跨章节一致性与质量控制 |
| 验收规范 | `specs/acceptance-spec.md` | 什么条件下可以称为完成并发布 | 验收记录、发布决定、整改任务 |

## 3. 标准开发流程

1. **对齐宪法**：确认工作项对应的课程定位、学习成果与一级目录。
2. **编写或更新规格**：先明确范围、产物、证据和验收条件。
3. **规格评审**：状态进入“已批准”后，再开展实质内容生产。
4. **同步生产**：教材、讲义、活动、视觉与评价依据同一规格开发。
5. **执行验收**：按质量门禁逐项检查，保留证据和未决问题。
6. **发布与迭代**：记录版本、变更、来源和后续改进项。

禁止先大规模生产内容，再补写规格以追认既有结果。

## 4. 标识规则

| 对象 | 格式 | 示例 |
|---|---|---|
| 学习成果 | `LO1`—`LO6` | `LO4` |
| 章节 | `CH01`—`CH12` | `CH07` |
| 章节成果 | `CHxx-LO-n` | `CH07-LO-1` |
| 活动 | `ACT-CHxx-nn` | `ACT-CH09-01` |
| 学习证据 | `EVD-CHxx-nn` | `EVD-CH07-01` |
| 来源 | `SRC-YYYY-nnn` | `SRC-2026-001` |
| 决策记录 | `ADR-nnnn` | `ADR-0001` |
| 变更请求 | `CR-YYYY-nnn` | `CR-2026-001` |

标识一经使用不得复用。章节更名不改变章节编号；删除对象时保留历史记录。

## 5. 规格状态

规格统一使用以下状态：

`草稿 → 评审中 → 已批准 → 实施中 → 待验收 → 已验收 → 已发布`

- **草稿**：允许存在未决项，不得作为大规模生产依据；
- **评审中**：范围和验收条件完整，等待评审；
- **已批准**：目标、范围和验收条件冻结，可开始生产；
- **实施中**：下游产物正在开发；
- **待验收**：产物齐全，已附验收证据；
- **已验收**：质量门禁通过，遗留问题不妨碍使用；
- **已发布**：已形成明确版本并对学习者可用。

“完成写作”不等于“已验收”，“文件已合并”不等于“已发布”。

## 6. 文件组织

```text
CONSTITUTION.md
AGENTS.md
CONTRIBUTING.md
CHANGELOG.md
specs/
  README.md
  course-spec.md
  preface-spec.md
  chapter-spec-template.md
  activity-spec-template.md
  chapters/
    CH01-ai-open-source-literacy-spec.md
  content-evidence-spec.md
  assessment-spec.md
  presentation-spec.md
  acceptance-spec.md
  collaboration-spec.md
  source-register.md
  decision-record-template.md
  change-request-template.md
textbook/
  preface.md
  chapters/
  assets/
activities/
slides/
online/
interactive/
deliverables/
scripts/
  check_repo.py
```

`textbook/chapters/` 是章节正文唯一正本；`online/` 保存在线版配置与组件；`interactive/` 保存交互实现与回退资源。新目录必须在相应规格中说明用途，不得形成无人维护的重复正本。

## 7. 变更与验收原则

- 宪法级、规格级、内容级变更按[课程宪法](../CONSTITUTION.md)和[协作规范](collaboration-spec.md)处理。
- 下游产物发生实质变化时，必须检查上游规格是否仍然准确。
- 每次变更必须明确受影响的章节、活动、评价和展现产物。
- 所有“已完成”声明必须对应[验收规范](acceptance-spec.md)中的证据。
- 未验证、未覆盖、待核实和真实为零必须分别记录，不得用确定语气掩盖缺口。

## 8. 在线学习资源评审

本轮经维护者授权，同步设计有限范围的评审原型，规格保持评审中。

- [VIS-AIOS101 课程专属视觉](course-identity-spec.md)
- [WEB-AIOS101 网站建设规格](website-spec.md)
- [WEB-ACT-01／02 序言及系统探索活动](website-activities.md)
- [技术核验与未决事项](website-review-record.md)
