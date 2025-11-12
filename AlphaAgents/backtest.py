"""
Backtest AlphaAgents AI-Generated Portfolio
"""
from workflow.portfolio_workflow import AlphaAgentsWorkflow
from backtesting import PortfolioBacktester
from datetime import datetime, timedelta
from utils.portfolio_formatter import print_portfolio
import json


def run_backtest(
    stock_universe=None,
    risk_tolerance="moderate",
    investment_horizon="long_term",
    portfolio_size=10,
    initial_capital=100000,
    backtest_years=2,
    benchmark="SPY"
):
    """
    Complete workflow: Generate AI portfolio and backtest it
    
    Args:
        stock_universe: List of stock tickers to analyze
        risk_tolerance: Risk level (low, moderate, high)
        investment_horizon: Time horizon (short_term, medium_term, long_term)
        portfolio_size: Number of stocks in final portfolio
        initial_capital: Starting capital for backtest
        backtest_years: Number of years to backtest
        benchmark: Benchmark ticker (default: SPY)
    
    Returns:
        dict: Complete results including AI portfolio and backtest metrics
    """
    
    # Default stock universe if not provided
    if stock_universe is None:
        stock_universe = [
            # Technology
            "AAPL", "MSFT", "GOOGL", "NVDA", "META", "ADBE",
            # Financials
            "JPM", "BAC", "V", "MA", "GS",
            # Healthcare
            "JNJ", "UNH", "PFE", "ABBV", "TMO",
            # Consumer
            "AMZN", "TSLA", "HD", "NKE", "WMT", "PG",
            # Energy
            "XOM", "CVX", "COP",
            # Communication
            "DIS", "NFLX", "CMCSA",
        ]
    
    print("="*70)
    print("ALPHAAGENTS AI PORTFOLIO BACKTESTING")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  Stock Universe: {len(stock_universe)} stocks")
    print(f"  Risk Tolerance: {risk_tolerance}")
    print(f"  Investment Horizon: {investment_horizon}")
    print(f"  Portfolio Size: {portfolio_size}")
    print(f"  Initial Capital: ${initial_capital:,}")
    print(f"  Backtest Period: {backtest_years} years")
    print(f"  Benchmark: {benchmark}")
    
    # STEP 1: Generate AI Portfolio
    print(f"\n{'='*70}")
    print("STEP 1: GENERATING AI PORTFOLIO")
    print(f"{'='*70}\n")
    print("⏳ Running AlphaAgents (this may take a few minutes)...\n")
    
    workflow = AlphaAgentsWorkflow()
    
    try:
        ai_results = workflow.run(
            stock_universe=stock_universe,
            risk_tolerance=risk_tolerance,
            investment_horizon=investment_horizon,
            portfolio_size=portfolio_size,
        )
        
        # Display AI portfolio
        print(f"\n{'='*70}")
        print("✅ AI PORTFOLIO GENERATED")
        print(f"{'='*70}")
        
        portfolio_data = ai_results["portfolio"]["data"]
        
        if portfolio_data and not isinstance(portfolio_data, str):
            print_portfolio(portfolio_data)
        else:
            print("\n⚠️  Portfolio returned as text")
            print(ai_results["portfolio"]["summary"])
        
        # Extract weights from AI portfolio
        ai_weights = extract_weights_from_portfolio(portfolio_data)
        
        if not ai_weights:
            print("\n❌ Error: Could not extract portfolio weights")
            return None
        
        # Normalize weights
        total = sum(ai_weights.values())
        if abs(total - 1.0) > 0.01:
            print(f"\n⚠️  Normalizing weights (sum was {total:.3f})")
            ai_weights = {k: v/total for k, v in ai_weights.items()}
        
        print(f"\n📋 Extracted Portfolio Weights:")
        for ticker, weight in ai_weights.items():
            print(f"   {ticker}: {weight*100:.1f}%")
        
    except Exception as e:
        print(f"\n❌ Error generating AI portfolio: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # STEP 2: Backtest the AI Portfolio
    print(f"\n{'='*70}")
    print("STEP 2: BACKTESTING AI PORTFOLIO")
    print(f"{'='*70}\n")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=backtest_years*365)
    
    # Run backtest
    backtester = PortfolioBacktester(initial_capital=initial_capital)
    
    backtest_results = backtester.backtest_weighted_portfolio(
        portfolio_weights=ai_weights,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        benchmark=benchmark
    )
    
    if not backtest_results:
        print("\n❌ Backtesting failed. Check if tickers have sufficient historical data.")
        return None
    
    # Display backtest results
    backtester.print_results(backtest_results)
    
    # STEP 3: Summary and Save
    print(f"\n{'='*70}")
    print("📊 FINAL SUMMARY")
    print(f"{'='*70}")
    
    metrics = backtest_results['portfolio_metrics']
    final_value = backtest_results['final_value']
    profit = final_value - initial_capital
    
    print(f"\nInvestment:     ${initial_capital:,.2f}")
    print(f"Final Value:    ${final_value:,.2f}")
    print(f"Profit/Loss:    ${profit:,.2f}")
    print(f"Return:         {metrics['total_return']:.2f}%")
    print(f"Sharpe Ratio:   {metrics['sharpe_ratio']:.2f}")
    
    if 'alpha' in metrics:
        print(f"Alpha vs {benchmark}:  {metrics['alpha']:.2f}%")
    
    # Performance rating
    sharpe = metrics['sharpe_ratio']
    if sharpe > 2.0:
        rating = "🌟 EXCELLENT"
    elif sharpe > 1.0:
        rating = "✅ GOOD"
    elif sharpe > 0.5:
        rating = "⚠️  FAIR"
    else:
        rating = "❌ POOR"
    
    print(f"\nPerformance:    {rating}")
    
    # Save complete results
    results_to_save = {
        'ai_portfolio': {
            'tickers': list(ai_weights.keys()),
            'weights': ai_weights,
            'risk_tolerance': risk_tolerance,
            'investment_horizon': investment_horizon,
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        'backtest': {
            'metrics': backtest_results['portfolio_metrics'],
            'final_value': final_value,
            'initial_capital': initial_capital,
            'profit_loss': profit,
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'benchmark': benchmark
        }
    }
    
    filename = f"backtest_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results_to_save, f, indent=2)
    
    print(f"\n✅ Results saved to '{filename}'")
    print(f"{'='*70}\n")
    
    return {
        'ai_results': ai_results,
        'backtest_results': backtest_results,
        'ai_weights': ai_weights,
        'filename': filename
    }


def extract_weights_from_portfolio(portfolio_data):
    """
    Extract portfolio weights from AI-generated portfolio data
    
    Args:
        portfolio_data: Portfolio data from AlphaAgents
    
    Returns:
        dict: Ticker to weight mapping
    """
    if not portfolio_data or isinstance(portfolio_data, str):
        return None
    
    # Try to find holdings
    holdings = None
    if hasattr(portfolio_data, 'holdings'):
        holdings = portfolio_data.holdings
    elif hasattr(portfolio_data, 'allocations'):
        holdings = portfolio_data.allocations
    
    if not holdings:
        return None
    
    # Extract weights
    weights = {}
    for holding in holdings:
        ticker = holding.ticker
        
        # Try different weight field names
        if hasattr(holding, 'allocation'):
            weight = holding.allocation / 100.0
        elif hasattr(holding, 'weight_percent'):
            weight = holding.weight_percent / 100.0
        elif hasattr(holding, 'weight'):
            weight = holding.weight / 100.0 if holding.weight > 1 else holding.weight
        else:
            weight = 1.0 / len(holdings)  # Equal weight fallback
        
        weights[ticker] = weight
    
    return weights


def main():
    """Main entry point for backtesting"""
    
    # Configuration - customize these parameters
    stock_universe = [
        # Technology
        "AAPL", "MSFT", "GOOGL", "NVDA", "META",
        # Financials
        "JPM", "BAC", "V", "MA",
        # Healthcare
        "JNJ", "UNH", "PFE",
        # Consumer
        "AMZN", "TSLA", "WMT", "HD",
        # Energy & Others
        "XOM", "CVX", "DIS"
    ]
    
    results = run_backtest(
        stock_universe=stock_universe,
        risk_tolerance="moderate",      # low, moderate, high
        investment_horizon="long_term", # short_term, medium_term, long_term
        portfolio_size=10,              # Number of stocks to select
        initial_capital=100000,         # $100k
        backtest_years=2,               # Test last 2 years
        benchmark="SPY"                 # S&P 500
    )
    
    return results


if __name__ == "__main__":
    main()
