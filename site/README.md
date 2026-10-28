# AIOS101 交互学习资源

状态：v0.4.0-learning-preview，维护者授权上线打样；教学验收、课堂效果和真实设备实测待评审。[公开网站](https://www.x-lab.info/AIOS101/)。

## 内容与实现

教材唯一正本在 textbook/，学生任务单在 activities/student/。构建生成完整阅读内容，不另行维护网页正文。全局范围见[网站规格](../specs/website-spec.md)，学习流程和验收依据见[学习体验规格](../specs/learning-experience-spec.md)。

| 路由 | 用途 |
|---|---|
| #/ | 学习首页、继续上次阅读或活动 |
| #/map | 十二章地图、全文关键词检索、待上线状态 |
| #/learn/PREFACE、CH01、CH02、APP-A | 完整阅读、分节书签、已读标记、页边笔记 |
| #/explore/system、materials、collaboration | 系统展开、DeepSeek-R1 材料、AIInfra 两条独立协作记录 |
| #/workshop | 三项观察和四项活动的入口 |
| #/activity/ACT-CH01-01 等 | 原任务单的分步填写、人工反馈和修订 |
| #/notebook | 个人笔记、活动产物、备份恢复、打印 |
| #/resources | 术语、固定来源、版本和附录 |
| #/identity | 已批准视觉基线与素材包 |

旧 #/preface、#/lab、#/review 路由保留重定向。核心界面有中英文与明暗主题；教材、任务单及中文案例解释尚未提供审定译本。

## 开发与检查

只需 Python 3 与 Node.js，无第三方构建依赖：

```bash
python scripts/build_site.py
node --check site/app.js
node --check site/brand.js
node --check site/learning-data.js
node --check site/learning-core.js
node scripts/check_learning.js
python scripts/check_course_markdown.py
python scripts/check_site.py
python scripts/check_repo.py
python scripts/package_course_brand.py --check
```

dist/ 为生成目录。正文更新触发 GitHub Actions 重建；GITHUB_SHA 用于固定来源链接，本地默认绑定本轮教材快照。不要提交 dist/ 或个人学习备份。四项活动定义集中在 learning-data.js，修改时必须核对对应任务单，运行数据逻辑检查并补充浏览器核验。

## 本地学习记录

浏览器存储使用 aios101.learning.v2，按活动 ID 保存字段、步骤和最多 20 次主动修订快照。旧版 v1 起点、探索和评审记录迁移并保留原文；旧存储键不删除。长篇旧探索原文在历史记录中完整保留，新编辑区最多显示前 6000 字符。

不上传个人学习文字，不提供云同步。JSON 备份导入先验证，再确认合并；保留导入前备份与被替换活动的原稿。当前导入限 2 MB；超限文件不会覆盖现有数据。Markdown 导出包含全部活动字段、缺项、反馈、修订历史和来源。浏览器限制下载时，可用文本备份与恢复；活动全文也可从预览窗复制。

首次加载需网络；下载的 Markdown 任务单可离线使用，完整网站离线缓存未实现。填写确认不等于成绩或教学验收。

## 发布与视觉

.github/workflows/course-pages.yml 在 PR 执行检查，main 更新通过后部署 GitHub Pages。Settings → Pages 已使用 GitHub Actions，沿用组织域名。Sites 另保留维护者私有预览，受众不变；托管专用 .openai/ 元数据不提交到课程仓库。

课程视觉沿用 [VIS-AIOS101 v1.0.0](../brand/README.md)，冻结资产与版本包未修改。资产来源见 [NOTICE](assets/NOTICE.md)。字体和图标本地托管。新交互全部以 HTML/CSS 表达，不加入第三方运行依赖；概念示意不替代教材正式插图。

实际执行与未验证项见[学习版核验记录](../specs/learning-review-record.md)。
