#!/usr/bin/env python3
"""
FastMCP Server for BayMax Agent - AI-Powered Stock Analysis

This server provides Model Context Protocol (MCP) tools for external applications
to access BayMax Agent's financial analysis capabilities.
"""

import os
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastmcp import FastMCP, Context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import BayMax Agent tools
from baymax.tools.prices import (
    get_current_stock_price,
    get_stock_price_history,
    get_stock_weekly_summary
)
from baymax.tools.analysis import (
    analyze_stock_with_ai,
    get_technical_indicators
)
from baymax.tools.financials import (
    get_income_statements,
    get_balance_sheets,
    get_cash_flow_statements
)
from baymax.tools.api import normalize_ticker

# Create FastMCP server
mcp = FastMCP(
    name="BayMax Agent - AI Stock Analysis",
    version="1.0.0",
    instructions="AI-powered financial analysis and stock research tools"
)

@mcp.tool()
def get_stock_price(ticker: str) -> Dict[str, Any]:
    """
    Get current stock price and basic market information.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', '600519', '1211.HK')

    Returns:
        Current price data including price, change, volume, etc.
    """
    try:
        print(f"[MCP] Getting current price for {ticker}")
        result = get_current_stock_price.func(ticker)

        # Convert to clean JSON-serializable format
        if "error" in result:
            return {
                "status": "error",
                "ticker": ticker,
                "message": result["error"],
                "timestamp": datetime.now().isoformat()
            }

        return {
            "status": "success",
            "ticker": ticker,
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker,
            "message": f"Failed to get stock price: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
def get_price_history(
    ticker: str,
    period: str = "daily",
    days_back: int = 30
) -> Dict[str, Any]:
    """
    Get historical stock price data with technical analysis.

    Args:
        ticker: Stock ticker symbol
        period: Time period ('daily', 'weekly', 'monthly')
        days_back: Number of days of historical data (default: 30)

    Returns:
        Historical price data with technical indicators and performance metrics
    """
    try:
        print(f"[MCP] Getting price history for {ticker} ({period}, {days_back} days)")
        result = get_stock_price_history.func(ticker, period=period, days_back=days_back)

        if "error" in result:
            return {
                "status": "error",
                "ticker": ticker,
                "message": result["error"],
                "timestamp": datetime.now().isoformat()
            }

        return {
            "status": "success",
            "ticker": ticker,
            "period": period,
            "days_back": days_back,
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker,
            "message": f"Failed to get price history: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
def analyze_stock(
    ticker: str,
    analysis_type: str = "comprehensive",
    include_recommendation: bool = True
) -> Dict[str, Any]:
    """
    Perform comprehensive AI-powered stock analysis.

    Args:
        ticker: Stock ticker symbol
        analysis_type: Type of analysis ('comprehensive', 'technical', 'fundamental', 'quick')
        include_recommendation: Whether to include buy/sell recommendations

    Returns:
        Complete analysis report with AI insights, recommendations, and price targets
    """
    try:
        print(f"[MCP] Analyzing {ticker} with AI ({analysis_type} analysis)")
        result = analyze_stock_with_ai.func(
            ticker,
            analysis_type=analysis_type,
            include_recommendation=include_recommendation
        )

        if "error" in result:
            return {
                "status": "error",
                "ticker": ticker,
                "message": result["error"],
                "timestamp": datetime.now().isoformat()
            }

        return {
            "status": "success",
            "ticker": ticker,
            "analysis_type": analysis_type,
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker,
            "message": f"Failed to analyze stock: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
def get_technical_analysis(
    ticker: str,
    period: str = "daily",
    days_back: int = 30
) -> Dict[str, Any]:
    """
    Get technical indicators and analysis for a stock.

    Args:
        ticker: Stock ticker symbol
        period: Time period ('daily', 'weekly', 'monthly')
        days_back: Number of days of historical data (default: 30)

    Returns:
        Technical indicators including RSI, moving averages, support/resistance levels
    """
    try:
        print(f"[MCP] Getting technical analysis for {ticker}")
        result = get_technical_indicators.func(
            ticker,
            period=period,
            days_back=days_back
        )

        if "error" in result:
            return {
                "status": "error",
                "ticker": ticker,
                "message": result["error"],
                "timestamp": datetime.now().isoformat()
            }

        return {
            "status": "success",
            "ticker": ticker,
            "period": period,
            "days_back": days_back,
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker,
            "message": f"Failed to get technical analysis: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
def get_weekly_summary(ticker: str) -> Dict[str, Any]:
    """
    Get comprehensive weekly summary for a stock.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Weekly performance summary with current price, trends, and volatility metrics
    """
    try:
        print(f"[MCP] Getting weekly summary for {ticker}")
        result = get_stock_weekly_summary.func(ticker)

        if "error" in result:
            return {
                "status": "error",
                "ticker": ticker,
                "message": result["error"],
                "timestamp": datetime.now().isoformat()
            }

        return {
            "status": "success",
            "ticker": ticker,
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker,
            "message": f"Failed to get weekly summary: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
def get_financial_statements(
    ticker: str,
    statement_type: str = "income",
    period: str = "quarterly",
    limit: int = 4
) -> Dict[str, Any]:
    """
    Get financial statements for a company.

    Args:
        ticker: Stock ticker symbol
        statement_type: Type of statement ('income', 'balance_sheet', 'cash_flow')
        period: Reporting period ('annual', 'quarterly', 'ttm')
        limit: Number of statements to retrieve (default: 4)

    Returns:
        Financial statements data with detailed metrics
    """
    try:
        print(f"[MCP] Getting {statement_type} statements for {ticker}")

        # Map statement types to functions
        statement_functions = {
            "income": get_income_statements,
            "balance_sheet": get_balance_sheets,
            "cash_flow": get_cash_flow_statements
        }

        if statement_type not in statement_functions:
            return {
                "status": "error",
                "ticker": ticker,
                "message": f"Invalid statement type. Choose from: {list(statement_functions.keys())}",
                "timestamp": datetime.now().isoformat()
            }

        func = statement_functions[statement_type]
        result = func.func(ticker, period=period, limit=limit)

        if "error" in result:
            return {
                "status": "error",
                "ticker": ticker,
                "message": result["error"],
                "timestamp": datetime.now().isoformat()
            }

        return {
            "status": "success",
            "ticker": ticker,
            "statement_type": statement_type,
            "period": period,
            "limit": limit,
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "ticker": ticker,
            "message": f"Failed to get financial statements: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@mcp.resource("config://info")
def get_server_info() -> Dict[str, Any]:
    """Get server configuration and information."""
    return {
        "name": "BayMax Agent MCP Server",
        "version": "1.0.0",
        "description": "AI-powered financial analysis and stock research",
        "supported_markets": ["A-shares", "US Stocks", "Hong Kong Stocks"],
        "features": [
            "Real-time stock prices",
            "Historical price analysis",
            "AI-powered recommendations",
            "Technical indicators",
            "Financial statements",
            "Risk assessment"
        ],
        "tools_count": 6,
        "timestamp": datetime.now().isoformat()
    }

@mcp.resource("help://usage")
def get_usage_help() -> str:
    """Get usage instructions and examples."""
    return """
# BayMax Agent MCP Server Usage

## Available Tools

1. **get_stock_price** - Get current stock price
   - Args: ticker (str)
   - Example: get_stock_price("AAPL")

2. **get_price_history** - Get historical price data
   - Args: ticker (str), period (str), days_back (int)
   - Example: get_price_history("600519", "daily", 30)

3. **analyze_stock** - AI-powered stock analysis
   - Args: ticker (str), analysis_type (str), include_recommendation (bool)
   - Example: analyze_stock("AAPL", "comprehensive", True)

4. **get_technical_analysis** - Technical indicators
   - Args: ticker (str), period (str), days_back (int)
   - Example: get_technical_analysis("MSFT", "daily", 30)

5. **get_weekly_summary** - Weekly performance summary
   - Args: ticker (str)
   - Example: get_weekly_summary("GOOGL")

6. **get_financial_statements** - Financial statements
   - Args: ticker (str), statement_type (str), period (str), limit (int)
   - Example: get_financial_statements("AAPL", "income", "quarterly", 4)

## Supported Markets
- A-shares (Chinese stocks): 600519, 600390, etc.
- US Stocks: AAPL, MSFT, GOOGL, etc.
- Hong Kong Stocks: 1211.HK, etc.

## Analysis Types
- comprehensive: Full analysis with all features
- technical: Focus on technical indicators
- fundamental: Focus on financial data
- quick: Fast analysis for immediate insights

## Statement Types
- income: Income statements
- balance_sheet: Balance sheets
- cash_flow: Cash flow statements
"""

@mcp.prompt()
def stock_analysis_prompt(ticker: str, focus_areas: Optional[str] = None) -> str:
    """
    Generate a prompt for comprehensive stock analysis.

    Args:
        ticker: Stock ticker symbol
        focus_areas: Specific areas to focus on (optional)

    Returns:
        Formatted prompt for AI analysis
    """
    base_prompt = f"""Please provide a comprehensive analysis of {ticker} stock including:

1. Current market position and recent price performance
2. Technical analysis with key indicators (RSI, moving averages, support/resistance)
3. Financial health assessment from recent statements
4. Risk evaluation and volatility analysis
5. Investment recommendation with reasoning
6. Price targets and risk-reward assessment

Use the available tools to gather all necessary data before providing insights."""

    if focus_areas:
        base_prompt += f"\n\nSpecial focus areas: {focus_areas}"

    return base_prompt

def main():
    """Run the MCP server."""
    print("🚀 Starting BayMax Agent MCP Server in HTTP mode...")
    print("📊 Available tools: stock price, historical data, AI analysis, technical indicators")
    print("🌐 HTTP endpoint: http://0.0.0.0:8000")
    print("🔧 Use any HTTP client or MCP-compatible application to connect")
    print("📖 See help resources: config://info, help://usage")

    # Run the server in HTTP mode
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()