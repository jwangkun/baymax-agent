#!/usr/bin/env python3
"""
Test script for BayMax Agent MCP Server
This script tests all the MCP tools to ensure they work correctly.
"""

import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the MCP tools directly for testing
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

def test_stock_price():
    """Test current stock price retrieval"""
    print("🔄 Testing get_current_stock_price...")
    try:
        result = get_current_stock_price.func("AAPL")
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        else:
            print(f"✅ Success: AAPL current price: ${result.get('current_price', 'N/A')}")
            return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_price_history():
    """Test historical price data"""
    print("\n🔄 Testing get_stock_price_history...")
    try:
        result = get_stock_price_history.func("AAPL", period="daily", days_back=7)
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        else:
            print(f"✅ Success: Retrieved {len(result.get('historical_data', []))} days of historical data")
            return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_weekly_summary():
    """Test weekly performance summary"""
    print("\n🔄 Testing get_stock_weekly_summary...")
    try:
        result = get_stock_weekly_summary.func("AAPL")
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        else:
            print(f"✅ Success: Weekly summary generated")
            print(f"   Current Price: ${result.get('current_price', 'N/A')}")
            print(f"   Weekly Change: {result.get('weekly_change_percent', 'N/A')}%")
            return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_ai_analysis():
    """Test AI-powered stock analysis"""
    print("\n🔄 Testing analyze_stock_with_ai...")
    try:
        result = analyze_stock_with_ai.func("AAPL", analysis_type="quick", include_recommendation=True)
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        else:
            print(f"✅ Success: AI analysis completed")
            recommendation = result.get("recommendation", {})
            print(f"   Recommendation: {recommendation.get('action', 'N/A')}")
            print(f"   Confidence: {recommendation.get('confidence_score', 'N/A')}")
            return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_technical_analysis():
    """Test technical indicators"""
    print("\n🔄 Testing get_technical_indicators...")
    try:
        result = get_technical_indicators.func("AAPL", period="daily", days_back=14)
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        else:
            print(f"✅ Success: Technical indicators calculated")
            rsi = result.get("indicators", {}).get("RSI", "N/A")
            print(f"   RSI: {rsi}")
            return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_financial_statements():
    """Test financial statements retrieval"""
    print("\n🔄 Testing get_income_statements...")
    try:
        result = get_income_statements.func("AAPL", period="quarterly", limit=2)
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        else:
            print(f"✅ Success: Retrieved {len(result)} income statements")
            return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def run_all_tests():
    """Run all tests and return summary"""
    print("🚀 Starting BayMax Agent MCP Server Tests\n")

    tests = [
        test_stock_price,
        test_price_history,
        test_weekly_summary,
        test_ai_analysis,
        test_technical_analysis,
        test_financial_statements
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"\n📊 Test Summary:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success Rate: {passed/total*100:.1f}%")

    if passed == total:
        print("🎉 All tests passed! MCP server is ready for use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)