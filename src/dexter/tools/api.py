import os
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
import numpy as np

####################################
# AkShare Configuration
####################################

def normalize_ticker(ticker: str) -> str:
    """标准化股票代码，支持美股和A股"""
    ticker = ticker.upper().strip()
    # 如果是美股，保持原样（如 AAPL, MSFT）
    # 如果是A股，确保是6位数字代码
    if ticker.isdigit():
        if len(ticker) == 6:
            return ticker
        else:
            # 尝试补充前导零
            return ticker.zfill(6)
    return ticker

####################################
# AkShare Configuration
####################################

def normalize_ticker(ticker: str) -> str:
    """标准化股票代码，支持美股和A股"""
    ticker = ticker.upper().strip()
    # 如果是美股，保持原样（如 AAPL, MSFT）
    # 如果是A股，确保是6位数字代码
    if ticker.isdigit():
        if len(ticker) == 6:
            return ticker
        else:
            # 尝试补充前导零
            return ticker.zfill(6)
    return ticker

def get_stock_financial_data(ticker: str, period: str, limit: int = 10) -> dict:
    """使用akshare获取股票财务数据"""
    try:
        ticker = normalize_ticker(ticker)
        
        # 获取财务报表数据 - 使用更稳定的接口
        try:
            # 尝试使用东方财富接口
            income_df = ak.stock_financial_abstract(symbol=ticker)
            balance_df = ak.stock_balance_sheet_by_report_em(symbol=ticker)
            cashflow_df = ak.stock_cash_flow_sheet_by_report_em(symbol=ticker)
        except:
            # 如果东方财富接口失败，使用新浪财经接口
            try:
                income_df = ak.stock_financial_report_sina(stock=ticker, symbol="利润表")
                balance_df = ak.stock_financial_report_sina(stock=ticker, symbol="资产负债表") 
                cashflow_df = ak.stock_financial_report_sina(stock=ticker, symbol="现金流量表")
            except:
                # 如果都失败，尝试使用其他接口
                income_df = ak.stock_financial_hk_report_em(symbol=ticker) if len(ticker) <= 4 else pd.DataFrame()
                balance_df = pd.DataFrame()
                cashflow_df = pd.DataFrame()

        # 数据清洗和标准化
        def clean_financial_data(df: pd.DataFrame, statement_type: str) -> pd.DataFrame:
            """清洗财务数据"""
            if df.empty:
                return df
                
            # 重命名列名为英文标准名称
            if '报表期截止日' in df.columns:
                df = df.rename(columns={'报表期截止日': 'report_date'})
            if '报告日期' in df.columns:
                df = df.rename(columns={'报告日期': 'report_date'})
                
            # 确保report_date列存在
            if 'report_date' not in df.columns and len(df) > 0:
                # 如果没有日期列，添加一个默认的
                df['report_date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
                
            return df

        # 清洗数据
        income_df = clean_financial_data(income_df, 'income')
        balance_df = clean_financial_data(balance_df, 'balance')
        cashflow_df = clean_financial_data(cashflow_df, 'cashflow')

        # 根据period类型筛选数据
        if period == "quarterly":
            # 筛选季报数据
            if not income_df.empty and 'report_date' in income_df.columns:
                # 假设季度数据有特定标识
                income_df = income_df.head(limit*4)  # 季度数据更多
            if not balance_df.empty and 'report_date' in balance_df.columns:
                balance_df = balance_df.head(limit*4)
            if not cashflow_df.empty and 'report_date' in cashflow_df.columns:
                cashflow_df = cashflow_df.head(limit*4)
        elif period == "ttm":
            # TTM数据：收入表和现金流量表取最近4期求和，资产负债表取最近一期
            if len(income_df) >= 4:
                numeric_cols = income_df.select_dtypes(include=[np.number]).columns
                ttm_data = income_df[numeric_cols].head(4).sum()
                ttm_data['report_date'] = f"TTM_{pd.Timestamp.now().strftime('%Y-%m-%d')}"
                income_df = pd.DataFrame([ttm_data])
            if len(balance_df) >= 1:
                balance_df = balance_df.head(1)
            if len(cashflow_df) >= 4:
                numeric_cols = cashflow_df.select_dtypes(include=[np.number]).columns
                ttm_data = cashflow_df[numeric_cols].head(4).sum()
                ttm_data['report_date'] = f"TTM_{pd.Timestamp.now().strftime('%Y-%m-%d')}"
                cashflow_df = pd.DataFrame([ttm_data])
        else:  # annual
            # 年报数据，按日期排序取最近的
            for df in [income_df, balance_df, cashflow_df]:
                if not df.empty and 'report_date' in df.columns:
                    df.sort_values('report_date', ascending=False, inplace=True)

        # 限制返回的记录数
        income_df = income_df.head(limit) if len(income_df) > 0 else pd.DataFrame()
        balance_df = balance_df.head(limit) if len(balance_df) > 0 else pd.DataFrame()
        cashflow_df = cashflow_df.head(limit) if len(cashflow_df) > 0 else pd.DataFrame()

        return {
            "income_statements": income_df.to_dict('records') if not income_df.empty else [],
            "balance_sheets": balance_df.to_dict('records') if not balance_df.empty else [],
            "cash_flow_statements": cashflow_df.to_dict('records') if not cashflow_df.empty else []
        }

    except Exception as e:
        print(f"获取股票{ticker}财务数据失败: {str(e)}")
        return {
            "income_statements": [],
            "balance_sheets": [],
            "cash_flow_statements": []
        }

def get_stock_basic_info(ticker: str) -> dict:
    """获取股票基本信息"""
    try:
        ticker = normalize_ticker(ticker)
        
        # 获取股票基本信息 - 尝试多个接口
        stock_info = None
        
        try:
            # 尝试使用东方财富接口
            stock_info = ak.stock_individual_info_em(symbol=ticker)
        except:
            try:
                # 尝试使用新浪财经接口
                stock_info = ak.stock_individual_info(symbol=ticker)
            except:
                # 如果都失败，返回空数据
                return {}
        
        if stock_info is not None and not stock_info.empty:
            # 转换为更友好的格式
            info_dict = {}
            for _, row in stock_info.iterrows():
                if 'item' in row and 'value' in row:
                    info_dict[row['item']] = row['value']
            return info_dict
        return {}
        
    except Exception as e:
        print(f"获取股票{ticker}基本信息失败: {str(e)}")
        return {}

def call_api(endpoint: str, params: dict) -> dict:
    """兼容原有API接口的函数，现在使用akshare实现"""
    ticker = params.get("ticker", "")
    period = params.get("period", "annual")
    limit = params.get("limit", 10)
    
    if not ticker:
        return {"error": "股票代码不能为空"}

    try:
        if "/financials/income-statements/" in endpoint:
            data = get_stock_financial_data(ticker, period, limit)
            return {"income_statements": data["income_statements"]}
        elif "/financials/balance-sheets/" in endpoint:
            data = get_stock_financial_data(ticker, period, limit)
            return {"balance_sheets": data["balance_sheets"]}
        elif "/financials/cash-flow-statements/" in endpoint:
            data = get_stock_financial_data(ticker, period, limit)
            return {"cash_flow_statements": data["cash_flow_statements"]}
        else:
            return {"error": f"不支持的端点: {endpoint}"}
    except Exception as e:
        return {"error": f"获取数据失败: {str(e)}"}

