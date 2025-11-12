"""
Pydantic schemas for structured outputs from AlphaAgents
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# ==================== Stock Research Schemas ====================

class StockPrice(BaseModel):
    """Stock price information"""
    ticker: str = Field(description="Stock ticker symbol")
    current_price: float = Field(description="Current stock price")
    change_percent: float = Field(description="Percentage change")
    volume: int = Field(description="Trading volume")
    market_cap: Optional[str] = Field(default=None, description="Market capitalization")


class StockNews(BaseModel):
    """News item for a stock"""
    title: str = Field(description="News headline")
    sentiment: Literal["positive", "negative", "neutral"] = Field(description="Sentiment analysis")
    relevance: Literal["high", "medium", "low"] = Field(description="Relevance to investment decision")


class StockResearch(BaseModel):
    """Research findings for a single stock"""
    ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Company name")
    sector: str = Field(description="Business sector")
    industry: str = Field(description="Industry classification")
    current_price: float = Field(description="Current stock price")
    market_cap: str = Field(description="Market capitalization")
    pe_ratio: Optional[float] = Field(default=None, description="P/E ratio")
    key_metrics: str = Field(description="Summary of key financial metrics")
    recent_performance: str = Field(description="Recent price performance summary")
    news_summary: str = Field(description="Summary of recent news and developments")
    sector_outlook: str = Field(description="Sector performance and outlook")


class ResearchOutput(BaseModel):
    """Complete research output for all stocks"""
    stocks: List[StockResearch] = Field(description="Research for each stock")
    market_overview: str = Field(description="Overall market conditions and context")
    key_findings: List[str] = Field(description="Key findings from research")


# ==================== Financial Analysis Schemas ====================

class FinancialMetrics(BaseModel):
    """Financial metrics for analysis"""
    revenue_growth: Optional[float] = Field(default=None, description="Revenue growth rate (%)")
    profit_margin: Optional[float] = Field(default=None, description="Profit margin (%)")
    roe: Optional[float] = Field(default=None, description="Return on Equity (%)")
    debt_to_equity: Optional[float] = Field(default=None, description="Debt to Equity ratio")
    current_ratio: Optional[float] = Field(default=None, description="Current ratio")
    eps: Optional[float] = Field(default=None, description="Earnings per share")


class StockAnalysis(BaseModel):
    """Detailed analysis for a single stock"""
    ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Company name")
    
    # Fundamental Analysis
    financial_strength: Literal["strong", "moderate", "weak"] = Field(description="Overall financial strength")
    financial_metrics_summary: str = Field(description="Summary of key financial metrics")
    
    # Valuation
    valuation: Literal["undervalued", "fairly_valued", "overvalued"] = Field(description="Valuation assessment")
    valuation_rationale: str = Field(description="Rationale for valuation assessment")
    
    # Growth & Competitive Position
    growth_potential: Literal["high", "moderate", "low"] = Field(description="Growth potential")
    growth_drivers: List[str] = Field(description="Key growth drivers")
    competitive_position: str = Field(description="Competitive position in industry")
    
    # Recommendation
    recommendation: Literal["strong_buy", "buy", "hold", "sell", "strong_sell"] = Field(description="Investment recommendation")
    target_price: Optional[float] = Field(default=None, description="12-month target price")
    rationale: str = Field(description="Rationale for recommendation")
    
    # Score
    investment_score: int = Field(ge=1, le=10, description="Investment attractiveness score (1-10)")


class AnalysisOutput(BaseModel):
    """Complete analysis output for all stocks"""
    stocks: List[StockAnalysis] = Field(description="Analysis for each stock")
    ranked_stocks: List[str] = Field(description="Tickers ranked by investment attractiveness")
    top_picks: List[str] = Field(description="Top stock picks (tickers)")
    avoid_list: List[str] = Field(description="Stocks to avoid (tickers)")
    analysis_summary: str = Field(description="Overall analysis summary")


# ==================== Risk Assessment Schemas ====================

class StockRisk(BaseModel):
    """Risk assessment for a single stock"""
    ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Company name")
    
    # Risk Metrics
    volatility: float = Field(description="Annualized volatility (%)")
    beta: Optional[float] = Field(default=None, description="Beta (market correlation)")
    sharpe_ratio: Optional[float] = Field(default=None, description="Sharpe ratio")
    
    # Risk Categories
    market_risk: Literal["low", "medium", "high"] = Field(description="Market/systematic risk")
    financial_risk: Literal["low", "medium", "high"] = Field(description="Financial/credit risk")
    business_risk: Literal["low", "medium", "high"] = Field(description="Business/operational risk")
    
    # Overall Assessment
    overall_risk: Literal["low", "medium", "high"] = Field(description="Overall risk rating")
    risk_factors: List[str] = Field(description="Key risk factors")
    risk_mitigation: str = Field(description="Risk mitigation recommendations")


class SectorConcentration(BaseModel):
    """Sector concentration details"""
    sector: str = Field(description="Sector name")
    percentage: float = Field(description="Percentage allocation to this sector")


class PortfolioRisk(BaseModel):
    """Portfolio-level risk assessment"""
    sector_concentration: List[SectorConcentration] = Field(description="Sector concentration breakdown")
    correlation_risk: str = Field(description="Assessment of correlation between holdings")
    diversification_score: int = Field(ge=1, le=10, description="Diversification score (1-10)")
    key_risks: List[str] = Field(description="Key portfolio-level risks")
    mitigation_strategies: List[str] = Field(description="Risk mitigation strategies")


class RiskOutput(BaseModel):
    """Complete risk assessment output"""
    stocks: List[StockRisk] = Field(description="Risk assessment for each stock")
    portfolio_risk: PortfolioRisk = Field(description="Portfolio-level risk analysis")
    risk_summary: str = Field(description="Overall risk assessment summary")
    recommendations: List[str] = Field(description="Risk management recommendations")


# ==================== Portfolio Construction Schemas ====================

class PortfolioHolding(BaseModel):
    """Individual holding in the portfolio"""
    ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Company name")
    sector: str = Field(description="Business sector")
    allocation: float = Field(ge=0, le=100, description="Allocation percentage")
    shares: Optional[int] = Field(default=None, description="Number of shares (if calculated)")
    rationale: str = Field(description="Rationale for inclusion and allocation")
    entry_criteria: str = Field(description="Criteria for initial entry")
    exit_criteria: str = Field(description="Criteria for exit/sell")


class PortfolioCharacteristics(BaseModel):
    """Overall portfolio characteristics"""
    total_allocation: float = Field(description="Total allocation (should be 100%)")
    number_of_holdings: int = Field(description="Number of stocks in portfolio")
    
    # Sector Distribution
    sector_breakdown: List[SectorConcentration] = Field(description="Sector allocation breakdown")
    largest_sector: str = Field(description="Largest sector exposure")
    
    # Risk-Return Profile
    expected_return: str = Field(description="Expected annual return range (e.g., '8-12%')")
    risk_level: Literal["low", "moderate", "high"] = Field(description="Overall portfolio risk")
    estimated_volatility: Optional[float] = Field(default=None, description="Estimated portfolio volatility")
    estimated_sharpe: Optional[float] = Field(default=None, description="Estimated Sharpe ratio")


class RebalancingGuidelines(BaseModel):
    """Guidelines for portfolio rebalancing"""
    frequency: str = Field(description="Recommended rebalancing frequency")
    triggers: List[str] = Field(description="Conditions that trigger rebalancing")
    threshold: str = Field(description="Allocation drift threshold for rebalancing")


class PortfolioOutput(BaseModel):
    """Complete portfolio construction output"""
    portfolio_name: str = Field(description="Portfolio name/identifier")
    creation_date: str = Field(description="Portfolio creation date")
    
    # Holdings
    holdings: List[PortfolioHolding] = Field(description="Portfolio holdings with allocations")
    
    # Characteristics
    characteristics: PortfolioCharacteristics = Field(description="Portfolio characteristics")
    
    # Strategy & Guidelines
    investment_strategy: str = Field(description="Overall investment strategy")
    rebalancing: RebalancingGuidelines = Field(description="Rebalancing guidelines")
    monitoring_points: List[str] = Field(description="Key metrics/events to monitor")
    
    # Risks & Assumptions
    key_risks: List[str] = Field(description="Main portfolio risks")
    key_assumptions: List[str] = Field(description="Key assumptions made")
    market_conditions: str = Field(description="Current market conditions considered")
    
    # Summary
    executive_summary: str = Field(description="Executive summary of portfolio recommendation")
