# AI ChatBot - 自动化学生的第一个AI项目

这是一个基于 Python 和 智谱 GLM-4 API 开发的命令行聊天机器人。

## 功能特性
- 支持多轮上下文记忆（带历史记录上下文）
- 包含完整的异常处理（网络错误、空输入防呆等）
- 优雅的命令行交互体验（支持 quit 退出）

## 技术栈
- Python 3.12
- requests (网络请求)
- 智谱 BigModel API

## 如何使用
1. 克隆本仓库
2. 安装依赖：`pip install requests`
3. 在代码中填入你的 API Key
4. 运行 `python day4_api.py` 即可开始对话