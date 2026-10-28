# 交互开发需求：从一次 AI 回答到四种学习行动

> 状态：历史交互设计，当前暂停上线。教学目标仍可复用；当前 app.js 已是纯阅读实现。恢复前按[交互入口](../README.md)重新对齐，不把下文 v0.4 状态当作现行网站。

> 活动 ID：`ACT-CH01-01`
>
> 学习证据：`EVD-CH01-01`
>
> 状态：v0.4 分步交互打样已实现；教学验收和课堂实测待进行
>
> 教学正本：[学生任务单](../../activities/student/ACT-CH01-01.md)
>
> 实施依据：[活动规格](../../activities/ACT-CH01-01-usage-understanding-creation-spec.md)｜[教师指南](../../activities/teacher/ACT-CH01-01.md)

## 一、要解决的问题

把纸质或 Markdown 任务单转化为可分步完成、可保存、可互评、可修订和可导出的学习过程。交互的价值是帮助学生看见“使用—理解—创造”的差异，而不是用动画或自动评分替代思考。

本页面不得自动判断某个 AI 工具是否开源，也不得把学生的设想显示为已经完成的研究或贡献。

## 二、用户流程

1. **记录案例**：填写工具或材料名称、任务、必要输入和回答摘要；提供教师统一案例入口。
2. **提出理解问题**：填写三个仅凭回答无法确认的问题，并选择或补充需要观察的材料。
3. **比较四种行动**：分别填写使用、研究、修改和分享所需的材料与条件。
4. **辨析学习位置**：完成“我得到什么／我还不能判断什么／下一步需要什么证据”对照表。
5. **连接历史与边界**：选择 GNU、Linux 或 OSI 的历史坐标，写出连接句和当前结论边界。
6. **同伴互评**：由学生输入同伴意见，或在线下互评后记录；系统不代替同伴生成评价。
7. **修订与披露**：保留修订前后内容、修订说明和 AI 使用披露。
8. **导出提交**：预览完整任务单，导出 Markdown 或 JSON。

每一步均可返回修改，不因步骤顺序丢失已填内容。允许先保存未完成草稿，但导出时应明确标记缺项。

## 三、建议数据结构

```text
activity_id: ACT-CH01-01
evidence_id: EVD-CH01-01
schema_version: 1
status: draft | complete
case:
  tool_or_material
  task
  input_summary
  answer_summary
understanding_questions[]:
  question
  needed_evidence
actions:
  use: {materials_conditions, uncertainty}
  study: {materials_conditions, uncertainty}
  modify: {materials_conditions, uncertainty}
  share: {materials_conditions, uncertainty}
learning_positions:
  use: {gained, cannot_judge, next_evidence}
  understand: {gained, cannot_judge, next_evidence}
  create: {gained, cannot_judge, next_evidence}
history_connection: {coordinate, explanation, analogy_boundary}
boundary: string
peer_feedback: {feedback, source_type}
revision: {before, after, explanation}
ai_disclosure: {used, description}
```

导出字段名称可以在实现时采用等效命名，但不得丢失任务单要求的内容。`status: complete` 只表示学生确认已填写，不表示教师已评价或学习成果已达成。

## 四、保存、导入与导出

- 默认保存在当前浏览器本地，无需账号，不默认上传任何内容；
- 页面刷新或暂时关闭后能够恢复本地草稿，并提供“清除本地内容”操作；
- 支持导出 UTF-8 编码的 Markdown 和 JSON，文件名包含活动 ID，不包含学生真实姓名；
- JSON 能重新导入并继续编辑，导入前提示是否覆盖当前草稿；
- Markdown 是学生可直接阅读和提交的完整任务单，不是调试信息或只有链接的空壳；
- 导出内容标明草稿状态、缺项、修订说明和 AI 使用披露；
- 如未来增加云端同步或互评功能，必须另行说明数据范围、可见对象、保存期限和删除方式。

## 五、反馈规则

自动反馈仅用于：

- 标出尚未填写的必要项目；
- 提示“仅凭回答能否确认”“需要什么材料”“这个结论能支持到哪里”等澄清问题；
- 在出现“免费所以开源”“能下载所以完整开源”等表述时，提示学生回到证据重新说明，而不直接给出事实认定。

不得根据关键词自动判定“是否开源”，不得自动给学生的历史解释、问题质量或反思打分，不得把 AI 生成的示范答案填作学生本人答案。

## 六、无网络回退、隐私与可及性

- 无脚本、交互加载失败或低性能设备上，直接提供[学生任务单](../../activities/student/ACT-CH01-01.md)作为等效路径；
- 不强制登录、公开发布、加入社区或提交私人 AI 对话；
- 教师案例不得包含真实个人信息、受限数据或未经许可的材料；
- 支持窄屏和移动端，主要操作不依赖悬停；
- 全部输入框有可见标签，步骤、错误和保存状态可被屏幕阅读器理解；
- 支持键盘完成全流程，焦点顺序清晰，颜色不是唯一状态提示。

## 七、验收测试

- [ ] 从案例记录到导出可完成全流程，四种行动、三种学习位置、历史连接、边界、互评、修订和披露均未遗漏；
- [ ] 刷新页面后本地草稿恢复，清除操作需要确认且确实生效；
- [ ] Markdown、JSON 与页面已填字段一致，JSON 重新导入后可以继续编辑；
- [ ] 草稿缺项有明确提示，不会被显示为教师已验收；
- [ ] 无网络、禁用脚本或组件失败时能够使用等效学生任务单；
- [ ] 不发生默认上传或公开，本地数据范围和清除方式有说明；
- [ ] 窄屏、键盘和屏幕阅读器路径可用；
- [ ] 自动反馈不产生虚假的开源判断、成绩或社区事实。

## 当前实现挂载（v0.4）

- 在线入口：[#/activity/ACT-CH01-01](https://www.x-lab.info/AIOS101/#/activity/ACT-CH01-01)。
- 字段与流程：[learning-data.js](../../site/learning-data.js)；本地数据、迁移和导出：[learning-core.js](../../site/learning-core.js)；统一页面：[v0.4 页面实现](https://github.com/X-lab2017/AIOS101/blob/8a529d1bfc74c62995d83787823770a059059d3d/site/app.js)。
- 使用 schema 2 的 activities[活动 ID] 保存 fields、step、status、history；教学字段按本页要求映射，原建议结构不作为已经发布的数据格式。
- 自动检查只提示缺项；反馈由本人、同伴或教师填写，完成状态不等于学习评价。静态回退使用上方学生任务单。
- 实际核验范围与限制见[学习版核验记录](../../specs/history/learning-review-record.md)。
