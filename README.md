# WechatMD Pro

一键将 Markdown 转换为微信公众号排版的 HTML 片段，自带清新 CSS 风格。

## 动机

作为技术写作者，我经常将博客文章同步到公众号。现有工具对代码块、中英文混排、自定义主题的支持很差，手动调整排版耗时巨大。  
WechatMD Pro 利用大模型（当前基于 MiMo API）理解文章结构与语义，直接输出排版精美、可直接粘贴到公众号编辑器的 HTML 代码。

## 特性

- 支持标准 Markdown 语法（标题、列表、链接、图片、代码块、表格）
- 自动在中英文之间添加空格，规范专有名词大小写
- 代码块采用公众号友好的样式（浅灰背景、圆角、等宽字体）
- 可自定义全局主题（通过修改 system prompt 实现）
- 输出纯内联样式的 HTML，无 JS，安全粘贴

## 技术栈

- Python 3.9+
- OpenAI 兼容客户端（调用 MiMo API）
- 后续计划：封装为 VSCode 插件、提供 Web UI

## 申请大模型 Token

本项目正在申请 [小米 MiMo 大模型](https://100t.xiaomimimo.com/) 的开发者 Token，用于日常文章转换与长文本质量测试。  
如果你也有类似需求，欢迎一起参与体验。

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/wechatmd-pro.git
cd wechatmd-pro
