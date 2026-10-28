# 交互活动材料（暂停上线）

当前网站按维护者要求聚焦图文阅读，已撤下活动表单、笔记、已读标记与个人手账。这里保留教学设计与历史兼容材料，不能视为现行网站功能。

| 活动 | 开发需求 |
|---|---|
| ACT-CH01-01 | [使用、理解与创造](ACT-CH01-01/README.md) |
| ACT-CH01-02 | [学习问题地图](ACT-CH01-02/README.md) |
| ACT-CH02-01 | [开放与复用](ACT-CH02-01/README.md) |
| ACT-CH02-02 | [可评审贡献](ACT-CH02-02/README.md) |

活动目标与评价正本在 `activities/`，学生和教师材料分别在其子目录。旧字段定义与兼容逻辑保留于 [learning-data.js](../site/learning-data.js)、[learning-core.js](../site/learning-core.js)，并有回归检查；当前部署不加载或分发这两个脚本，当前 `app.js` 不再实现这些活动页面。

恢复交互须先确定具体学习需求，核对 ACT/EVD ID、任务单、旧记录迁移、无账号与静态替代路径，再另行实施和评审。历史实现与验证见[历史记录](../docs/history/README.md)，当前边界见[阅读体验规格](../specs/learning-experience-spec.md)。
