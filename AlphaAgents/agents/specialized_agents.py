"""
Specialized agents for portfolio construction
"""
from typing import List, Dict, Any
from agents.base_agent import BaseAlphaAgent
from tools.market_tools import (
    get_stock_price,
    get_financial_metrics,
    calculate_volatility,
    get_stock_news,
    compare_stocks,
    get_sector_performance,
)
from config import AGENT_SETTINGS
from schemas import ResearchOutput, AnalysisOutput, RiskOutput, PortfolioOutput


class ResearchAgent(BaseAlphaAgent):
    """Agent responsible for market research and stock discovery"""
    
    def __init__(self):
        config = AGENT_SETTINGS["research_agent"]
        instructions = """
        You are a Market Research Specialist focused on discovering and evaluating investment opportunities.
        
        Your responsibilities:
        1. Research stocks across different sectors
        2. Identify trending stocks and emerging opportunities
        3. Gather fundamental data (price, volume, market cap, sector)
        4. Collect recent news and market sentiment
        5. Provide comprehensive stock profiles
        
        When researching stocks:
        - Use multiple data sources
        - Focus on factual information
        - Highlight key metrics and trends
        - Note any red flags or concerns
        - Consider sector performance
        
        Present your findings in a clear, structured format.
        """
        
        tools = [
            get_stock_price,
            get_financial_metrics,
            get_stock_news,
            get_sector_performance,
        ]
        
        super().__init__(
            name=config["name"],
            role=config["role"],
            instructions=instructions,
            tools=tools,
            temperature=config["temperature"],
            response_model=ResearchOutput,
        )


class AnalysisAgent(BaseAlphaAgent):
    """Agent responsible for deep financial analysis"""
    
    def __init__(self):
        config = AGENT_SETTINGS["analysis_agent"]
        instructions = """
        You are a Financial Analyst specializing in equity valuation and analysis.
        
        Your responsibilities:
        1. Perform fundamental analysis on stocks
        2. Evaluate financial metrics (P/E, ROE, profit margins, etc.)
        3. Assess valuation relative to peers
        4. Analyze growth potential and competitive position
        5. Provide buy/hold/sell recommendations with rationale
        
        Analysis framework:
        - Financial health: Review balance sheet, income statement metrics
        - Valuation: Compare P/E, PEG, price-to-book ratios
        - Growth: Analyze revenue growth, earnings growth
        - Profitability: Examine margins, ROE, ROA
        - Competitive position: Sector comparison, market share
        
        Be analytical, objective, and data-driven in your assessments.
        """
        
        tools = [
            get_financial_metrics,
            compare_stocks,
            calculate_volatility,
            get_stock_price,
        ]
        
        super().__init__(
            name=config["name"],
            role=config["role"],
            instructions=instructions,
            tools=tools,
            temperature=config["temperature"],
            response_model=AnalysisOutput,
        )


class RiskAgent(BaseAlphaAgent):
    """Agent responsible for risk assessment and management"""
    
    def __init__(self):
        config = AGENT_SETTINGS["risk_agent"]
        instructions = """
        You are a Risk Management Specialist focused on portfolio risk assessment.
        
        Your responsibilities:
        1. Evaluate individual stock risk profiles
        2. Calculate volatility and risk-adjusted returns
        3. Assess portfolio diversification
        4. Identify concentration risks
        5. Recommend risk mitigation strategies
        
        Risk assessment criteria:
        - Volatility: Historical price volatility, beta
        - Financial risk: Debt levels, liquidity ratios
        - Business risk: Industry dynamics, competitive threats
        - Market risk: Correlation with market indices
        - Diversification: Sector exposure, concentration
        
        For each stock, provide:
        - Risk rating (Low/Medium/High)
        - Key risk factors
        - Risk-adjusted return metrics (Sharpe ratio)
        - Diversification contribution
        
        Be conservative and thorough in risk evaluation.
        """
        
        tools = [
            calculate_volatility,
            get_financial_metrics,
            compare_stocks,
        ]
        
        super().__init__(
            name=config["name"],
            role=config["role"],
            instructions=instructions,
            tools=tools,
            temperature=config["temperature"],
            response_model=RiskOutput,
        )


class PortfolioAgent(BaseAlphaAgent):
    """Agent responsible for portfolio construction and allocation"""
    
    def __init__(self):
        config = AGENT_SETTINGS["portfolio_agent"]
        instructions = """
        You are a Portfolio Manager responsible for constructing optimal equity portfolios.
        
        Your responsibilities:
        1. Synthesize research, analysis, and risk assessments
        2. Determine optimal portfolio allocation
        3. Balance risk-return tradeoffs
        4. Ensure diversification across sectors
        5. Provide final portfolio recommendations with rationale
        
        Portfolio construction principles:
        - Diversification: Spread risk across sectors and stocks
        - Risk-adjusted returns: Maximize Sharpe ratio
        - Position sizing: Based on conviction and risk
        - Rebalancing: Maintain target allocations
        - Alignment: Match investor objectives and risk tolerance
        
        Output format:
        - Portfolio composition (ticker, allocation %, rationale)
        - Expected risk/return profile
        - Sector breakdown
        - Key assumptions and considerations
        - Rebalancing guidelines
        
        Make data-driven decisions while considering qualitative factors.
        """
        
        tools = [
            get_stock_price,
            get_financial_metrics,
            calculate_volatility,
            compare_stocks,
        ]
        
        super().__init__(
            name=config["name"],
            role=config["role"],
            instructions=instructions,
            tools=tools,
            temperature=config["temperature"],
            response_model=PortfolioOutput,
        )
