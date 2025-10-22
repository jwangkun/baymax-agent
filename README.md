# BayMax Agent - AI股票分析助手

<div align="center">

![BayMax Agent](https://img.shields.io/badge/BayMax-Agent-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

[![PyPI version](https://badge.fury.io/py/baymax-agent.svg)](https://badge.fury.io/py/baymax-agent)
[![Downloads](https://static.pepy.tech/badge/baymax-agent/month)](https://pepy.tech/project/baymax-agent)

**智能AI驱动的金融研究助手，专为股票分析和投资研究而设计**

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用指南](#使用指南) • [API文档](#api文档) • [贡献指南](#贡献指南)

</div>

## 📖 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [安装说明](#安装说明)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [配置说明](#配置说明)
- [API文档](#api文档)
- [开发指南](#开发指南)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [常见问题](#常见问题)

## 🌟 项目简介

BayMax Agent是一个基于大语言模型(LLM)的智能金融研究助手，专为股票分析和投资研究而设计。它能够自动获取股票市场数据，进行财务分析，并提供基于AI的投资洞察。

该项目采用模块化设计，支持多种LLM提供商，并提供了丰富的金融数据获取工具，帮助投资者做出更明智的决策。

## ✨ 功能特性

- 🔍 **智能股票分析**: 基于AI的股票市场数据分析和投资研究
- 🤖 **多模型支持**: 兼容OpenAI、Anthropic Claude、Google Gemini等多种LLM
- 📊 **全面财务数据**: 获取收入表、资产负债表、现金流量表等财务报表
- 🌍 **多市场支持**: 支持A股和美股市场数据
- 📋 **智能任务规划**: 自动分解复杂查询并规划执行步骤
- 🛠️ **丰富工具集**: 内置多种金融数据获取和分析工具
- 💬 **交互式界面**: 简洁易用的命令行交互界面
- 🔧 **灵活配置**: 支持自定义模型参数和API配置

## 🚀 安装说明

### 环境要求

- Python 3.10 或更高版本
- pip 或 uv 包管理器

### 使用pip安装

```bash
pip install baymax-agent
```

### 使用uv安装（推荐）

```bash
uv add baymax
```

### 从源码安装

```bash
git clone https://github.com/your-username/baymax-agent.git
cd baymax-agent
pip install -e .
```

## 🏃‍♂️ 快速开始

### 1. 配置环境变量

创建 `.env` 文件并添加必要的API密钥：

```bash
# LLM API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_API_KEY=your-google-api-key

# 可选：自定义模型配置
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 2. 启动BayMax Agent

```bash
baymax
```

### 3. 开始提问

```
>> 分析苹果公司(AAPL)最近的财务状况
>> 获取特斯拉(TSLA)的年度收入表
>> 比较微软(MSFT)和谷歌(GOOGL)的现金流量表
>> 获取贵州茅台(600519)的最新资产负债表
```

## 📚 使用指南

### 基本命令

```bash
# 启动交互式界面
baymax

# 查看帮助信息
baymax --help

# 查看版本信息
baymax --version
```

### 支持的查询类型

1. **财务报表查询**
   - 收入表: "获取AAPL的收入表"
   - 资产负债表: "显示MSFT的资产负债表"
   - 现金流量表: "查看TSLA的现金流量表"

2. **财务分析**
   - "分析AAPL的盈利能力"
   - "比较MSFT和GOOGL的财务状况"
   - "评估TSLA的现金流健康状况"

3. **公司信息查询**
   - "获取AAPL的基本信息"
   - "查询MSFT的业务概况"

4. **多股票对比**
   - "比较苹果和微软的财务指标"
   - "分析科技股的盈利能力排名"

## ⚙️ 配置说明

### 环境变量配置

| 变量名 | 描述 | 必需 | 示例 |
|--------|------|------|------|
| `OPENAI_API_KEY` | OpenAI API密钥 | 是 | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API密钥 | 否 | `sk-ant-...` |
| `GOOGLE_API_KEY` | Google AI API密钥 | 否 | `AI...` |
| `OPENAI_BASE_URL` | 自定义OpenAI API端点 | 否 | `https://api.openai.com/v1` |

### 模型配置

BayMax Agent支持以下模型提供商：

- **OpenAI**: GPT-4, GPT-3.5-turbo等
- **Anthropic**: Claude-3-opus, Claude-3-sonnet等
- **Google Gemini**: Gemini-pro等

### 自定义配置

您可以通过修改配置文件来自定义模型参数：

```python
# 示例配置
{
    "default_model": {
        "provider": "openai",
        "model_name": "gpt-4",
        "temperature": 0,
        "max_tokens": 4096
    }
}
```

## 📖 API文档

### 核心模块

#### Agent类

主要的代理类，负责处理用户查询和协调工具执行。

```python
from baymax.agent import Agent

agent = Agent()
result = agent.run("分析AAPL的财务状况")
```

#### Model类

统一的模型接口，支持多种LLM提供商。

```python
from baymax.model import Model

model = Model(provider="openai", api_key="your-key", model_name="gpt-4")
response = model.generate("分析AAPL的财务状况")
```

### 工具函数

#### 财务数据获取

```python
from baymax.tools.financials import get_income_statements

# 获取收入表
income_data = get_income_statements(ticker="AAPL", period="annual", limit=5)
```

#### 公司文件获取

```python
from baymax.tools.filings import get_10K_filing_items

# 获取10K文件
filing_data = get_10K_filing_items(ticker="AAPL", limit=3)
```

## 🛠️ 开发指南

### 项目结构

```
baymax-agent/
├── src/
│   └── baymax/
│       ├── __init__.py          # 包初始化
│       ├── agent.py             # 主代理类
│       ├── cli.py               # 命令行接口
│       ├── model.py             # 模型接口
│       ├── model_manager.py     # 模型管理器
│       ├── prompts.py           # 提示词模板
│       ├── schemas.py           # 数据模型
│       ├── tools/               # 工具模块
│       │   ├── __init__.py
│       │   ├── api.py           # API工具
│       │   ├── constants.py     # 常量定义
│       │   ├── filings.py       # 文件工具
│       │   └── financials.py    # 财务工具
│       └── utils/               # 工具函数
│           ├── intro.py         # 介绍信息
│           ├── logger.py        # 日志工具
│           └── ui.py            # UI工具
├── tests/                       # 测试文件
├── docs/                        # 文档
├── pyproject.toml               # 项目配置
└── README.md                    # 项目说明
```

### 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/your-username/baymax-agent.git
cd baymax-agent
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装开发依赖
```bash
pip install -e ".[dev]"
```

4. 运行测试
```bash
pytest
```

### 添加新工具

1. 在 `src/baymax/tools/` 目录下创建新工具文件
2. 实现工具函数，遵循现有工具的接口规范
3. 在 `src/baymax/tools/__init__.py` 中导入并添加到 `TOOLS` 列表
4. 编写相应的测试用例

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 贡献流程

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 代码规范

- 使用 PEP 8 代码风格
- 添加适当的文档字符串
- 为新功能编写测试用例
- 确保所有测试通过

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ❓ 常见问题

### Q: 如何切换不同的LLM模型？

A: 您可以通过设置环境变量或在代码中指定模型提供商来切换不同的LLM模型。详细配置请参考[配置说明](#配置说明)部分。

### Q: 支持哪些股票市场？

A: 目前支持A股（中国股市）和美股（美国股市）的股票数据。A股使用6位数字代码（如000001），美股使用股票代码（如AAPL）。

### Q: 如何获取API密钥？

A: 
- OpenAI API密钥: 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
- Anthropic API密钥: 访问 [Anthropic Console](https://console.anthropic.com/)
- Google AI API密钥: 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)

### Q: 数据更新频率如何？

A: 财务数据通常每季度更新一次，股价数据每日更新。具体更新频率取决于数据源。

### Q: 如何报告问题或请求新功能？

A: 您可以在 [Issues](https://github.com/your-username/baymax-agent/issues) 页面报告问题或请求新功能。

## 🙏 致谢

- [AkShare](https://github.com/akfamily/akshare) - 提供金融数据接口
- [LangChain](https://github.com/langchain-ai/langchain) - 提供LLM集成框架
- [OpenAI](https://openai.com/) - 提供强大的语言模型
- [Anthropic](https://anthropic.com/) - 提供Claude系列模型
- [Google](https://ai.google.dev/) - 提供Gemini模型

## 📞 联系我们

- 项目主页: [https://github.com/your-username/baymax-agent](https://github.com/your-username/baymax-agent)
- 问题反馈: [Issues](https://github.com/your-username/baymax-agent/issues)
- 邮箱: contact@baymax-stock-agent.com

---

<div align="center">

**如果这个项目对您有帮助，请给我们一个 ⭐️**

Made with ❤️ by BayMax Stock Agent Team

</div>