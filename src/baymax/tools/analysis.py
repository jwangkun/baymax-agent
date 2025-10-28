from langchain.tools import tool
from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from baymax.tools.prices import get_current_stock_price, get_stock_price_history, get_stock_weekly_summary
from baymax.tools.api import normalize_ticker, get_stock_financial_data

class StockAnalysisInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol to analyze. For example, 'AAPL' for Apple, '600519' for 贵州茅台")
    analysis_type: Literal["comprehensive", "technical", "fundamental", "quick"] = Field(default="comprehensive", description="Type of analysis to perform")
    include_recommendation: bool = Field(default=True, description="Whether to include buy/sell recommendation")

class TechnicalIndicatorsInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol to analyze")
    period: Literal["daily", "weekly", "monthly"] = Field(default="daily", description="Time period for technical analysis")
    days_back: int = Field(default=30, description="Number of days of historical data to analyze")

@tool(args_schema=StockAnalysisInput)
def analyze_stock_with_ai(ticker: str, analysis_type: str = "comprehensive", include_recommendation: bool = True) -> dict:
    """
    Performs comprehensive AI-powered stock analysis including:
    - Current price and recent performance
    - Technical indicators and trends
    - Risk assessment
    - Buy/sell/hold recommendations with reasoning
    - Price targets and support/resistance levels
    """
    try:
        ticker = normalize_ticker(ticker)

        print(f"Analyzing {ticker} with AI...")

        # Gather comprehensive data
        analysis_data = gather_analysis_data(ticker, analysis_type)

        if "error" in analysis_data:
            return analysis_data

        # Generate AI-powered insights and recommendations
        ai_analysis = generate_ai_analysis(analysis_data, analysis_type, include_recommendation)

        # Combine all analysis
        comprehensive_report = {
            "ticker": ticker,
            "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "analysis_type": analysis_type,
            "data_summary": analysis_data.get("data_summary", {}),
            "technical_analysis": analysis_data.get("technical_analysis", {}),
            "risk_assessment": analysis_data.get("risk_assessment", {}),
            "ai_insights": ai_analysis.get("ai_insights", {}),
            "recommendation": ai_analysis.get("recommendation", {}),
            "price_targets": ai_analysis.get("price_targets", {}),
            "confidence_score": ai_analysis.get("confidence_score", 0)
        }

        return comprehensive_report

    except Exception as e:
        return {
            "error": f"Failed to analyze {ticker}: {str(e)}",
            "ticker": ticker,
            "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def gather_analysis_data(ticker: str, analysis_type: str) -> dict:
    """Gather all necessary data for analysis"""
    try:
        data_summary = {}
        technical_analysis = {}
        risk_assessment = {}

        # Get current price and recent performance
        print("Getting current price data...")
        current_price_data = get_current_stock_price.func(ticker)
        if "error" not in current_price_data:
            data_summary["current_price"] = current_price_data.get("current_price")
            data_summary["daily_change"] = current_price_data.get("change_percent", 0)
            data_summary["volume"] = current_price_data.get("volume", 0)

        # Get weekly performance
        print("Getting weekly performance...")
        weekly_data = get_stock_weekly_summary.func(ticker)
        if "error" not in weekly_data:
            weekly_perf = weekly_data.get("weekly_performance", {})
            data_summary["weekly_return"] = weekly_perf.get("weekly_change_percent", 0)
            data_summary["volatility"] = weekly_perf.get("volatility", {}).get("volatility_percent", 0)
            data_summary["best_day"] = weekly_perf.get("best_performing_day", {})
            data_summary["worst_day"] = weekly_perf.get("worst_performing_day", {})

        # Get price history for technical analysis
        print("Getting price history for technical analysis...")
        price_history = get_stock_price_history.func(ticker, period="daily", days_back=60)
        if "error" not in price_history and price_history.get("price_data"):
            technical_analysis = calculate_technical_indicators(price_history["price_data"])
            risk_assessment = assess_risk(price_history["price_data"])

        # Get financial data if comprehensive analysis
        if analysis_type == "comprehensive":
            print("Getting financial data...")
            financial_data = get_stock_financial_data(ticker, "quarterly", 4)
            if financial_data.get("income_statements"):
                data_summary["latest_revenue"] = extract_latest_revenue(financial_data["income_statements"])
                data_summary["profitability_trend"] = analyze_profitability_trend(financial_data["income_statements"])

        return {
            "data_summary": data_summary,
            "technical_analysis": technical_analysis,
            "risk_assessment": risk_assessment,
            "raw_data": {
                "current_price": current_price_data,
                "weekly_summary": weekly_data,
                "price_history": price_history
            }
        }

    except Exception as e:
        return {"error": f"Failed to gather analysis data: {str(e)}"}

def calculate_technical_indicators(price_data: list) -> dict:
    """Calculate technical indicators"""
    try:
        if len(price_data) < 20:  # Need minimum data for indicators
            return {"error": "Insufficient data for technical analysis"}

        # Extract prices and volumes
        closes = [float(data['close']) for data in price_data]
        highs = [float(data['high']) for data in price_data]
        lows = [float(data['low']) for data in price_data]
        volumes = [float(data['volume']) for data in price_data]

        indicators = {}

        # Moving Averages
        indicators["sma_5"] = np.mean(closes[-5:]) if len(closes) >= 5 else closes[-1]
        indicators["sma_20"] = np.mean(closes[-20:]) if len(closes) >= 20 else np.mean(closes)
        indicators["sma_50"] = np.mean(closes[-50:]) if len(closes) >= 50 else np.mean(closes)

        # Price relative to moving averages
        current_price = closes[-1]
        indicators["price_vs_sma5"] = ((current_price - indicators["sma_5"]) / indicators["sma_5"]) * 100
        indicators["price_vs_sma20"] = ((current_price - indicators["sma_20"]) / indicators["sma_20"]) * 100

        # RSI (Relative Strength Index) - simplified calculation
        indicators["rsi"] = calculate_rsi(closes)

        # Support and Resistance levels
        support_resistance = calculate_support_resistance(highs, lows, closes)
        indicators.update(support_resistance)

        # Volume analysis
        avg_volume = np.mean(volumes[-20:]) if len(volumes) >= 20 else np.mean(volumes)
        current_volume = volumes[-1]
        indicators["volume_ratio"] = current_volume / avg_volume if avg_volume > 0 else 1

        # Trend analysis
        indicators["trend"] = analyze_trend(closes)

        return indicators

    except Exception as e:
        return {"error": f"Failed to calculate technical indicators: {str(e)}"}

def calculate_rsi(prices: list, period: int = 14) -> float:
    """Calculate RSI (Relative Strength Index)"""
    try:
        if len(prices) < period + 1:
            return 50.0  # Neutral RSI if insufficient data

        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas[-period:]]
        losses = [-d if d < 0 else 0 for d in deltas[-period:]]

        avg_gain = np.mean(gains) if gains else 0
        avg_loss = np.mean(losses) if losses else 0

        if avg_loss == 0:
            return 100.0  # Overbought if no losses

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return round(rsi, 2)

    except Exception:
        return 50.0

def calculate_support_resistance(highs: list, lows: list, closes: list) -> dict:
    """Calculate support and resistance levels"""
    try:
        # Simple pivot point calculation
        recent_high = max(highs[-10:])
        recent_low = min(lows[-10:])
        recent_close = closes[-1]

        # Classic pivot point
        pivot = (recent_high + recent_low + recent_close) / 3

        # Support and resistance levels
        r1 = 2 * pivot - recent_low
        s1 = 2 * pivot - recent_high
        r2 = pivot + (recent_high - recent_low)
        s2 = pivot - (recent_high - recent_low)

        return {
            "pivot_point": round(pivot, 2),
            "resistance_1": round(r1, 2),
            "support_1": round(s1, 2),
            "resistance_2": round(r2, 2),
            "support_2": round(s2, 2),
            "recent_high": recent_high,
            "recent_low": recent_low
        }

    except Exception:
        return {}

def analyze_trend(prices: list) -> str:
    """Analyze price trend"""
    try:
        if len(prices) < 5:
            return "NEUTRAL"

        # Simple trend analysis based on recent vs older prices
        recent_avg = np.mean(prices[-5:])
        older_avg = np.mean(prices[-10:-5]) if len(prices) >= 10 else np.mean(prices[:-5])

        trend_strength = abs(recent_avg - older_avg) / older_avg * 100

        if recent_avg > older_avg:
            if trend_strength > 2:
                return "STRONG_UPTREND"
            else:
                return "WEAK_UPTREND"
        elif recent_avg < older_avg:
            if trend_strength > 2:
                return "STRONG_DOWNTREND"
            else:
                return "WEAK_DOWNTREND"
        else:
            return "NEUTRAL"

    except Exception:
        return "NEUTRAL"

def assess_risk(price_data: list) -> dict:
    """Assess investment risk"""
    try:
        if len(price_data) < 10:
            return {"error": "Insufficient data for risk assessment"}

        closes = [float(data['close']) for data in price_data]

        # Volatility calculation
        returns = []
        for i in range(1, len(closes)):
            if closes[i-1] != 0:
                returns.append((closes[i] - closes[i-1]) / closes[i-1])

        volatility = np.std(returns) * 100 if returns else 0

        # Maximum drawdown
        max_drawdown = calculate_max_drawdown(closes)

        # Risk rating based on volatility
        if volatility < 2:
            risk_rating = "LOW"
            risk_score = 1
        elif volatility < 5:
            risk_rating = "MEDIUM"
            risk_score = 2
        else:
            risk_rating = "HIGH"
            risk_score = 3

        return {
            "volatility_percent": round(volatility, 2),
            "max_drawdown_percent": round(max_drawdown, 2),
            "risk_rating": risk_rating,
            "risk_score": risk_score,
            "risk_factors": [
                f"Price volatility: {volatility:.1f}%",
                f"Maximum drawdown: {max_drawdown:.1f}%"
            ]
        }

    except Exception as e:
        return {"error": f"Failed to assess risk: {str(e)}"}

def calculate_max_drawdown(prices: list) -> float:
    """Calculate maximum drawdown"""
    try:
        if len(prices) < 2:
            return 0

        peak = prices[0]
        max_dd = 0

        for price in prices[1:]:
            if price > peak:
                peak = price
            else:
                drawdown = (peak - price) / peak * 100
                if drawdown > max_dd:
                    max_dd = drawdown

        return max_dd

    except Exception:
        return 0

def extract_latest_revenue(financial_statements: list) -> float:
    """Extract latest revenue from financial statements"""
    try:
        if not financial_statements:
            return 0

        # Try to find revenue in the first statement
        latest = financial_statements[0]

        # Common revenue field names
        revenue_fields = ['revenue', '营业收入', '营业总收入', 'total_revenue', '销售收入']

        for field in revenue_fields:
            if field in latest:
                value = latest[field]
                if isinstance(value, (int, float)) and value > 0:
                    return float(value)

        return 0

    except Exception:
        return 0

def analyze_profitability_trend(financial_statements: list) -> str:
    """Analyze profitability trend"""
    try:
        if len(financial_statements) < 2:
            return "INSUFFICIENT_DATA"

        # Extract net income or profit data
        profits = []
        profit_fields = ['net_income', '净利润', '归属于母公司股东的净利润', 'profit', 'net_profit']

        for statement in financial_statements[:4]:  # Look at last 4 periods
            profit_found = False
            for field in profit_fields:
                if field in statement:
                    value = statement[field]
                    if isinstance(value, (int, float)):
                        profits.append(float(value))
                        profit_found = True
                        break
            if not profit_found:
                profits.append(0)

        if len(profits) < 2:
            return "INSUFFICIENT_DATA"

        # Analyze trend
        recent_profit = profits[0]
        older_profit = profits[-1]

        if recent_profit > older_profit * 1.1:  # 10% increase
            return "IMPROVING"
        elif recent_profit < older_profit * 0.9:  # 10% decrease
            return "DECLINING"
        else:
            return "STABLE"

    except Exception:
        return "UNKNOWN"

def generate_ai_analysis(analysis_data: dict, analysis_type: str, include_recommendation: bool) -> dict:
    """Generate AI-powered insights and recommendations"""
    try:
        data_summary = analysis_data.get("data_summary", {})
        technical = analysis_data.get("technical_analysis", {})
        risk = analysis_data.get("risk_assessment", {})

        ai_insights = {}
        recommendation = {}
        price_targets = {}
        confidence_score = 0

        # Technical Analysis Insights
        if technical and "error" not in technical:
            rsi = technical.get("rsi", 50)
            trend = technical.get("trend", "NEUTRAL")
            price_vs_sma20 = technical.get("price_vs_sma20", 0)

            ai_insights["technical"] = {
                "momentum": interpret_rsi(rsi),
                "trend_analysis": interpret_trend(trend, price_vs_sma20),
                "support_resistance": analyze_support_resistance(technical, data_summary.get("current_price", 0))
            }

        # Risk Assessment Insights
        if risk and "error" not in risk:
            risk_rating = risk.get("risk_rating", "MEDIUM")
            volatility = risk.get("volatility_percent", 0)
            max_dd = risk.get("max_drawdown_percent", 0)

            ai_insights["risk"] = {
                "risk_level": risk_rating,
                "volatility_assessment": interpret_volatility(volatility),
                "drawdown_concern": max_dd > 15,
                "suitability": assess_suitability(risk_rating, volatility)
            }

        # Generate recommendation if requested
        if include_recommendation:
            recommendation = generate_recommendation(data_summary, technical, risk)
            price_targets = generate_price_targets(data_summary, technical)
            confidence_score = calculate_confidence_score(data_summary, technical, risk)

        return {
            "ai_insights": ai_insights,
            "recommendation": recommendation,
            "price_targets": price_targets,
            "confidence_score": confidence_score
        }

    except Exception as e:
        return {
            "error": f"Failed to generate AI analysis: {str(e)}",
            "ai_insights": {},
            "recommendation": {},
            "price_targets": {},
            "confidence_score": 0
        }

def interpret_rsi(rsi: float) -> dict:
    """Interpret RSI value"""
    if rsi >= 70:
        return {"level": "OVERBOUGHT", "value": rsi, "signal": "SELL"}
    elif rsi <= 30:
        return {"level": "OVERSOLD", "value": rsi, "signal": "BUY"}
    else:
        return {"level": "NEUTRAL", "value": rsi, "signal": "HOLD"}

def interpret_trend(trend: str, price_vs_sma20: float) -> dict:
    """Interpret trend analysis"""
    trend_strength = "STRONG" if "STRONG" in trend else "WEAK" if "WEAK" in trend else "NEUTRAL"

    return {
        "trend_direction": trend.replace("STRONG_", "").replace("WEAK_", ""),
        "trend_strength": trend_strength,
        "price_vs_moving_average": round(price_vs_sma20, 2),
        "signal": "BUY" if "UPTREND" in trend else "SELL" if "DOWNTREND" in trend else "HOLD"
    }

def analyze_support_resistance(technical: dict, current_price: float) -> dict:
    """Analyze support and resistance levels"""
    try:
        support_1 = technical.get("support_1", 0)
        resistance_1 = technical.get("resistance_1", 0)

        if current_price == 0 or support_1 == 0 or resistance_1 == 0:
            return {"signal": "HOLD", "levels": {}}

        # Calculate proximity to levels
        support_distance = ((current_price - support_1) / support_1) * 100 if support_1 > 0 else 100
        resistance_distance = ((resistance_1 - current_price) / current_price) * 100 if current_price > 0 else 100

        if support_distance < 2:  # Within 2% of support
            signal = "BUY"
        elif resistance_distance < 2:  # Within 2% of resistance
            signal = "SELL"
        else:
            signal = "HOLD"

        return {
            "signal": signal,
            "levels": {
                "support_1": support_1,
                "resistance_1": resistance_1,
                "support_distance_percent": round(support_distance, 2),
                "resistance_distance_percent": round(resistance_distance, 2)
            }
        }

    except Exception:
        return {"signal": "HOLD", "levels": {}}

def interpret_volatility(volatility: float) -> str:
    """Interpret volatility value"""
    if volatility < 2:
        return "LOW_VOLATILITY_STABLE"
    elif volatility < 5:
        return "MODERATE_VOLATILITY_NORMAL"
    elif volatility < 10:
        return "HIGH_VOLATILITY_RISKY"
    else:
        return "VERY_HIGH_VOLATILITY_SPECULATIVE"

def assess_suitability(risk_rating: str, volatility: float) -> str:
    """Assess investment suitability"""
    if risk_rating == "LOW":
        return "SUITABLE_FOR_CONSERVATIVE_INVESTORS"
    elif risk_rating == "MEDIUM":
        return "SUITABLE_FOR_MODERATE_INVESTORS"
    else:
        return "SUITABLE_FOR_AGGRESSIVE_INVESTORS_ONLY"

def generate_recommendation(data_summary: dict, technical: dict, risk: dict) -> dict:
    """Generate buy/sell/hold recommendation"""
    try:
        # Initialize scoring
        buy_score = 0
        sell_score = 0
        hold_score = 0
        reasoning = []

        # Technical factors
        if technical and "error" not in technical:
            # RSI signal
            rsi_signal = interpret_rsi(technical.get("rsi", 50))["signal"]
            if rsi_signal == "BUY":
                buy_score += 2
                reasoning.append(f"RSI indicates oversold conditions ({technical.get('rsi', 0):.1f})")
            elif rsi_signal == "SELL":
                sell_score += 2
                reasoning.append(f"RSI indicates overbought conditions ({technical.get('rsi', 0):.1f})")
            else:
                hold_score += 1

            # Trend signal
            trend_signal = interpret_trend(technical.get("trend", "NEUTRAL"), technical.get("price_vs_sma20", 0))["signal"]
            if trend_signal == "BUY":
                buy_score += 3
                reasoning.append("Technical trend shows upward momentum")
            elif trend_signal == "SELL":
                sell_score += 3
                reasoning.append("Technical trend shows downward momentum")
            else:
                hold_score += 1

            # Support/Resistance
            sr_analysis = analyze_support_resistance(technical, data_summary.get("current_price", 0))
            if sr_analysis["signal"] == "BUY":
                buy_score += 2
                reasoning.append("Price near support level")
            elif sr_analysis["signal"] == "SELL":
                sell_score += 2
                reasoning.append("Price near resistance level")

        # Risk factors
        if risk and "error" not in risk:
            risk_rating = risk.get("risk_rating", "MEDIUM")
            volatility = risk.get("volatility_percent", 0)
            max_dd = risk.get("max_drawdown_percent", 0)

            if risk_rating == "HIGH":
                sell_score += 1
                reasoning.append("High risk level requires caution")
            elif risk_rating == "LOW":
                buy_score += 1
                reasoning.append("Low risk profile is favorable")

            if volatility > 10:
                hold_score += 1
                reasoning.append("High volatility suggests waiting for clearer signals")

            if max_dd > 20:
                sell_score += 1
                reasoning.append("Large maximum drawdown indicates significant downside risk")

        # Price performance factors
        weekly_return = data_summary.get("weekly_return", 0)
        if weekly_return < -5:
            buy_score += 1
            reasoning.append("Recent price decline may present buying opportunity")
        elif weekly_return > 5:
            sell_score += 1
            reasoning.append("Recent strong gains suggest taking profits")

        # Determine final recommendation
        if buy_score > sell_score and buy_score > hold_score:
            action = "BUY"
            urgency = "STRONG" if buy_score >= sell_score + 3 else "MODERATE"
        elif sell_score > buy_score and sell_score > hold_score:
            action = "SELL"
            urgency = "STRONG" if sell_score >= buy_score + 3 else "MODERATE"
        else:
            action = "HOLD"
            urgency = "NEUTRAL"

        return {
            "action": action,
            "urgency": urgency,
            "score_breakdown": {
                "buy_score": buy_score,
                "sell_score": sell_score,
                "hold_score": hold_score
            },
            "reasoning": reasoning,
            "time_horizon": "SHORT_TERM" if urgency == "STRONG" else "MEDIUM_TERM"
        }

    except Exception as e:
        return {
            "action": "HOLD",
            "urgency": "NEUTRAL",
            "score_breakdown": {"buy_score": 0, "sell_score": 0, "hold_score": 1},
            "reasoning": [f"Analysis error: {str(e)}"],
            "time_horizon": "UNKNOWN"
        }

def generate_price_targets(data_summary: dict, technical: dict) -> dict:
    """Generate price targets based on analysis"""
    try:
        current_price = data_summary.get("current_price", 0)
        if current_price == 0:
            return {"error": "No current price available for target generation"}

        # Base targets on technical levels
        support_1 = technical.get("support_1", current_price * 0.95)
        resistance_1 = technical.get("resistance_1", current_price * 1.05)

        # Calculate percentage targets
        upside_potential = ((resistance_1 - current_price) / current_price) * 100
        downside_risk = ((current_price - support_1) / current_price) * 100

        # Risk-reward ratio
        risk_reward = upside_potential / downside_risk if downside_risk > 0 else upside_potential

        return {
            "current_price": round(current_price, 2),
            "upside_target": round(resistance_1, 2),
            "downside_target": round(support_1, 2),
            "upside_potential_percent": round(upside_potential, 2),
            "downside_risk_percent": round(downside_risk, 2),
            "risk_reward_ratio": round(risk_reward, 2),
            "target_timeframe": "1-4 weeks",
            "confidence_level": "MODERATE"
        }

    except Exception as e:
        return {"error": f"Failed to generate price targets: {str(e)}"}

def calculate_confidence_score(data_summary: dict, technical: dict, risk: dict) -> int:
    """Calculate confidence score for the analysis (0-100)"""
    try:
        score = 50  # Base score

        # Data quality factors
        if data_summary.get("current_price"):
            score += 10
        if data_summary.get("weekly_return") is not None:
            score += 10
        if data_summary.get("volatility") is not None:
            score += 10

        # Technical analysis factors
        if technical and "error" not in technical:
            if technical.get("rsi"):
                score += 10
            if technical.get("trend"):
                score += 10
            if technical.get("support_1") and technical.get("resistance_1"):
                score += 10

        # Risk assessment factors
        if risk and "error" not in risk:
            if risk.get("risk_rating"):
                score += 5
            if risk.get("volatility_percent") is not None:
                score += 5

        # Penalize high volatility
        volatility = data_summary.get("volatility", 0)
        if volatility > 10:
            score -= 10
        elif volatility > 5:
            score -= 5

        return max(0, min(100, score))  # Ensure 0-100 range

    except Exception:
        return 50  # Default confidence if calculation fails

@tool(args_schema=TechnicalIndicatorsInput)
def get_technical_indicators(ticker: str, period: str = "daily", days_back: int = 30) -> dict:
    """
    Calculates technical indicators for a stock including:
    - Moving averages (5, 20, 50 day)
    - RSI (Relative Strength Index)
    - Support and resistance levels
    - Volume analysis
    - Trend identification
    """
    try:
        ticker = normalize_ticker(ticker)

        # Get price history
        price_history = get_stock_price_history.func(ticker, period, days_back)

        if "error" in price_history or not price_history.get("price_data"):
            return {
                "error": f"Failed to get price history for {ticker}",
                "ticker": ticker
            }

        # Calculate technical indicators
        indicators = calculate_technical_indicators(price_history["price_data"])

        return {
            "ticker": ticker,
            "period": period,
            "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "indicators": indicators,
            "data_points": len(price_history.get("price_data", [])),
            "current_price": price_history.get("latest_price", 0)
        }

    except Exception as e:
        return {
            "error": f"Failed to calculate technical indicators for {ticker}: {str(e)}",
            "ticker": ticker
        }