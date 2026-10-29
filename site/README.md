# AIOS101 图文阅读网站

当前公开站：https://www.x-lab.info/AIOS101/ 。有效内容和未决事项见[当前状态](../docs/STATUS.md)。

## 内容与路由

教材 Markdown 是唯一正文，`scripts/build_site.py` 生成 `dist/`。序言、六章、附录与关于完整接入；后六章保留规划状态。

| 路由 | 用途 |
|---|---|
| `#/` | 前六章图文入口与序言 |
| `#/map` | 四篇十二章目录和正文检索 |
| `#/learn/PREFACE`、`CH01`—`CH06`、`APP-A`、`ABOUT` | 完整阅读、目录、字号、上下篇和来源 |
| `#/about` | 关于页别名，转到 `#/learn/ABOUT` |
| `figures/0-4.html` 等 | 当前图号的大图、缩放、来源与可用原图 |
| `review/narrow.html?chapter=PREFACE` | 320px／390px 布局核验，亦可用 `?figure=0-4` |

旧活动、工坊、手账和视觉展厅路由回退到目录或对应正文。当前产品不展示个人学习表单；只保存语言、主题和字号偏好，不触碰旧学习记录。中文正文尚无审定译本。

## 构建与发布

```bash
python scripts/check_all.py
python -m http.server 8000 --directory dist
```

Python 与 Node.js 即可完成常规检查；不需要安装图像或 PDF 生成依赖。构建使用 `GITHUB_SHA`，本地默认当前 Git HEAD，工作区未提交内容不能冒充该提交已包含的内容。

GitHub Actions 对 PR 执行检查，main 检查通过后部署 Pages；文档修改也触发检查。Pages 已设置为 GitHub Actions，沿用现有组织域名。不编辑 `dist/`，不把生成目录或个人备份提交到仓库。

当前页面仍使用 `brand.css`、`learning.css` 中的排版样式。`brand.js`、`learning-data.js`、`learning-core.js` 是历史实现／兼容参考，不进入当前部署；后两者保留独立数据回归检查。历史来源见[文档索引](../docs/history/README.md)。

构建只复制 manifest 指向的当前图版、放大源和原始截图；历史图号和生成输入留在 GitHub，不随每次部署重复分发。字体、图标和当前品牌包保留各自许可。更改品牌文件先运行品牌校验。
