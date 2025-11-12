"""
Utility for formatting portfolio output in a readable format
"""
from schemas import PortfolioOutput
from typing import Any


def format_portfolio_output(portfolio: PortfolioOutput) -> str:
    """
    Format portfolio output in a clean, readable format
    
    Args:
        portfolio: PortfolioOutput object to format
        
    Returns:
        Formatted string representation
    """
    lines = []
    lines.append("\n" + "="*80)
    lines.append(f"PORTFOLIO: {portfolio.portfolio_name}")
    lines.append(f"Created: {portfolio.creation_date}")
    lines.append("="*80)
    
    # Executive Summary
    lines.append("\n📊 EXECUTIVE SUMMARY")
    lines.append("-" * 80)
    lines.append(portfolio.executive_summary)
    
    # Portfolio Holdings
    lines.append("\n\n💼 PORTFOLIO HOLDINGS")
    lines.append("-" * 80)
    lines.append(f"{'#':<4} {'Ticker':<8} {'Company':<30} {'Sector':<20} {'Allocation':>10}")
    lines.append("-" * 80)
    
    for i, holding in enumerate(portfolio.holdings, 1):
        lines.append(
            f"{i:<4} {holding.ticker:<8} {holding.company_name:<30} "
            f"{holding.sector:<20} {holding.allocation:>9.1f}%"
        )
    
    lines.append("-" * 80)
    lines.append(f"{'TOTAL':<62} {portfolio.characteristics.total_allocation:>9.1f}%")
    
    # Holdings Details
    lines.append("\n\n📝 HOLDINGS RATIONALE")
    lines.append("-" * 80)
    for holding in portfolio.holdings:
        lines.append(f"\n🔹 {holding.ticker} - {holding.company_name}")
        lines.append(f"   Allocation: {holding.allocation}%")
        lines.append(f"   Rationale: {holding.rationale}")
        lines.append(f"   Entry: {holding.entry_criteria}")
        lines.append(f"   Exit: {holding.exit_criteria}")
    
    # Portfolio Characteristics
    lines.append("\n\n📈 PORTFOLIO CHARACTERISTICS")
    lines.append("-" * 80)
    lines.append(f"Number of Holdings: {portfolio.characteristics.number_of_holdings}")
    lines.append(f"Expected Return: {portfolio.characteristics.expected_return}")
    lines.append(f"Risk Level: {portfolio.characteristics.risk_level.upper()}")
    lines.append(f"Largest Sector: {portfolio.characteristics.largest_sector}")
    
    # Sector Breakdown
    lines.append("\n\n🏢 SECTOR ALLOCATION")
    lines.append("-" * 80)
    for sector in portfolio.characteristics.sector_breakdown:
        bar_length = int(sector.percentage / 2)  # Scale to fit
        bar = "█" * bar_length
        lines.append(f"{sector.sector:<25} {sector.percentage:>6.1f}% {bar}")
    
    # Investment Strategy
    lines.append("\n\n🎯 INVESTMENT STRATEGY")
    lines.append("-" * 80)
    lines.append(portfolio.investment_strategy)
    
    # Rebalancing
    lines.append("\n\n🔄 REBALANCING GUIDELINES")
    lines.append("-" * 80)
    lines.append(f"Frequency: {portfolio.rebalancing.frequency}")
    lines.append(f"Threshold: {portfolio.rebalancing.threshold}")
    lines.append("\nTriggers:")
    for trigger in portfolio.rebalancing.triggers:
        lines.append(f"  • {trigger}")
    
    # Monitoring Points
    lines.append("\n\n👀 MONITORING POINTS")
    lines.append("-" * 80)
    for point in portfolio.monitoring_points:
        lines.append(f"  • {point}")
    
    # Risks
    lines.append("\n\n⚠️  KEY RISKS")
    lines.append("-" * 80)
    for risk in portfolio.key_risks:
        lines.append(f"  • {risk}")
    
    # Assumptions
    lines.append("\n\n💡 KEY ASSUMPTIONS")
    lines.append("-" * 80)
    for assumption in portfolio.key_assumptions:
        lines.append(f"  • {assumption}")
    
    # Market Conditions
    lines.append("\n\n🌍 MARKET CONDITIONS")
    lines.append("-" * 80)
    lines.append(portfolio.market_conditions)
    
    lines.append("\n" + "="*80 + "\n")
    
    return "\n".join(lines)


def print_portfolio(portfolio: PortfolioOutput) -> None:
    """
    Print formatted portfolio output to console
    
    Args:
        portfolio: PortfolioOutput object to print
    """
    print(format_portfolio_output(portfolio))
