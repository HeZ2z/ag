# AG - 智能 AI 命令行助手

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

AG 是一个功能强大的 AI 命令行工具，支持文本对话和图像分析，兼容所有 OpenAI 接口规范的模型服务。通过简单的命令行界面，让您随时随地与 AI 交流，分析图像，提高工作效率。

![Demo Screenshot](test.png)

## ✨ 核心功能

- 🤖 **智能对话**：与 AI 进行自然流畅的文本对话
- 📸 **图像分析**：快速截取屏幕或分析指定图片，获取 AI 智能描述
- 🔄 **多模式交互**：支持单次命令和交互式对话模式
- 🌐 **广泛兼容**：兼容 OpenAI、通义千问等支持 OpenAI 接口规范的服务
- ⚙️ **灵活配置**：通过环境变量和配置文件轻松定制

## 🚀 快速开始

### 安装

```shell
# 克隆仓库
git clone https://github.com/yourusername/ag.git
cd ag

# 安装依赖
pip install -e .
```

### 环境配置

1. 创建环境变量配置文件：

   ```shell
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入您的 API 信息：

   ```plaintext
   MODEL="gpt-3.5-turbo"       # 使用的模型
   BASE_URL="https://api.openai.com/v1"  # API 基础 URL
   API_KEY="your_api_key_here" # API 密钥
   ```

## 💡 使用指南

### 基本命令

```shell
# 查看帮助信息
ag --help

# 文本对话
ag -t "请介绍一下自己"

# 分析屏幕截图
ag -i

# 分析指定图片
ag -p /path/to/image.png

# 带提示词的图像分析
ag -t "描述这张图片中的主要内容" -i

# 自定义系统提示词
ag --prompt "你是一个医学专家" -t "头痛可能是什么原因导致的？"

# 进入交互式对话模式
ag
```

### 命令行选项

| 选项 | 说明 |
|------|------|
| `-t, --text TEXT` | 向 AI 发送的文本提示 |
| `-i, --image` | 分析屏幕截图 |
| `-p, --path PATH` | 指定要分析的图片路径 |
| `--prompt TEXT` | 自定义系统提示词 |
| `--start TEXT` | 自定义交互模式的开场白 |
| `-h, --help` | 显示帮助信息 |

## 🔧 项目结构

```text
ag/
├── main.py            # 主入口点
├── pyproject.toml     # 项目配置和依赖管理
├── README.md          # 项目文档
└── src/               # 源代码目录
    ├── cli/           # 命令行接口
    │   └── commands.py # 命令行命令实现
    ├── models/        # AI 模型客户端
    │   └── client.py  # OpenAI 兼容客户端
    └── utils/         # 工具函数
        └── screenshot.py # 屏幕截图工具
```

## 🔍 技术特点

- **模块化设计**：清晰的代码结构，易于扩展和维护
- **统一客户端**：封装 OpenAI 客户端，提供一致的接口
- **流式响应**：支持 AI 回答的流式输出，提供更好的用户体验
- **错误处理**：全面的异常捕获和错误提示
- **Python 类型提示**：严格的类型注解，提高代码可读性和可维护性

## 📚 参考资源

- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [通义千问 OpenAI 兼容接口](https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api)

## 📄 许可证

[MIT](LICENSE) © [HeZzz](mailto:hez2z@foxmail.com)
