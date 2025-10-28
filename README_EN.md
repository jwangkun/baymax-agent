# BayMax Agent - AI-Powered Stock Analysis Assistant

<div align="center">

![BayMax Agent](https://img.shields.io/badge/BayMax-Agent-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

[![PyPI version](https://badge.fury.io/py/baymax-agent.svg)](https://badge.fury.io/py/baymax-agent)
[![Downloads](https://static.pepy.tech/badge/baymax-agent/month)](https://pepy.tech/project/baymax-agent)

**An intelligent AI-driven financial research assistant designed for stock analysis and investment research**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage Guide](#-usage-guide) • [MCP Integration](#-mcp-integration) • [API Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [🏃‍♂️ Quick Start](#-quick-start)
- [📚 Usage Guide](#-usage-guide)
- [⚙️ Configuration](#️configuration)
- [📊 Data Sources & Limitations](#-data-sources--limitations)
- [🔌 MCP Integration](#-mcp-integration)
- [📖 API Documentation](#-api-documentation)
- [🛠️ Development Guide](#-development-guide)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [❓ FAQ](#-faq)

## 🌟 Project Overview

BayMax Agent is an intelligent financial research assistant powered by Large Language Models (LLMs), specifically designed for stock analysis and investment research. It automatically retrieves stock market data, performs financial analysis, and provides AI-driven investment insights to help investors efficiently obtain valuable investment references in an information-overloaded market environment.

Key Advantages:
- **Automated Data Analysis**: Automatically acquires, processes, and analyzes massive financial data
- **Intelligent Insight Generation**: Provides in-depth analysis and investment recommendations based on LLM technology
- **Multi-Market Coverage**: Simultaneously supports A-share and US stock market analysis
- **Flexible and Extensible**: Modular design, easy to integrate new data sources and analysis tools
- **DeepSeek Model Integration**: Based on DeepSeek AI model, providing high-quality financial analysis capabilities

Whether you are an individual investor, financial analyst, or researcher, BayMax Agent can be a powerful assistant in your investment decision-making process.

## ✨ Features

- 🔍 **Intelligent Stock Analysis**: Advanced LLM-based deep market data analysis and investment research, providing professional-grade analysis reports
- 🤖 **DeepSeek Model Support**: Based on DeepSeek model providing AI analysis capabilities with OpenAI-compatible interface
- 📊 **Comprehensive Financial Data**: Retrieves core financial statements including income statements, balance sheets, cash flow statements, with multi-year comparative analysis support
- 🌍 **Multi-Market Support**: Seamlessly supports A-share and US stock market data, providing unified analysis experience
- 📋 **Intelligent Task Planning**: Automatically decomposes complex queries, plans execution steps, and solves complex analysis tasks involving multiple data sources
- 🛠️ **Rich Toolset**: Built-in professional tools for financial data acquisition, company document analysis, fundamental evaluation, and more
- 💬 **Interactive Interface**: Simple and intuitive command-line interactive interface, supporting natural language queries and context understanding
- 🔧 **Flexible Configuration**: Supports custom model parameters, API configurations, and analysis preferences
- 📈 **Technical Indicator Analysis**: Provides common technical indicator calculations and trend analysis
- 📝 **Intelligent Report Generation**: Automatically generates structured analysis reports with key findings and investment recommendations
- 🔒 **Data Security**: Local processing of sensitive data, supports environment variable management for API keys

## 🚀 Installation

### Environment Requirements

- Python 3.10 or higher
- pip or uv package manager
- Network connection (for API calls and data retrieval)

### Using pip

```bash
pip install baymax-agent
```

### Using uv (Recommended)

uv is a modern Python package manager that provides faster installation speeds and better dependency resolution:

```bash
uv add baymax-agent
```

Note: If you encounter errors when running this command in the project directory due to the project name conflicting with the dependency name, use one of the following commands:

1. For development environment installation:
   ```bash
   uv add --dev baymax-agent
   ```

2. If you just want to install project dependencies:
   ```bash
   uv sync
   ```

3. If you want to use baymax in a new project:
   ```bash
   cd /path/to/your/project
   uv add baymax-agent
   ```

### Install from Source

```bash
git clone https://github.com/jwangkun/baymax-agent.git
cd baymax-agent
pip install -e .
```

### Installation Verification

After installation, you can verify the installation was successful by running:

```bash
baymax --version
```

## 🏃‍♂️ Quick Start

### 1. Configure Environment Variables

Create a `.env` file and add the necessary API keys (at least one LLM provider API key is required):

```bash
# Copy the example configuration file
cp env.example .env
```

Edit the `.env` file and add the necessary API keys:

```bash
# LLM API Keys (configure at least one)
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_API_KEY=your-google-api-key

# Optional: Custom model configuration
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 2. Start BayMax Agent

```bash
baymax
```

### 3. Start Asking Questions

```
>> Analyze Apple Inc. (AAPL) recent financial condition and future growth potential
>> Get Tesla (TSLA) income statements for the past 5 years and analyze revenue growth trends
>> Compare Microsoft (MSFT) and Google (GOOGL) cash flow statements to evaluate their cash flow health
>> Get Kweichow Moutai (600519) latest balance sheet, focusing on debt ratio and cash flow
>> Analyze main financial indicators comparison of leading tech stocks
```

### Example Analysis Report

When you ask a question, BayMax Agent will automatically retrieve relevant data and generate an analysis report, for example:

```
Analysis of Apple Inc. (AAPL) recent financial condition:

1. Revenue Performance:
   - Latest quarter total revenue: $123.0 billion, up 15% year-over-year
   - Product revenue: $98.0 billion, Service revenue: $25.0 billion
   - Service business growing rapidly, up 23% year-over-year

2. Profitability:
   - Gross margin: 42.3%, up 1.2 percentage points year-over-year
   - Net profit margin: 28.5%, showing strong profitability
   - Earnings per share (EPS): $2.15, up 18% year-over-year

3. Balance Sheet Condition:
   - Total assets: $350.0 billion
   - Cash and equivalents: $20.5 billion
   - Total liabilities: $190.0 billion
   - Debt ratio: 54.3%

4. Cash Flow Situation:
   - Operating cash flow: $87.5 billion/year
   - Free cash flow: $76.0 billion/year
   - Dividend payments: $14.5 billion/year
   - Stock buybacks: $85.0 billion/year

5. Investment Recommendation:
   - Apple shows solid financial condition and sustained growth capability
   - Rapid growth of service business provides new growth points
   - Strong cash flow supports continuous shareholder return programs
   - Recommend monitoring impact of upcoming new product cycles on revenue
```

## 📚 Usage Guide

### Basic Commands

```bash
# Start interactive interface
baymax

# View help information
baymax --help

# Check version
baymax --version
```

### Advanced Usage

```bash
# Run with custom configuration
baymax --config custom_config.json

# Run in quiet mode (reduced output)
baymax --quiet

# Run with debug mode (detailed logging)
baymax --debug
```

### Query Examples

#### Financial Analysis
- "Analyze Apple's profitability trends over the past 3 years"
- "Compare revenue growth between Tesla and traditional automakers"
- "Evaluate Microsoft's cash flow stability and capital allocation efficiency"

#### Technical Analysis
- "What are the current technical indicators for Google stock?"
- "Analyze recent price trends and support/resistance levels for Amazon"
- "Calculate volatility and risk metrics for Netflix stock"

#### Market Comparison
- "Compare valuation metrics between major tech companies"
- "Analyze financial health differences between growth and value stocks"
- "Which semiconductor companies show the strongest balance sheets?"

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root directory:

```bash
# DeepSeek API Key (required)
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

# Optional: Model configuration
DEFAULT_MODEL=deepseek
MAX_TOKENS=4000
TEMPERATURE=0.7
```

### Configuration File

You can also create a `config.json` file for advanced configuration:

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4",
    "max_tokens": 4000,
    "temperature": 0.7
  },
  "data_sources": {
    "financial_data": "akshare",
    "news_data": "optional_source"
  },
  "analysis": {
    "default_period": "quarterly",
    "historical_years": 5
  }
}
```

## 📊 Data Sources & Limitations

### Data Sources
BayMax Agent uses free data sources for stock analysis, primarily relying on:

- **AkShare**: Free open-source financial data interface library
  - Provides A-shares, US stocks, Hong Kong stocks market data
  - Data sources include Sina Finance, Tencent Finance, East Money
  - No API key required for access
  - Data update frequency and stability depend on source websites

### Important Limitations ⚠️

1. **Data Quality**:
   - Uses free data sources, data accuracy depends on third-party websites
   - May have delays, missing data, or errors
   - Recommend cross-validation with official data sources for important decisions

2. **Network Dependency**:
   - Requires stable network connection to access data sources
   - Some data sources may have access frequency limits
   - Network issues may cause data retrieval failures

3. **Real-time Capability**:
   - Not professional real-time market data
   - Stock price data may have 15-20 minute delays
   - Financial data updated according to official release cycles

4. **Coverage Scope**:
   - Mainly covers A-shares and US stock markets
   - Hong Kong stock market support is limited
   - Other international markets not currently supported

5. **AI Model Limitations**:
   - Currently only supports DeepSeek model
   - Analysis results are AI model-based and for reference only
   - Does not constitute investment advice

## 🔌 MCP (Model Context Protocol) Integration

BayMax Agent now supports the Model Context Protocol (MCP), allowing external applications and AI assistants to access its financial analysis capabilities through a standardized HTTP interface.

### 🚀 Starting the MCP Server

#### Prerequisites
Ensure required dependencies are installed:
```bash
pip install fastmcp
```

#### Startup Steps
1. **Configure environment variables** (if not already configured):
```bash
export DEEPSEEK_API_KEY=your-api-key
```

2. **Start the MCP server**:
```bash
python mcp_server.py
```

3. **Verify successful startup**:
After starting, you should see:
```
🚀 Starting BayMax Agent MCP Server in HTTP mode...
🌐 HTTP endpoint: http://0.0.0.0:8000
📦 Transport: HTTP
🔗 Server URL: http://0.0.0.0:8000/mcp
```

#### Server Features
- **Transport**: HTTP with Server-Sent Events (SSE)
- **Endpoint**: `http://localhost:8000/mcp`
- **Protocol**: Model Context Protocol (MCP)
- **Concurrency**: Supports multiple simultaneous client connections

#### Connection Testing
After starting, you can test with:
```bash
# Test server status
curl -N -H "Accept: text/event-stream" http://localhost:8000/mcp

# If SSE format data is returned, server is running normally
```

### 🛠️ Available MCP Tools

The MCP server exposes 6 financial analysis tools:

#### 1. **get_stock_price**
Get current stock price and market information
```json
{
  "tool": "get_stock_price",
  "arguments": {
    "ticker": "AAPL"
  }
}
```

#### 2. **get_price_history**
Retrieve historical price data with technical analysis
```json
{
  "tool": "get_price_history",
  "arguments": {
    "ticker": "AAPL",
    "period": "daily",
    "days_back": 30
  }
}
```

#### 3. **analyze_stock**
AI-powered comprehensive stock analysis with buy/sell recommendations
```json
{
  "tool": "analyze_stock",
  "arguments": {
    "ticker": "AAPL",
    "analysis_type": "comprehensive",
    "include_recommendation": true
  }
}
```

#### 4. **get_technical_analysis**
Technical indicators and analysis (RSI, moving averages, support/resistance)
```json
{
  "tool": "get_technical_analysis",
  "arguments": {
    "ticker": "AAPL",
    "period": "daily",
    "days_back": 30
  }
}
```

#### 5. **get_weekly_summary**
Weekly performance summary with volatility metrics
```json
{
  "tool": "get_weekly_summary",
  "arguments": {
    "ticker": "AAPL"
  }
}
```

#### 6. **get_financial_statements**
Financial statements (income, balance sheet, cash flow)
```json
{
  "tool": "get_financial_statements",
  "arguments": {
    "ticker": "AAPL",
    "statement_type": "income",
    "period": "quarterly",
    "limit": 4
  }
}
```

### 🔗 Integration Examples

#### Using with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "baymax-agent": {
      "url": "http://localhost:8000/mcp",
      "transport": "http"
    }
  }
}
```

#### Using with Cursor

Add to your Cursor MCP settings:

```json
{
  "name": "BayMax Agent",
  "url": "http://localhost:8000/mcp",
  "type": "http"
}
```

#### Direct HTTP API Usage

You can also interact with the MCP server directly using HTTP requests:

```bash
# Get server information
curl -N -H "Accept: text/event-stream" http://localhost:8000/mcp

# Call a tool (requires MCP protocol formatting)
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "get_stock_price",
      "arguments": {
        "ticker": "AAPL"
      }
    }
  }'
```

### 📋 Supported Markets

- **A-shares**: Chinese stocks (e.g., 600519, 000001)
- **US Stocks**: American stocks (e.g., AAPL, MSFT, GOOGL)
- **Hong Kong Stocks**: HK stocks (e.g., 1211.HK)

### ⚠️ Important Notes

- **Network Requirements**: The MCP server requires internet access for real-time financial data
- **Rate Limiting**: Be mindful of API rate limits when making frequent requests
- **Data Accuracy**: Financial data is sourced from multiple providers with fallback mechanisms
- **Error Handling**: The server includes comprehensive error handling for network issues

### 🔧 Configuration & Troubleshooting

#### Environment Configuration
The MCP server supports environment variables for configuration:

```bash
# Optional: Set log level
export BAYMAX_LOG_LEVEL=INFO

# Optional: Set default model for AI analysis
export BAYMAX_DEFAULT_MODEL=deepseek

# Optional: Set API timeout
export BAYMAX_REQUEST_TIMEOUT=30
```

#### Common Issues & Solutions

**Issue 1: Server fails to start**
```bash
# Error: ModuleNotFoundError: No module named 'fastmcp'
# Solution:
pip install fastmcp
```

**Issue 2: API call failures**
```bash
# Error: DeepSeek API error
# Solutions:
# 1. Check if API key is correct
# 2. Check network connection
# 3. Verify API quota is not exhausted
```

**Issue 3: Data retrieval failures**
```bash
# Error: Network error: US price fetch failed
# Solutions:
# 1. Check network connection
# 2. Wait for network recovery and retry
# 3. Try alternative data sources
```

**Issue 4: MCP client connection failures**
```bash
# Error: Connection refused
# Solutions:
# 1. Confirm server is running
# 2. Check port number is correct (8000)
# 3. Check firewall settings
```

#### Performance Optimization Tips

1. **Caching**: Same queries are cached to reduce API calls
2. **Batch queries**: Get data in batches to reduce network requests
3. **Error retry**: Network failures automatically retry up to 2 times
4. **Timeout settings**: Set reasonable timeout to avoid long waits

## 📖 API Documentation

### Core Functions

#### `get_current_stock_price(ticker: str) -> dict`

Fetches current stock price and basic market information.

**Parameters:**
- `ticker`: Stock ticker symbol (e.g., 'AAPL', '600519')

**Returns:** Dictionary containing price data, change information, volume, etc.

#### `get_stock_price_history(ticker: str, period: str, days_back: int) -> dict`

Retrieves historical stock price data.

**Parameters:**
- `ticker`: Stock ticker symbol
- `period`: Time period ('daily', 'weekly', 'monthly')
- `days_back`: Number of days of historical data

**Returns:** Dictionary containing price history, technical indicators, and performance metrics

#### `analyze_stock_with_ai(ticker: str, analysis_type: str, include_recommendation: bool) -> dict`

Performs comprehensive AI-powered stock analysis.

**Parameters:**
- `ticker`: Stock ticker symbol
- `analysis_type`: Type of analysis ('comprehensive', 'technical', 'fundamental', 'quick')
- `include_recommendation`: Whether to include buy/sell recommendations

**Returns:** Complete analysis report with AI insights, recommendations, and price targets

### Data Models

#### StockPriceData
```python
{
    "ticker": str,
    "current_price": float,
    "change": float,
    "change_percent": float,
    "volume": int,
    "high": float,
    "low": float,
    "open": float,
    "previous_close": float,
    "market_time": str,
    "data_source": str
}
```

#### AIAnalysisResult
```python
{
    "ticker": str,
    "analysis_date": str,
    "analysis_type": str,
    "recommendation": {
        "action": str,  # 'BUY', 'SELL', 'HOLD'
        "urgency": str,  # 'STRONG', 'MODERATE', 'NEUTRAL'
        "reasoning": List[str],
        "confidence_score": int
    },
    "price_targets": {
        "upside_target": float,
        "downside_target": float,
        "risk_reward_ratio": float
    },
    "technical_analysis": dict,
    "risk_assessment": dict
}
```

## 🛠️ Development Guide

### Project Structure

```
baymax-agent/
├── src/baymax/                    # Main source code
│   ├── __init__.py               # Package initialization
│   ├── agent.py                  # Core agent logic
│   ├── cli.py                    # Command-line interface
│   ├── model.py                  # LLM model interface
│   ├── model_manager.py          # Model management
│   ├── prompts.py                # LLM prompt templates
│   ├── schemas.py                # Data models
│   ├── tools/                    # Financial analysis tools
│   │   ├── __init__.py          # Tool registry
│   │   ├── api.py               # API utilities
│   │   ├── prices.py            # Price data tools
│   │   ├── analysis.py          # AI analysis tools
│   │   ├── financials.py        # Financial statement tools
│   │   └── filings.py           # SEC filings tools
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── intro.py             # Welcome messages
│       ├── logger.py            # Logging utilities
│       └── ui.py                # UI/display utilities
├── tests/                        # Test files
├── docs/                         # Documentation
├── examples/                     # Usage examples
└── requirements.txt              # Dependencies
```

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jwangkun/baymax-agent.git
   cd baymax-agent
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env file with your API keys
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=src/baymax tests/
```

### Adding New Tools

1. Create your tool in the appropriate module under `src/baymax/tools/`
2. Use the `@tool` decorator from LangChain
3. Define input schema using Pydantic models
4. Register the tool in `src/baymax/tools/__init__.py`

Example:
```python
from langchain.tools import tool
from pydantic import BaseModel

class MyToolInput(BaseModel):
    param: str

@tool(args_schema=MyToolInput)
def my_new_tool(param: str) -> dict:
    """Tool description"""
    # Implementation here
    return {"result": "success"}
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: Submit issues for any bugs you find
- 💡 **Suggest Features**: Propose new features or improvements
- 📝 **Improve Documentation**: Help improve docs and examples
- 🔧 **Submit Code**: Contribute bug fixes or new features
- 🌍 **Translations**: Help translate documentation

### Contribution Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes and test them**
4. **Commit with clear messages**: `git commit -m "Add amazing feature"`
5. **Push to your branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Write tests for new features
- Keep functions focused and modular

### Commit Message Guidelines

Use clear, descriptive commit messages:
- `feat: add new stock screening tool`
- `fix: resolve timeout issue in price fetching`
- `docs: update API documentation`
- `test: add unit tests for analysis module`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ❓ FAQ

### Q: What markets does BayMax Agent support?
A: Currently supports A-shares (Chinese stocks) and US stocks. Hong Kong stocks have partial support with some network limitations.

### Q: Which LLM providers are supported?
A: Currently, only DeepSeek models are supported. The system uses DeepSeek's API with OpenAI-compatible interface for high-quality financial analysis.

### Q: Is real-time data guaranteed?
A: The system tries multiple data sources with fallback mechanisms, but network issues may affect real-time data availability. Historical data is generally more reliable.

### Q: How accurate are the AI recommendations?
A: AI recommendations are based on financial data analysis and should be used as reference only. Always conduct your own research and consider multiple sources before making investment decisions.

### Q: Can I use this for commercial purposes?
A: Yes, under the MIT license, but please review the license terms and consider the disclaimer about investment advice.

### Q: How do I handle network connectivity issues?
A: The system includes robust error handling and fallback mechanisms. If you encounter persistent issues, check your network configuration and try different data sources.

---

## ⚠️ Disclaimer

**Important**: BayMax Agent is a research tool for educational and informational purposes only. It does not constitute financial advice, investment recommendations, or professional consulting. Always consult with qualified financial advisors before making investment decisions. Past performance does not guarantee future results.

**Risk Warning**: Stock investment involves risks, including possible loss of principal. The AI analysis and recommendations provided by this tool are based on historical data and statistical models, which may not predict future market behavior accurately.

---

<div align="center">

**[⬆ Back to Top](#-table-of-contents)**

Made with ❤️ by the BayMax Agent Team

</div>