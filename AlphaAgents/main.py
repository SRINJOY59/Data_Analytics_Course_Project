"""
AlphaAgents - AI-Powered Portfolio Construction System
Main execution script
"""
from workflow.portfolio_workflow import AlphaAgentsWorkflow
from utils.portfolio_formatter import print_portfolio
import json
from datetime import datetime


def run_alphaagents(
    stock_universe=None,
    risk_tolerance="moderate",
    investment_horizon="long_term",
    portfolio_size=10,
    save_results=True
):
    """
    Run the AlphaAgents portfolio construction system
    
    Args:
        stock_universe: List of stock tickers to analyze
        risk_tolerance: Risk level (low, moderate, high)
        investment_horizon: Time horizon (short_term, medium_term, long_term)
        portfolio_size: Number of stocks in final portfolio
        save_results: Whether to save results to JSON file
    
    Returns:
        dict: Complete results from all agents
    """
    
    # Default stock universe if not provided
    if stock_universe is None:
        stock_universe = [
            # Technology
            "AAPL", "MSFT", "GOOGL", "NVDA",
            # Financials
            "JPM", "V", "MA",
            # Healthcare
            "JNJ", "UNH",
            # Consumer
            "AMZN", "WMT", "PG",
            # Energy & Others
            "XOM", "DIS", "TSLA"
        ]
    
    print("="*70)
    print("ALPHAAGENTS - AI PORTFOLIO CONSTRUCTION")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  Stock Universe: {len(stock_universe)} stocks")
    print(f"  Risk Tolerance: {risk_tolerance}")
    print(f"  Investment Horizon: {investment_horizon}")
    print(f"  Portfolio Size: {portfolio_size}")
    print("="*70)
    
    # Initialize and run workflow
    workflow = AlphaAgentsWorkflow()
    
    try:
        results = workflow.run(
            stock_universe=stock_universe,
            risk_tolerance=risk_tolerance,
            investment_horizon=investment_horizon,
            portfolio_size=portfolio_size,
        )
        
        # Display the final portfolio
        print("\n" + "="*70)
        print("FINAL PORTFOLIO RECOMMENDATION")
        print("="*70)
        
        portfolio_data = results["portfolio"]["data"]
        
        if portfolio_data and not isinstance(portfolio_data, str):
            print_portfolio(portfolio_data)
        else:
            print("\n⚠️  Portfolio returned as text:")
            print(results["portfolio"]["summary"])
        
        # Save results if requested
        if save_results:
            filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Extract portfolio for saving
            portfolio_summary = {
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'parameters': {
                    'stock_universe': stock_universe,
                    'risk_tolerance': risk_tolerance,
                    'investment_horizon': investment_horizon,
                    'portfolio_size': portfolio_size
                },
                'portfolio_summary': results["portfolio"]["summary"]
            }
            
            # Add structured data if available
            if portfolio_data and hasattr(portfolio_data, 'model_dump'):
                portfolio_summary['portfolio'] = portfolio_data.model_dump()
            
            with open(filename, 'w') as f:
                json.dump(portfolio_summary, f, indent=2)
            
            print(f"\n✅ Results saved to '{filename}'")
        
        print("\n" + "="*70)
        print("✅ PORTFOLIO GENERATION COMPLETE")
        print("="*70 + "\n")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main entry point"""
    
    # Customize your portfolio parameters here
    stock_universe = [
        "AAPL",  # Technology - Apple
        "MSFT",  # Technology - Microsoft
        "GOOGL", # Communication - Google
        "NVDA",  # Technology - NVIDIA
        "JPM",   # Financials - JPMorgan
        "JNJ",   # Healthcare - Johnson & Johnson
        "V",     # Financials - Visa
        "PG",    # Consumer Staples - Procter & Gamble
        "XOM",   # Energy - Exxon Mobil
        "DIS",   # Communication - Disney
        "TSLA",  # Automotive/Tech - Tesla
        "WMT",   # Consumer Staples - Walmart
    ]
    
    results = run_alphaagents(
        stock_universe=stock_universe,
        risk_tolerance="moderate",      # Options: low, moderate, high
        investment_horizon="long_term", # Options: short_term, medium_term, long_term
        portfolio_size=8,               # Number of stocks to include
        save_results=True
    )
    
    return results


if __name__ == "__main__":
    main()
