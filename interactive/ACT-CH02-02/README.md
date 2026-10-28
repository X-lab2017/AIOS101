# 交互开发需求：设计一次有效贡献——从善意到可评审

> 活动 ID：`ACT-CH02-02`
>
> 学习证据：`EVD-CH02-02`
>
> 状态：待开发，尚未实现或课堂实测
>
> 教学正本：[学生任务单](../../activities/student/ACT-CH02-02.md)
>
> 实施依据：[活动规格](../../activities/ACT-CH02-02-reviewable-contribution-spec.md)｜[教师指南](../../activities/teacher/ACT-CH02-02.md)

## 一、交互目标

帮助学生把模糊善意整理成一项范围适当、证据完整、可以接受角色评审的贡献方案，并保留反馈、回应和修订。界面及导出必须始终标明“模拟贡献”，不得连接真实项目提交或生成虚假社区状态。

## 二、用户流程

1. 阅读虚构项目目标、现有材料、贡献规则和候选需要；
2. 选择或补充项目需要，填写受影响者、案例依据和待确认事项；
3. 选择贡献形式，限定交付物、修改范围和明确不做的内容；
4. 形成贡献说明，补充来源、许可、检查方式和 AI 披露；
5. 分析评审成本、后续维护、隐私和其他风险；
6. 由同伴输入角色评审意见及模拟决定，或使用教师预写意见；
7. 逐条回应反馈，保留采纳情况、理由和修订前后版本；
8. 区分预期受益者、可观察价值证据、未覆盖群体和未知结论；
9. 导出标注“模拟贡献”的 Markdown 或 JSON。

## 三、建议数据结构

```text
activity_id: ACT-CH02-02
evidence_id: EVD-CH02-02
schema_version: 1
contribution_mode: simulated
status: draft | complete
project_context: {project_name, materials_reviewed, rules_version}
need: {description, affected_people, evidence, to_confirm}
contribution:
  type
  deliverable
  scope
  out_of_scope
  materials
  validation_plan
proposal: string
responsibility:
  review_cost
  maintenance_cost
  licensing_notes
  risks
  rejection_response
review:
  reviewer_type: peer | teacher_prompt | self
  comments[]
  simulated_decision: accept | revise | decline
responses[]:
  feedback
  response
  adoption: accepted | partial | declined
  reason
revision: {before, after, changes, remaining_questions}
public_value:
  intended_beneficiaries
  intended_outcome
  observable_evidence
  uncovered_or_cost_bearers
  unsupported_conclusions
ai_disclosure: {used, description, verification, final_responsibility}
```

`simulated_decision` 只能表示课堂角色评审。界面不得显示“已合并”“已获社区接纳”“真实贡献”等状态。

## 四、保存、反馈与导出

- 默认本地保存，无需账号，不默认上传；支持刷新恢复、手动清除和 JSON 重新导入；
- Markdown 和 JSON 均在显著位置包含 `模拟贡献`；
- 导出保留原始方案、评审、逐条回应和修订版本，而非只保留最终文本；
- 自动反馈只检查缺项，提示范围是否过大、检查方式是否缺失、预期与证据是否混淆；
- 不自动给贡献质量、公共价值或模拟维护者决定评分；
- AI 可提供表达建议，但不得自动伪造同伴或维护者反馈。

## 五、回退、隐私与可及性

- 无网络、无脚本或组件失败时使用[学生任务单](../../activities/student/ACT-CH02-02.md)；
- 不提供真实 Issue／PR 提交按钮，不引导联系真实维护者；
- 不输入私人对话、敏感信息、真实学生作业或无权发布的材料；
- 角色评审默认仅班级内记录，公开展示由学生另行自愿选择；
- 支持窄屏、键盘和屏幕阅读器，评审状态不只依赖颜色或图标。

## 六、验收测试

- [ ] 需要、范围、贡献说明、来源、检查、维护、风险、评审、回应、修订、公共价值和披露均完整；
- [ ] 所有页面与导出均标注模拟，不能触发真实社区提交；
- [ ] 模拟决定不会被显示为真实接纳，未接纳也不自动等于学习未达成；
- [ ] 原始方案与修订版本均保留，本地恢复和导入导出字段一致；
- [ ] 自动反馈不伪造评审、不产生公共价值结论；
- [ ] 无网络、无脚本、窄屏、键盘和屏幕阅读器路径可用；
- [ ] 不默认上传或公开个人内容。
