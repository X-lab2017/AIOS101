# 交互开发需求：拆解一项开放成果——从公开到复用

> 状态：历史交互设计，当前暂停上线。教学目标仍可复用；当前 app.js 已是纯阅读实现。恢复前按[交互入口](../README.md)重新对齐，不把下文 v0.4 状态当作现行网站。

> 活动 ID：`ACT-CH02-01`
>
> 学习证据：`EVD-CH02-01`
>
> 状态：v0.4 分步交互打样已实现；教学验收和课堂实测待进行
>
> 教学正本：[学生任务单](../../activities/student/ACT-CH02-01.md)
>
> 实施依据：[活动规格](../../activities/ACT-CH02-01-openness-reuse-mechanism-spec.md)｜[教师指南](../../activities/teacher/ACT-CH02-01.md)

## 一、交互目标

把四次虚构发布转化为可逐层展开、可分类、可比较和可导出的机制分析。交互应帮助学生看到“新增材料—形成条件—仍有边界”，而不是把四次发布做成自动加分的升级游戏。

不得自动判断现实项目是否开源，也不得根据材料数量计算公共价值分数。

## 二、用户流程

1. 展示“已公开发布”，记录学生初始判断；
2. 逐次展开四次发布，让学生填写新增材料、可能行动和不能推出的结论；
3. 选择复用目标，完成对象、版本、权利、文档、格式、来源、署名和验证清单；
4. 将案例证据连接到发现需要、提出贡献、评审、决定、发布和维护等协作环节；
5. 写出公开到复用、复用到协作、协作到公共价值的三个断点；
6. 记录至少三个公共价值未知事项；
7. 输入线下或在线同伴反馈，完成修订；
8. 预览并导出 Markdown 或 JSON。

## 三、建议数据结构

```text
activity_id: ACT-CH02-01
evidence_id: EVD-CH02-01
schema_version: 1
status: draft | complete
initial_judgment: {can_do, needs_evidence, reflection}
releases[]:
  release_id
  new_materials
  enabled_actions
  unsupported_conclusions
reuse_goal: string
reuse_conditions[]:
  type
  existing_evidence
  to_verify
reuse_explanation: string
collaboration[]:
  stage
  evidence
  missing_consequence
collaboration_explanation: string
breakpoints:
  openness_to_reuse
  reuse_to_collaboration
  collaboration_to_public_value
public_value_unknowns[]: string
peer_feedback: string
revision: {feedback_response, changes, new_understanding}
ai_disclosure: {used, description, verification}
```

所有结论应能回溯到虚构案例材料。`status: complete` 只表示学生确认填写完整，不表示教师评价或学习成果达成。

## 四、保存、反馈与导出

- 默认本地保存，无需账号，刷新后恢复，可清除草稿；
- 支持 Markdown、JSON 导出及 JSON 重新导入；
- 导出保留四次发布比较、未知事项、反馈和修订，而非只输出最终表格；
- 自动反馈仅检查缺项，并提示“这属于条件、过程还是结果”“案例是否提供这项证据”；
- 若学生把“未知”写成“没有”，提示区分证据缺失与负面事实，但不自动改写答案；
- 不按材料数量、关键词或发布次数生成开源、协作质量或公共价值评分。

## 五、回退、隐私与可及性

- 交互不可用时直接使用[学生任务单](../../activities/student/ACT-CH02-01.md)；
- 案例全部内置，无网络也能完成，不要求访问真实社区；
- 不默认上传、公开或收集真实姓名；
- 卡片分类提供按钮和文本等效路径，拖拽不是唯一操作；
- 支持窄屏、键盘和屏幕阅读器，状态不只依赖颜色。

## 六、验收测试

- [ ] 四次发布、复用清单、协作闭环、三个断点、公共价值未知、互评、修订和披露均完整；
- [ ] 每次判断能够关联案例材料，未知与“没有”被清楚区分；
- [ ] 本地恢复、清除、导出和重新导入字段一致；
- [ ] 不产生自动开源认定、综合评分或公共价值结论；
- [ ] 无网络、无脚本、窄屏和键盘路径可用；
- [ ] 不默认上传或公开个人内容。

## 当前实现挂载（v0.4）

- 在线入口：[#/activity/ACT-CH02-01](https://www.x-lab.info/AIOS101/#/activity/ACT-CH02-01)。
- 字段与流程：[learning-data.js](../../site/learning-data.js)；本地数据、迁移和导出：[learning-core.js](../../site/learning-core.js)；统一页面：[v0.4 页面实现](https://github.com/X-lab2017/AIOS101/blob/8a529d1bfc74c62995d83787823770a059059d3d/site/app.js)。
- 使用 schema 2 的 activities[活动 ID] 保存 fields、step、status、history；教学字段按本页要求映射，原建议结构不作为已经发布的数据格式。
- 自动检查只提示缺项；反馈由本人、同伴或教师填写，完成状态不等于学习评价。静态回退使用上方学生任务单。
- 实际核验范围与限制见[学习版核验记录](../../specs/history/learning-review-record.md)。
