# CH04—CH06 Pages 发布后核验

- 日期：2026-10-28
- 已部署版本：`3a139976dcb92144f815e04159199f1fa193f15d`
- [Actions 构建与部署](https://github.com/X-lab2017/AIOS101/actions/runs/40719940227)：build 与 deploy 均为 completed / success。
- [本地自检记录](../specs/ch04-ch06-figures-review.md)

## 公开站点核验

[首页](https://www.x-lab.info/AIOS101/) 已显示前六章、44 幅图与六个章节入口，加载的 app.js 版本为上述部署提交。

逐个读取公开站点的 28 幅新增 WebP，并与提交时文件进行 SHA-256 比较：全部一致，总计 3,225,708 字节。公开 content.json 的 sourceCommit 与已部署版本一致。

浏览器分别检查：

| 章节 | 图数 | 默认折叠的结构源码数 | 桌面横向溢出 |
|---|---:|---:|---|
| [第四章](https://www.x-lab.info/AIOS101/#/learn/CH04) | 9 | 7 | 无 |
| [第五章](https://www.x-lab.info/AIOS101/#/learn/CH05) | 9 | 7 | 无 |
| [第六章](https://www.x-lab.info/AIOS101/#/learn/CH06) | 10 | 8 | 无 |

实际操作章节选择器与源码展开／折叠，检查第四章形成要素图、第六章文档分块及语义近邻图的在线排版。图片自然比例、大图链接、图注、侧栏与课程署名均存在。

## 验证边界

本轮完成工程与桌面在线核验；未声明真实手机、读屏器、印刷缩样或课堂教学测试完成。维护者可从上述三个章节开始视觉评审；正式出版许可与校样条件沿用[来源记录](../textbook/assets/figures/ch04-ch06-sources.md)。
