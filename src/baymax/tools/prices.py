from langchain.tools import tool
from typing import Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import akshare as ak
import pandas as pd
import numpy as np
import requests
import time
from baymax.tools.api import normalize_ticker

# Configure requests timeout and retry settings
requests.adapters.DEFAULT_RETRIES = 3
requests.adapters.DEFAULT_POOL_TIMEOUT = 30

class StockPriceInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol to fetch price data for. For example, 'AAPL' for Apple, '600519' for 贵州茅台")
    period: Literal["daily", "weekly", "monthly"] = Field(default="daily", description="The time period for price data")
    days_back: int = Field(default=30, description="Number of days of historical data to retrieve")

class StockCurrentPriceInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol to fetch current price for. For example, 'AAPL' for Apple, '600519' for 贵州茅台")

@tool(args_schema=StockCurrentPriceInput)
def get_current_stock_price(ticker: str) -> dict:
    """
    Fetches the current stock price and basic market information including:
    - Current price
    - Price change and percentage change
    - Volume and market cap (if available)
    - Daily high/low prices

    Uses multiple fallback mechanisms to handle network issues.
    """
    try:
        ticker = normalize_ticker(ticker)
        print(f"Fetching current price for {ticker}...")

        # Try multiple approaches with fallbacks
        result = None

        # Approach 1: Try real-time data with timeout
        try:
            result = get_current_price_with_timeout(ticker, timeout=10)
            if result and result.get("current_price") and result["current_price"] > 0:
                print(f"✓ Got real-time price for {ticker}: {result['current_price']}")
                return result
        except Exception as e:
            print(f"⚠ Real-time data failed for {ticker}: {e}")

        # Approach 2: Try historical data fallback
        try:
            result = get_price_from_history_improved(ticker, timeout=15)
            if result and result.get("current_price") and result["current_price"] > 0:
                print(f"✓ Got historical price for {ticker}: {result['current_price']}")
                return result
        except Exception as e:
            print(f"⚠ Historical data failed for {ticker}: {e}")

        # Approach 3: Try alternative data sources
        try:
            result = get_price_from_alternative_source(ticker)
            if result and result.get("current_price") and result["current_price"] > 0:
                print(f"✓ Got alternative price for {ticker}: {result['current_price']}")
                return result
        except Exception as e:
            print(f"⚠ Alternative data failed for {ticker}: {e}")

        # If all approaches fail, return error with detailed info
        return {
            "error": f"All data sources failed for {ticker}. This may be due to network issues or the stock being delisted/renamed.",
            "ticker": ticker,
            "current_price": None,
            "attempted_sources": ["real_time", "historical", "alternative"],
            "suggestion": "Please check the ticker symbol or try again later."
        }

    except Exception as e:
        return {
            "error": f"Critical error getting current price for {ticker}: {str(e)}",
            "ticker": ticker,
            "current_price": None
        }

def get_current_price_with_timeout(ticker: str, timeout: int = 10) -> dict:
    """Get current price with timeout control"""
    try:
        # Set timeout for akshare operations
        import socket
        original_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)

        try:
            if ticker.endswith('.HK'):
                return get_hk_current_price_improved(ticker)
            elif ticker.isalpha() and len(ticker) <= 5:
                return get_us_current_price_improved(ticker)
            else:
                return get_cn_current_price_improved(ticker)
        finally:
            socket.setdefaulttimeout(original_timeout)

    except socket.timeout:
        raise Exception(f"Timeout after {timeout} seconds")
    except Exception as e:
        raise Exception(f"Network error: {str(e)}")

def get_hk_current_price_improved(ticker: str) -> dict:
    """Get current price for Hong Kong stocks with improved error handling"""
    try:
        stock_code = ticker.replace('.HK', '')

        # Try with timeout and retry logic
        for attempt in range(2):  # 2 attempts
            try:
                hk_spot = ak.stock_hk_spot_em()
                if not hk_spot.empty:
                    stock_data = hk_spot[hk_spot['代码'] == stock_code]
                    if not stock_data.empty:
                        stock_info = stock_data.iloc[0]
                        return {
                            "ticker": ticker,
                            "current_price": float(stock_info.get('最新价', 0)),
                            "change": float(stock_info.get('涨跌额', 0)),
                            "change_percent": float(stock_info.get('涨跌幅', 0)),
                            "volume": int(stock_info.get('成交量', 0)),
                            "high": float(stock_info.get('最高', 0)),
                            "low": float(stock_info.get('最低', 0)),
                            "open": float(stock_info.get('今开', 0)),
                            "previous_close": float(stock_info.get('昨收', 0)),
                            "market_time": stock_info.get('时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                            "data_source": "real_time_hk"
                        }
                break  # Success, exit retry loop
            except Exception as e:
                if attempt == 1:  # Last attempt
                    raise e
                time.sleep(1)  # Wait before retry

        # If real-time fails, try historical
        return get_price_from_history_improved(ticker, 'HK')

    except Exception as e:
        raise Exception(f"HK price fetch failed: {str(e)}")

def get_us_current_price_improved(ticker: str) -> dict:
    """Get current price for US stocks with improved error handling"""
    try:
        # Try with timeout and retry logic
        for attempt in range(2):  # 2 attempts
            try:
                us_spot = ak.stock_us_spot_em()
                if not us_spot.empty:
                    stock_data = us_spot[us_spot['代码'] == ticker]
                    if not stock_data.empty:
                        stock_info = stock_data.iloc[0]
                        return {
                            "ticker": ticker,
                            "current_price": float(stock_info.get('最新价', 0)),
                            "change": float(stock_info.get('涨跌额', 0)),
                            "change_percent": float(stock_info.get('涨跌幅', 0)),
                            "volume": int(stock_info.get('成交量', 0)),
                            "high": float(stock_info.get('最高', 0)),
                            "low": float(stock_info.get('最低', 0)),
                            "open": float(stock_info.get('今开', 0)),
                            "previous_close": float(stock_info.get('昨收', 0)),
                            "market_cap": float(stock_info.get('总市值', 0)) if '总市值' in stock_info else None,
                            "market_time": stock_info.get('时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                            "data_source": "real_time_us"
                        }
                break  # Success, exit retry loop
            except Exception as e:
                if attempt == 1:  # Last attempt
                    raise e
                time.sleep(1)  # Wait before retry

        # If real-time fails, try historical
        return get_price_from_history_improved(ticker, 'US')

    except Exception as e:
        raise Exception(f"US price fetch failed: {str(e)}")

def get_cn_current_price_improved(ticker: str) -> dict:
    """Get current price for A-shares with improved error handling"""
    try:
        # Try with timeout and retry logic
        for attempt in range(2):  # 2 attempts
            try:
                current_price = ak.stock_zh_a_spot_em()
                if not current_price.empty:
                    stock_data = current_price[current_price['代码'] == ticker]
                    if not stock_data.empty:
                        stock_info = stock_data.iloc[0]
                        return {
                            "ticker": ticker,
                            "current_price": float(stock_info.get('最新价', 0)),
                            "change": float(stock_info.get('涨跌额', 0)),
                            "change_percent": float(stock_info.get('涨跌幅', 0)),
                            "volume": int(stock_info.get('成交量', 0)),
                            "turnover": float(stock_info.get('成交额', 0)),
                            "high": float(stock_info.get('最高', 0)),
                            "low": float(stock_info.get('最低', 0)),
                            "open": float(stock_info.get('今开', 0)),
                            "previous_close": float(stock_info.get('昨收', 0)),
                            "market_cap": float(stock_info.get('总市值', 0)) if '总市值' in stock_info else None,
                            "pe_ratio": float(stock_info.get('市盈率', 0)) if '市盈率' in stock_info else None,
                            "pb_ratio": float(stock_info.get('市净率', 0)) if '市净率' in stock_info else None,
                            "market_time": stock_info.get('时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                            "data_source": "real_time_cn"
                        }
                break  # Success, exit retry loop
            except Exception as e:
                if attempt == 1:  # Last attempt
                    raise e
                time.sleep(1)  # Wait before retry

        # If real-time fails, try historical
        return get_price_from_history_improved(ticker, 'CN')

    except Exception as e:
        raise Exception(f"CN price fetch failed: {str(e)}")

def get_price_from_history_improved(ticker: str, market_type: str = 'CN', timeout: int = 15) -> dict:
    """Improved fallback method to get current price from historical data"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=14)  # Extended range for more data

        # Set socket timeout for historical data
        import socket
        original_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)

        try:
            if market_type == 'HK':
                hist_data = ak.stock_hk_hist(
                    symbol=ticker.replace('.HK', ''),
                    period="daily",
                    start_date=start_date.strftime('%Y%m%d'),
                    end_date=end_date.strftime('%Y%m%d')
                )
            elif market_type == 'US':
                hist_data = ak.stock_us_hist(
                    symbol=ticker,
                    period="daily",
                    start_date=start_date.strftime('%Y%m%d'),
                    end_date=end_date.strftime('%Y%m%d')
                )
            else:  # CN
                hist_data = ak.stock_zh_a_hist(
                    symbol=ticker,
                    period="daily",
                    start_date=start_date.strftime('%Y%m%d'),
                    end_date=end_date.strftime('%Y%m%d')
                )

            if not hist_data.empty:
                # Get the most recent data
                latest_data = hist_data.iloc[-1]

                # Get previous day for change calculation
                if len(hist_data) > 1:
                    previous_data = hist_data.iloc[-2]
                    prev_close = float(previous_data.get('收盘', 0))
                else:
                    prev_close = float(latest_data.get('收盘', 1))

                current_close = float(latest_data.get('收盘', 0))
                change = current_close - prev_close
                change_percent = (change / prev_close) * 100 if prev_close != 0 else 0

                return {
                    "ticker": ticker,
                    "current_price": current_close,
                    "change": change,
                    "change_percent": change_percent,
                    "volume": int(latest_data.get('成交量', 0)),
                    "high": float(latest_data.get('最高', 0)),
                    "low": float(latest_data.get('最低', 0)),
                    "open": float(latest_data.get('开盘', 0)),
                    "previous_close": prev_close,
                    "market_time": latest_data.get('日期', datetime.now().strftime('%Y-%m-%d')),
                    "data_source": "historical",
                    "data_points": len(hist_data)
                }
            else:
                raise Exception("No historical data available")

        finally:
            socket.setdefaulttimeout(original_timeout)

    except Exception as e:
        raise Exception(f"Historical price fetch failed: {str(e)}")

def get_price_from_alternative_source(ticker: str) -> dict:
    """Alternative data source using different AkShare functions"""
    try:
        ticker = normalize_ticker(ticker)

        # Try alternative approaches for different markets
        if ticker.endswith('.HK'):
            return get_hk_alternative(ticker)
        elif ticker.isalpha() and len(ticker) <= 5:
            return get_us_alternative(ticker)
        else:
            return get_cn_alternative(ticker)

    except Exception as e:
        raise Exception(f"Alternative data source failed: {str(e)}")

def get_hk_alternative(ticker: str) -> dict:
    """Alternative HK data source"""
    try:
        stock_code = ticker.replace('.HK', '')

        # Try individual stock info
        try:
            stock_info = ak.stock_hk_info(symbol=stock_code)
            if not stock_info.empty:
                info = stock_info.iloc[0]
                return {
                    "ticker": ticker,
                    "current_price": float(info.get('现价', 0)),
                    "change": float(info.get('涨跌', 0)),
                    "change_percent": float(info.get('涨跌幅', 0)),
                    "volume": int(info.get('成交量', 0)),
                    "data_source": "alternative_hk"
                }
        except:
            pass

        # Try using stock_individual_info_em with HK prefix
        try:
            stock_individual = ak.stock_individual_info_em(symbol=f"HK{stock_code}")
            if not stock_individual.empty:
                # Extract price from individual info
                return {
                    "ticker": ticker,
                    "current_price": 0,  # Will need to extract from info
                    "data_source": "individual_info_hk",
                    "note": "Limited data available"
                }
        except:
            pass

        raise Exception("No alternative HK data sources available")

    except Exception as e:
        raise Exception(f"Alternative HK failed: {str(e)}")

def get_us_alternative(ticker: str) -> dict:
    """Alternative US data source"""
    try:
        # Try stock_info interface
        try:
            stock_info = ak.stock_info(symbol=ticker)
            if not stock_info.empty:
                info = stock_info.iloc[0]
                return {
                    "ticker": ticker,
                    "current_price": float(info.get('current_price', 0)),
                    "data_source": "alternative_us",
                    "note": "Limited data from stock_info"
                }
        except:
            pass

        # Try using individual info
        try:
            individual_info = ak.stock_individual_info_em(symbol=ticker)
            if not individual_info.empty:
                return {
                    "ticker": ticker,
                    "current_price": 0,  # Extract from info
                    "data_source": "individual_info_us",
                    "note": "Individual info available"
                }
        except:
            pass

        raise Exception("No alternative US data sources available")

    except Exception as e:
        raise Exception(f"Alternative US failed: {str(e)}")

def get_cn_alternative(ticker: str) -> dict:
    """Alternative CN data source"""
    try:
        # Try individual stock info
        try:
            individual_info = ak.stock_individual_info_em(symbol=ticker)
            if not individual_info.empty:
                info_dict = {}
                for _, row in individual_info.iterrows():
                    if 'item' in row and 'value' in row:
                        info_dict[row['item']] = row['value']

                # Try to extract price from individual info
                price = 0
                if '现价' in info_dict:
                    price = float(info_dict['现价'])
                elif 'current_price' in info_dict:
                    price = float(info_dict['current_price'])

                return {
                    "ticker": ticker,
                    "current_price": price,
                    "data_source": "individual_info_cn",
                    "additional_info": info_dict,
                    "note": "Limited data from individual info"
                }
        except Exception as e:
            print(f"Individual info failed: {e}")

        # Try using stock_info interface
        try:
            stock_info = ak.stock_info(symbol=ticker)
            if not stock_info.empty:
                return {
                    "ticker": ticker,
                    "current_price": 0,  # Extract from available data
                    "data_source": "stock_info_cn",
                    "note": "Limited stock info available"
                }
        except:
            pass

        raise Exception("No alternative CN data sources available")

    except Exception as e:
        raise Exception(f"Alternative CN failed: {str(e)}")

@tool(args_schema=StockPriceInput)
def get_stock_price_history(ticker: str, period: Literal["daily", "weekly", "monthly"] = "daily", days_back: int = 30) -> dict:
    """
    Fetches historical stock price data including:
    - Daily/weekly/monthly price history
    - Volume data
    - High/low prices
    - Price change calculations
    """
    try:
        ticker = normalize_ticker(ticker)

        # Calculate date range with buffer
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back * 2)  # Buffer for weekends/holidays

        # Set timeout for operations
        import socket
        original_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(30)

        try:
            # Get historical data based on market type
            if ticker.endswith('.HK'):
                hist_data = ak.stock_hk_hist(
                    symbol=ticker.replace('.HK', ''),
                    period=period,
                    start_date=start_date.strftime('%Y%m%d'),
                    end_date=end_date.strftime('%Y%m%d')
                )
            elif ticker.isalpha() and len(ticker) <= 5:
                hist_data = ak.stock_us_hist(
                    symbol=ticker,
                    period=period,
                    start_date=start_date.strftime('%Y%m%d'),
                    end_date=end_date.strftime('%Y%m%d')
                )
            else:
                hist_data = ak.stock_zh_a_hist(
                    symbol=ticker,
                    period=period,
                    start_date=start_date.strftime('%Y%m%d'),
                    end_date=end_date.strftime('%Y%m%d')
                )

            if hist_data.empty:
                return {
                    "error": f"No price history found for {ticker}",
                    "ticker": ticker,
                    "price_data": []
                }

            # Process and clean data
            price_data = []
            for _, row in hist_data.iterrows():
                price_record = {
                    "date": row.get('日期', ''),
                    "open": float(row.get('开盘', 0)),
                    "high": float(row.get('最高', 0)),
                    "low": float(row.get('最低', 0)),
                    "close": float(row.get('收盘', 0)),
                    "volume": int(row.get('成交量', 0)),
                    "turnover": float(row.get('成交额', 0)) if '成交额' in row else 0
                }
                price_data.append(price_record)

            # Calculate additional metrics
            if len(price_data) > 0:
                latest_price = price_data[-1]['close']
                if len(price_data) > 1:
                    previous_price = price_data[-2]['close']
                    recent_change = latest_price - previous_price
                    recent_change_percent = (recent_change / previous_price) * 100 if previous_price != 0 else 0
                else:
                    recent_change = 0
                    recent_change_percent = 0

                # Calculate weekly performance if enough data
                weekly_performance = calculate_weekly_performance(price_data)

                return {
                    "ticker": ticker,
                    "period": period,
                    "price_data": price_data,
                    "latest_price": latest_price,
                    "recent_change": recent_change,
                    "recent_change_percent": recent_change_percent,
                    "weekly_performance": weekly_performance,
                    "data_points": len(price_data),
                    "date_range": {
                        "start": price_data[0]['date'] if price_data else None,
                        "end": price_data[-1]['date'] if price_data else None
                    }
                }

            return {
                "error": "No valid price data found",
                "ticker": ticker,
                "price_data": []
            }

        finally:
            socket.setdefaulttimeout(original_timeout)

    except Exception as e:
        return {
            "error": f"Failed to get price history for {ticker}: {str(e)}",
            "ticker": ticker,
            "price_data": []
        }

def calculate_weekly_performance(price_data: list) -> dict:
    """Calculate weekly performance metrics"""
    try:
        if len(price_data) < 5:  # Need at least 5 days for meaningful weekly data
            return {"error": "Insufficient data for weekly analysis"}

        # Get last 7 days of data (or available data)
        recent_data = price_data[-7:] if len(price_data) >= 7 else price_data

        if len(recent_data) < 2:
            return {"error": "Insufficient data for weekly analysis"}

        start_price = recent_data[0]['close']
        end_price = recent_data[-1]['close']

        weekly_change = end_price - start_price
        weekly_change_percent = (weekly_change / start_price) * 100 if start_price != 0 else 0

        # Calculate daily changes for the week
        daily_changes = []
        for i in range(1, len(recent_data)):
            prev_price = recent_data[i-1]['close']
            curr_price = recent_data[i]['close']
            daily_change = curr_price - prev_price
            daily_change_percent = (daily_change / prev_price) * 100 if prev_price != 0 else 0

            daily_changes.append({
                "date": recent_data[i]['date'],
                "price": curr_price,
                "change": daily_change,
                "change_percent": daily_change_percent
            })

        # Find best and worst performing days
        if daily_changes:
            best_day = max(daily_changes, key=lambda x: x['change_percent'])
            worst_day = min(daily_changes, key=lambda x: x['change_percent'])
        else:
            best_day = worst_day = None

        return {
            "period": "7_days",
            "start_date": recent_data[0]['date'],
            "end_date": recent_data[-1]['date'],
            "start_price": start_price,
            "end_price": end_price,
            "weekly_change": weekly_change,
            "weekly_change_percent": weekly_change_percent,
            "daily_changes": daily_changes,
            "best_performing_day": best_day,
            "worst_performing_day": worst_day,
            "volatility": calculate_volatility(recent_data)
        }

    except Exception as e:
        return {"error": f"Failed to calculate weekly performance: {str(e)}"}

def calculate_volatility(price_data: list) -> dict:
    """Calculate price volatility metrics"""
    try:
        if len(price_data) < 2:
            return {"error": "Insufficient data for volatility calculation"}

        prices = [data['close'] for data in price_data]
        returns = []

        for i in range(1, len(prices)):
            prev_price = prices[i-1]
            curr_price = prices[i]
            if prev_price != 0:
                daily_return = (curr_price - prev_price) / prev_price
                returns.append(daily_return)

        if not returns:
            return {"error": "No valid returns for volatility calculation"}

        # Calculate standard deviation of returns
        volatility = np.std(returns) * 100  # Convert to percentage
        avg_return = np.mean(returns) * 100

        return {
            "volatility_percent": round(volatility, 2),
            "average_daily_return": round(avg_return, 2),
            "data_points": len(returns)
        }

    except Exception as e:
        return {"error": f"Failed to calculate volatility: {str(e)}"}

@tool(args_schema=StockCurrentPriceInput)
def get_stock_weekly_summary(ticker: str) -> dict:
    """
    Gets a comprehensive weekly summary for a stock including:
    - Current price and recent performance
    - Weekly price changes and trends
    - Key statistics and volatility metrics
    """
    try:
        ticker = normalize_ticker(ticker)

        # Get current price with improved function
        current_price_info = get_current_stock_price.func(ticker)

        # Get weekly price history with improved function
        weekly_history = get_stock_price_history.func(ticker, period="daily", days_back=14)

        if "error" in current_price_info and current_price_info["current_price"] is None:
            return {
                "error": f"Failed to get current price for {ticker}",
                "ticker": ticker,
                "data_source_attempts": current_price_info.get("attempted_sources", [])
            }

        if "error" in weekly_history and not weekly_history.get("price_data"):
            return {
                "error": f"Failed to get price history for {ticker}",
                "ticker": ticker,
                "current_price": current_price_info.get("current_price"),
                "data_source": current_price_info.get("data_source", "unknown")
            }

        # Combine the data
        weekly_summary = {
            "ticker": ticker,
            "current_price_info": current_price_info,
            "weekly_performance": weekly_history.get("weekly_performance", {}),
            "price_history": weekly_history.get("price_data", [])[-10:],
            "data_summary": {
                "total_return_7d": weekly_history.get("weekly_performance", {}).get("weekly_change_percent", 0),
                "recent_change": weekly_history.get("recent_change_percent", 0),
                "volatility": weekly_history.get("weekly_performance", {}).get("volatility", {}).get("volatility_percent", 0),
                "trading_days_analyzed": len(weekly_history.get("price_data", [])),
                "data_sources": {
                    "price_source": current_price_info.get("data_source", "unknown"),
                    "history_source": "historical_data"
                }
            }
        }

        return weekly_summary

    except Exception as e:
        return {
            "error": f"Failed to get weekly summary for {ticker}: {str(e)}",
            "ticker": ticker
        }