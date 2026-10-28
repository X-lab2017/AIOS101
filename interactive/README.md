# 交互版资源入口

本目录保存交互活动的配置、组件说明和专用资源。活动教学目标与评价要求仍以 `activities/` 中的活动规格为准。

## 编号与挂载

- 活动 ID：`ACT-CHxx-nn`；
- 学习证据：`EVD-CHxx-nn`；
- 正文通过活动目录链接接入交互，活动 ID 用于规格追踪与实现挂载；
- 一个交互可以服务多个页面，但不得建立相互冲突的任务正本。

## 设计约束

1. 交互必须产生观察、比较、核查、解释或创造，而非只提供动画；
2. 保留学习者的输入、选择、反馈和修订记录，能够导出学习证据；
3. 明确真实数据、简化模型、模拟情境和 AI 生成内容；
4. 无账号、无脚本或低性能设备下提供等效静态路径；
5. 不收集不必要的个人信息，不把公开提交设为唯一完成方式；
6. 图片、数据、代码和第三方组件分别核查许可与版本。

每项活动按 `ACT-CHxx-nn/` 建立目录，并在其中保存开发需求、配置、资源索引、测试和回退材料。教学材料与开发材料的职责如下：

- `activities/student/`：学生直接填写的任务单；
- `activities/teacher/`：教师组织、提问与评价指南；
- `activities/` 根目录：活动目标、证据和量规规格；
- `interactive/`：交互流程、字段、导出、隐私、可及性和验收要求。

第一章已建立 [ACT-CH01-01 开发需求](ACT-CH01-01/README.md)与 [ACT-CH01-02 开发需求](ACT-CH01-02/README.md)。

第二章已建立 [ACT-CH02-01 开发需求](ACT-CH02-01/README.md)与 [ACT-CH02-02 开发需求](ACT-CH02-02/README.md)。

四项活动现已实现为 v0.4 分步交互打样，使用统一字段定义、草稿保存、反馈修订和导出逻辑。教学验收与课堂实测仍待进行。

实现见 [site/learning-data.js](../site/learning-data.js)、[site/learning-core.js](../site/learning-core.js)与 [site/app.js](../site/app.js)；规格和实际核验分别见[学习体验规格](../specs/learning-experience-spec.md)与[核验记录](../specs/learning-review-record.md)。
