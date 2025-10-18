# BayMax Stock Agent 🤖📈

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)

**BayMax Stock Agent** 是一个智能的股票研究代理，专为投资者和金融分析师设计。它利用人工智能技术进行深度财务分析、实时市场数据获取和投资决策支持。

## 🌟 核心特性

- **🤖 AI驱动的分析**: 使用先进的语言模型进行智能财务分析
- **📊 实时市场数据**: 集成多个金融数据源，提供实时股票信息
- **🔍 深度研究报告**: 自动生成详细的股票分析报告
- **💡 投资建议**: 基于数据分析提供投资建议和风险评估
- **🌐 多市场支持**: 支持全球主要股票市场的数据获取
- **⚡ 高性能**: 异步处理，快速响应用户查询

## 🚀 快速开始

### 前置要求

- Python 3.10 或更高版本
- Node.js 16.0 或更高版本
- OpenAI API 密钥

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-username/baymax-stock-agent.git
   cd baymax-stock-agent
   ```

2. **安装依赖**
   ```bash
   # 安装Node.js依赖
   npm install
   
   # 安装Python依赖
   pip install -e .
   ```

3. **配置环境变量**
   ```bash
   cp env.example .env
   # 编辑 .env 文件，添加你的API密钥
   ```

4. **运行应用**
   ```bash
   # 使用npm
   npm start
   
   # 或者直接运行
   baymax
   ```

## 📖 使用方法

### 基本命令

```bash
# 分析特定股票
baymax analyze AAPL

# 获取市场概览
baymax market-overview

# 生成研究报告
baymax report TSLA --detailed

# 交互式模式
baymax interactive
```

### Python API

```python
from baymax_stock_agent import StockAgent

# 初始化代理
agent = StockAgent()

# 分析股票
result = agent.analyze_stock("AAPL")
print(result)

# 获取财务数据
financials = agent.get_financial_data("TSLA")
print(financials)
```

## 🛠️ 技术架构

### 核心组件

- **AI引擎**: 基于OpenAI GPT模型进行智能分析
- **数据层**: 集成AkShare、Yahoo Finance等多个数据源
- **分析引擎**: 专业的财务指标计算和分析算法
- **API接口**: RESTful API支持各种客户端集成

### 项目结构

```
baymax-stock-agent/
├── src/
│   └── dexter/
│       ├── agent.py          # 核心代理逻辑
│       ├── cli.py           # 命令行接口
│       ├── model.py         # 数据模型
│       ├── prompts.py       # AI提示模板
│       ├── schemas.py       # 数据架构
│       └── tools/           # 工具模块
│           ├── api.py       # API接口
│           ├── financials.py # 财务分析工具
│           └── filings.py   # 财报处理工具
├── package.json             # Node.js配置
├── pyproject.toml          # Python项目配置
└── README.md               # 项目文档
```

## 📊 支持的功能

### 股票分析
- [x] 实时股价查询
- [x] 历史价格分析
- [x] 技术指标计算
- [x] 财务比率分析
- [x] 估值模型
- [x] 风险评估

### 市场数据
- [x] 全球市场数据
- [x] 行业对比分析
- [x] 市场情绪指标
- [x] 新闻情绪分析

### 报告生成
- [x] 自动化研究报告
- [x] 可视化图表
- [x] PDF导出功能
- [x] 自定义报告模板

## 🔧 配置选项

### 环境变量

```bash
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4

# 数据源配置
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
YAHOO_FINANCE_ENABLED=true

# 数据库配置（可选）
DATABASE_URL=sqlite:///baymax.db

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/baymax.log
```

### 高级配置

可以在配置文件中设置更多高级选项，如分析参数、数据源优先级、缓存设置等。

## 🤝 贡献指南

我们欢迎社区贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解如何参与项目开发。

### 开发环境设置

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码质量检查
ruff check .
black .
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [OpenAI](https://openai.com/) - 提供强大的AI模型
- [AkShare](https://github.com/akfamily/akshare) - 开源金融数据接口
- [LangChain](https://langchain.com/) - AI应用开发框架

## 📞 支持与联系

- **问题反馈**: [GitHub Issues](https://github.com/your-username/baymax-stock-agent/issues)
- **功能请求**: [GitHub Discussions](https://github.com/your-username/baymax-stock-agent/discussions)
- **邮件联系**: contact@baymax-stock-agent.com

## ⚠️ 免责声明

**重要提示**: BayMax Stock Agent 仅供教育和研究目的使用。所有投资建议仅供参考，不构成实际投资建议。投资有风险，入市需谨慎。请始终进行自己的研究并咨询专业的财务顾问。

---

**Made with ❤️ by the BayMax Stock Agent Team**