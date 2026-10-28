# 在线版内容入口

本目录用于后续生成《AI 开源通识》在线阅读版本，不维护第二套教材正文。

## 内容来源

- 序言：`textbook/preface.md`
- 章节正文：`textbook/chapters/CHxx-*.md`
- 章节规格：`specs/chapters/CHxx-*-spec.md`
- 视觉资产：`textbook/assets/chxx/`
- 交互活动：`interactive/`

在线构建时应保留章号、标题层级、图号、活动 ID、来源和版本信息。当前正文中的“图片占位”和“交互占位”是后续集成锚点，不应被构建脚本静默删除。

## 集成原则

1. 教材 Markdown 是唯一内容正本，网页只保存配置、组件和派生结果；
2. 图片以稳定图号接入，替换占位时不得改变正文结论；
3. 交互组件以 `ACT-CHxx-nn` 接入，并保留无脚本、静态或离线替代；
4. 来源、许可、版本和结论边界必须随内容一起发布；
5. 每次正文更新后重新检查导航、锚点、移动端阅读和交互回退。

## 当前交互学习打样 v0.4

[课程网站](https://www.x-lab.info/AIOS101/)从教材正本自动生成绪论、CH01、CH02 与附录 A 的完整阅读页；第三章新草稿也已自动接入阅读。保留来源、版本和插图占位。阅读器支持分节目录、字号、专注模式、书签和页边笔记。

源码在 [site/](../site/README.md)，生成器在 [scripts/build_site.py](../scripts/build_site.py)。[学习体验规格](../specs/learning-experience-spec.md)定义三个案例观察窗、四项分步活动与本地学习手账；任务单仍是教学正本。[核验记录](../specs/learning-review-record.md)区分工程检查与待开展的教学评审。

新章节文件进入 textbook/chapters/ 后，会在下一次构建自动生成阅读页。定制活动需要在 site/learning-data.js 中按既有 ACT/EVD ID 接入并核对学生任务单。未出现的章正文不会被补写。
