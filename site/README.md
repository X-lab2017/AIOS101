# AIOS101 交互学习资源 · 设计评审版

状态：v0.1.0-review。源码在 site/，正文唯一正本在 textbook/，网站规格在 specs/website-spec.md。仅供本轮设计评审，不代表课程教学验收。

## 构建

要求 Python 3；无需安装第三方 Python 或 npm 包。

```bash
python scripts/build_site.py
node --check site/app.js
python scripts/check_repo.py
```

输出目录 dist/。JavaScript 语法检查需要 Node.js；构建本身不依赖 Node.js。部署时只发布 dist/，不要将个人学习备份放入仓库。

## 页面

- #/ 首页
- #/map 课程地图与章节检索
- #/preface 完整中文序言与起点问题卡
- #/lab 五层系统探索、关系判断与修订
- #/notebook 本地学习档案与导入导出
- #/review 版本来源、规格下载与本地评审记录

核心资料只有中文正本；英文界面明确提示翻译待审。全部个人记录在当前浏览器，不上传。学习档案 JSON 不能自动跨设备同步，请主动备份。若浏览器限制文件下载，可使用“备份文本 / 从文本恢复”保存和恢复 JSON。

## GitHub Pages

工作流在 .github/workflows/course-pages.yml。首次由仓库维护者在 Settings → Pages → Build and deployment 选择 GitHub Actions。PR 只执行检查与构建，推送 main 或在 main 手动触发才部署。当前评审分支不会自动公开部署。

发布步骤：完成设计评审 → 确认发布范围和素材许可 → 合并 PR → 开通 Pages → 查看 Actions 部署结果。组织的自定义域名可能影响最终网址，以 GitHub 返回的部署 URL 为准。

Sites 使用独立的私有托管快照供维护者当前评审；GitHub 分支是规格与源码的协作入口。托管专用 .openai/ 元数据不提交到课程仓库。

## 后续接入教材

当前构建从课程规格读取十二章计划，从 textbook/preface.md 读取完整序言；不会为缺失章节生成正文。正式章节接入时，增加章节正文路径、批准状态及活动映射，再扩展构建脚本。请同步更新教材版本、来源提交、活动和翻译状态。

## 来源

品牌 SVG 来源及使用边界见 assets/NOTICE.md。OpenDipper 截图未复制到本站；系统分层和情境为概念示意。
