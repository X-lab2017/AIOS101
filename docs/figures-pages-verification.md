# 前三章图文上线核验

- 图文提交：5b46d8527cd933f18b17b6fd12a1360ae8398ed6。
- 最终站点发布：ea4f347b6bb09b4f3b392d9c41f49f2d117aa74a（附发布版本缓存绑定）。
- Actions：https://github.com/X-lab2017/AIOS101/actions/runs/40702078027 ，completed / success。
- 评审入口：https://www.x-lab.info/AIOS101/?v=ea4f347#/learn/CH01 。第二、三章在同一阅读器的章节选择器中切换。

## 实际核验

公开站点三章分别含 4、4、8 个图版，16 个 WebP 的线上响应字节 SHA-256 与本地交付文件全部一致。16 张文件均成功解码，9 份独立 Mermaid 源文件与正文代码逐一一致。浏览器确认正文来源提交 ea4f347；历史插画在 720px 正文栏中以 718px 内容宽度等比显示，原图 1536px；Agent Infra 大图入口返回 2520×1718 的 WebP。结构关系折叠区经键盘 Enter 实测可展开；深色模式保留图片原色，OpenDipper 截图与相邻正文正常显示。

新增图片安全、尺寸、站内路径、下载原图链接和折叠区回归检查已进入 scripts/check_course_markdown.py，Actions 全部构建检查通过。未进行真实移动设备测试、完整屏幕阅读器审计或课堂学习效果验证；移动端依据现有响应式容器、100% 宽度和自动高度适配。正式出版第三方素材复用条件仍见 textbook/assets/figures/README.md。
