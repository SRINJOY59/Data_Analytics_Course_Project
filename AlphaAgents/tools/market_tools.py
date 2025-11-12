"""
Tools for agents to interact with market data and perform analysis
"""
from typing import List, Dict, Any
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_stock_price(ticker: str, period: str = "1mo") -> Dict[str, Any]:
    """
    Get current stock price and basic information
    
    Args:
        ticker: Stock ticker symbol
        period: Time period for historical data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y)
    
    Returns:
        Dictionary with price data and metrics
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        
        return {
            "ticker": ticker,
            "current_price": info.get("currentPrice", hist['Close'].iloc[-1]),
            "change": hist['Close'].iloc[-1] - hist['Close'].iloc[0],
            "change_percent": ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100,
            "volume": info.get("volume", hist['Volume'].iloc[-1]),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def get_financial_metrics(ticker: str) -> Dict[str, Any]:
    """
    Get comprehensive financial metrics for a stock
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Dictionary with financial metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "ticker": ticker,
            "revenue": info.get("totalRevenue", "N/A"),
            "profit_margin": info.get("profitMargins", "N/A"),
            "roe": info.get("returnOnEquity", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "current_ratio": info.get("currentRatio", "N/A"),
            "eps": info.get("trailingEps", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "peg_ratio": info.get("pegRatio", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "beta": info.get("beta", "N/A"),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def calculate_volatility(ticker: str, period: str = "1y") -> Dict[str, float]:
    """
    Calculate historical volatility for a stock
    
    Args:
        ticker: Stock ticker symbol
        period: Time period for calculation
    
    Returns:
        Dictionary with volatility metrics
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        returns = hist['Close'].pct_change().dropna()
        
        return {
            "ticker": ticker,
            "volatility": returns.std() * (252 ** 0.5),  # Annualized
            "avg_return": returns.mean() * 252,  # Annualized
            "sharpe_ratio": (returns.mean() * 252) / (returns.std() * (252 ** 0.5)) if returns.std() > 0 else 0,
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def get_stock_news(ticker: str, max_items: int = 5) -> List[Dict[str, str]]:
    """
    Get recent news for a stock
    
    Args:
        ticker: Stock ticker symbol
        max_items: Maximum number of news items
    
    Returns:
        List of news items
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news[:max_items] if stock.news else []
        
        return [
            {
                "title": item.get("title", ""),
                "publisher": item.get("publisher", ""),
                "link": item.get("link", ""),
            }
            for item in news
        ]
    except Exception as e:
        return [{"error": str(e)}]


def compare_stocks(tickers: List[str], metric: str = "pe_ratio") -> Dict[str, Any]:
    """
    Compare multiple stocks on a specific metric
    
    Args:
        tickers: List of stock ticker symbols
        metric: Metric to compare (pe_ratio, market_cap, roe, etc.)
    
    Returns:
        Comparison data
    """
    results = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            metric_map = {
                "pe_ratio": "trailingPE",
                "market_cap": "marketCap",
                "roe": "returnOnEquity",
                "profit_margin": "profitMargins",
                "dividend_yield": "dividendYield",
                "beta": "beta",
            }
            
            key = metric_map.get(metric, metric)
            results[ticker] = info.get(key, "N/A")
            
        except Exception as e:
            results[ticker] = f"Error: {str(e)}"
    
    return results


def get_sector_performance(sector: str = "Technology") -> Dict[str, Any]:
    """
    Get sector performance metrics (simplified)
    
    Args:
        sector: Sector name
    
    Returns:
        Sector performance data
    """
    # Using sector ETFs as proxies
    sector_etfs = {
        "Technology": "XLK",
        "Healthcare": "XLV",
        "Financials": "XLF",
        "Energy": "XLE",
        "Consumer Discretionary": "XLY",
        "Consumer Staples": "XLP",
        "Industrials": "XLI",
        "Materials": "XLB",
        "Utilities": "XLU",
        "Real Estate": "XLRE",
        "Communication Services": "XLC",
    }
    
    etf_ticker = sector_etfs.get(sector, "SPY")
    
    try:
        etf = yf.Ticker(etf_ticker)
        hist = etf.history(period="1mo")
        
        return {
            "sector": sector,
            "etf_ticker": etf_ticker,
            "change_1m": ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100,
            "current_price": hist['Close'].iloc[-1],
        }
    except Exception as e:
        return {"sector": sector, "error": str(e)}
