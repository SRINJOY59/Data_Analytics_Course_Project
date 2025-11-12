"""
Comprehensive Backtesting Script for AlphaAgents Portfolio
Supports multiple tickers, historical analysis, and performance metrics
"""
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import json
from pathlib import Path


class PortfolioBacktester:
    """Backtesting engine for portfolio strategies"""
    
    def __init__(self, initial_capital: float = 100000.0):
        """
        Initialize the backtester
        
        Args:
            initial_capital: Starting capital for the portfolio
        """
        self.initial_capital = initial_capital
        self.results = {}
        
    def fetch_historical_data(
        self, 
        tickers: List[str], 
        start_date: str, 
        end_date: str
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical price data for multiple tickers
        
        Args:
            tickers: List of stock ticker symbols
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            
        Returns:
            Dictionary mapping tickers to their historical data
        """
        print(f"\n{'='*60}")
        print(f"Fetching historical data for {len(tickers)} tickers")
        print(f"Period: {start_date} to {end_date}")
        print(f"{'='*60}\n")
        
        historical_data = {}
        
        for ticker in tickers:
            try:
                print(f"Downloading {ticker}...")
                stock = yf.Ticker(ticker)
                df = stock.history(start=start_date, end=end_date)
                
                if not df.empty:
                    historical_data[ticker] = df
                    print(f"✓ {ticker}: {len(df)} days of data")
                else:
                    print(f"✗ {ticker}: No data available")
                    
            except Exception as e:
                print(f"✗ {ticker}: Error - {str(e)}")
                
        return historical_data
    
    def calculate_returns(self, data: pd.DataFrame) -> pd.Series:
        """Calculate daily returns from price data"""
        return data['Close'].pct_change().dropna()
    
    def calculate_performance_metrics(
        self, 
        returns: pd.Series, 
        benchmark_returns: pd.Series = None
    ) -> Dict[str, float]:
        """
        Calculate comprehensive performance metrics
        
        Args:
            returns: Series of daily returns
            benchmark_returns: Optional benchmark returns for comparison
            
        Returns:
            Dictionary of performance metrics
        """
        # Basic return metrics
        total_return = (1 + returns).prod() - 1
        annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
        
        # Risk metrics
        volatility = returns.std() * np.sqrt(252)
        downside_returns = returns[returns < 0]
        downside_volatility = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        
        # Risk-adjusted metrics
        sharpe_ratio = annualized_return / volatility if volatility > 0 else 0
        sortino_ratio = annualized_return / downside_volatility if downside_volatility > 0 else 0
        
        # Drawdown analysis
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Win rate
        win_rate = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0
        
        metrics = {
            'total_return': total_return * 100,
            'annualized_return': annualized_return * 100,
            'volatility': volatility * 100,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown * 100,
            'win_rate': win_rate * 100,
            'best_day': returns.max() * 100,
            'worst_day': returns.min() * 100,
        }
        
        # Add benchmark comparison if provided
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            aligned_returns = returns.align(benchmark_returns, join='inner')[0]
            aligned_benchmark = returns.align(benchmark_returns, join='inner')[1]
            
            if len(aligned_returns) > 0:
                correlation = aligned_returns.corr(aligned_benchmark)
                excess_returns = aligned_returns - aligned_benchmark
                tracking_error = excess_returns.std() * np.sqrt(252)
                information_ratio = excess_returns.mean() * 252 / tracking_error if tracking_error > 0 else 0
                
                benchmark_total = (1 + benchmark_returns).prod() - 1
                
                metrics['correlation_to_benchmark'] = correlation
                metrics['tracking_error'] = tracking_error * 100
                metrics['information_ratio'] = information_ratio
                metrics['alpha'] = (total_return - benchmark_total) * 100
        
        return metrics
    
    def backtest_equal_weight_portfolio(
        self,
        tickers: List[str],
        start_date: str,
        end_date: str,
        benchmark: str = "SPY",
        rebalance_frequency: str = "monthly"
    ) -> Dict[str, Any]:
        """
        Backtest an equal-weight portfolio strategy
        
        Args:
            tickers: List of stock tickers
            start_date: Start date for backtest
            end_date: End date for backtest
            benchmark: Benchmark ticker (default: SPY)
            rebalance_frequency: How often to rebalance ('daily', 'weekly', 'monthly', 'quarterly')
            
        Returns:
            Dictionary with backtest results
        """
        print(f"\n{'='*60}")
        print(f"BACKTESTING EQUAL-WEIGHT PORTFOLIO")
        print(f"{'='*60}")
        print(f"Tickers: {', '.join(tickers)}")
        print(f"Period: {start_date} to {end_date}")
        print(f"Rebalance: {rebalance_frequency}")
        print(f"{'='*60}\n")
        
        # Fetch data
        all_tickers = tickers + [benchmark]
        historical_data = self.fetch_historical_data(all_tickers, start_date, end_date)
        
        if len(historical_data) < len(tickers):
            print(f"\n⚠️  Warning: Only {len(historical_data)} out of {len(tickers)} tickers have data")
        
        # Get benchmark data
        benchmark_data = historical_data.pop(benchmark, None)
        
        # Create combined price dataframe
        prices = pd.DataFrame({
            ticker: data['Close'] 
            for ticker, data in historical_data.items()
        })
        
        # Forward fill and drop any remaining NaN
        prices = prices.fillna(method='ffill').dropna()
        
        if prices.empty:
            print("❌ Error: No overlapping data for the tickers")
            return {}
        
        print(f"\n✓ Combined data: {len(prices)} days, {len(prices.columns)} tickers")
        
        # Calculate daily returns for each stock
        returns = prices.pct_change().dropna()
        
        # Equal weight portfolio returns
        portfolio_returns = returns.mean(axis=1)
        
        # Calculate portfolio value over time
        portfolio_value = self.initial_capital * (1 + portfolio_returns).cumprod()
        
        # Calculate metrics
        metrics = self.calculate_performance_metrics(
            portfolio_returns,
            self.calculate_returns(benchmark_data) if benchmark_data is not None else None
        )
        
        # Individual stock performance
        individual_metrics = {}
        for ticker in prices.columns:
            stock_returns = returns[ticker]
            individual_metrics[ticker] = self.calculate_performance_metrics(stock_returns)
        
        # Correlation matrix
        correlation_matrix = returns.corr()
        
        results = {
            'portfolio_metrics': metrics,
            'individual_metrics': individual_metrics,
            'portfolio_returns': portfolio_returns,
            'portfolio_value': portfolio_value,
            'final_value': portfolio_value.iloc[-1],
            'total_return_pct': ((portfolio_value.iloc[-1] / self.initial_capital) - 1) * 100,
            'correlation_matrix': correlation_matrix,
            'tickers': list(prices.columns),
            'start_date': start_date,
            'end_date': end_date,
            'trading_days': len(prices)
        }
        
        self.results = results
        return results
    
    def backtest_weighted_portfolio(
        self,
        portfolio_weights: Dict[str, float],
        start_date: str,
        end_date: str,
        benchmark: str = "SPY"
    ) -> Dict[str, Any]:
        """
        Backtest a custom weighted portfolio
        
        Args:
            portfolio_weights: Dictionary mapping tickers to weights (should sum to 1.0)
            start_date: Start date for backtest
            end_date: End date for backtest
            benchmark: Benchmark ticker
            
        Returns:
            Dictionary with backtest results
        """
        print(f"\n{'='*60}")
        print(f"BACKTESTING WEIGHTED PORTFOLIO")
        print(f"{'='*60}")
        print(f"Weights: {json.dumps(portfolio_weights, indent=2)}")
        print(f"Period: {start_date} to {end_date}")
        print(f"{'='*60}\n")
        
        # Validate weights
        total_weight = sum(portfolio_weights.values())
        if abs(total_weight - 1.0) > 0.01:
            print(f"⚠️  Warning: Weights sum to {total_weight:.2f}, normalizing...")
            portfolio_weights = {k: v/total_weight for k, v in portfolio_weights.items()}
        
        # Fetch data
        tickers = list(portfolio_weights.keys())
        all_tickers = tickers + [benchmark]
        historical_data = self.fetch_historical_data(all_tickers, start_date, end_date)
        
        # Get benchmark data
        benchmark_data = historical_data.pop(benchmark, None)
        
        # Create combined price dataframe
        prices = pd.DataFrame({
            ticker: data['Close'] 
            for ticker, data in historical_data.items()
        })
        
        prices = prices.fillna(method='ffill').dropna()
        
        if prices.empty:
            print("❌ Error: No overlapping data for the tickers")
            return {}
        
        print(f"\n✓ Combined data: {len(prices)} days, {len(prices.columns)} tickers")
        
        # Calculate returns
        returns = prices.pct_change().dropna()
        
        # Weighted portfolio returns
        portfolio_returns = sum(
            returns[ticker] * portfolio_weights.get(ticker, 0) 
            for ticker in returns.columns
        )
        
        # Portfolio value over time
        portfolio_value = self.initial_capital * (1 + portfolio_returns).cumprod()
        
        # Calculate metrics
        metrics = self.calculate_performance_metrics(
            portfolio_returns,
            self.calculate_returns(benchmark_data) if benchmark_data is not None else None
        )
        
        # Individual stock performance
        individual_metrics = {}
        for ticker in prices.columns:
            stock_returns = returns[ticker]
            individual_metrics[ticker] = self.calculate_performance_metrics(stock_returns)
        
        results = {
            'portfolio_metrics': metrics,
            'individual_metrics': individual_metrics,
            'portfolio_weights': portfolio_weights,
            'portfolio_returns': portfolio_returns,
            'portfolio_value': portfolio_value,
            'final_value': portfolio_value.iloc[-1],
            'total_return_pct': ((portfolio_value.iloc[-1] / self.initial_capital) - 1) * 100,
            'correlation_matrix': returns.corr(),
            'tickers': list(prices.columns),
            'start_date': start_date,
            'end_date': end_date,
            'trading_days': len(prices)
        }
        
        self.results = results
        return results
    
    def print_results(self, results: Dict[str, Any] = None):
        """Print formatted backtest results"""
        if results is None:
            results = self.results
            
        if not results:
            print("No results to display")
            return
        
        print(f"\n{'='*60}")
        print(f"BACKTEST RESULTS SUMMARY")
        print(f"{'='*60}\n")
        
        # Portfolio overview
        print(f"Period: {results['start_date']} to {results['end_date']}")
        print(f"Trading Days: {results['trading_days']}")
        print(f"Tickers: {', '.join(results['tickers'])}\n")
        
        # Portfolio performance
        print(f"{'='*60}")
        print(f"PORTFOLIO PERFORMANCE")
        print(f"{'='*60}")
        
        metrics = results['portfolio_metrics']
        print(f"Initial Capital:        ${self.initial_capital:,.2f}")
        print(f"Final Value:            ${results['final_value']:,.2f}")
        print(f"Total Return:           {metrics['total_return']:.2f}%")
        print(f"Annualized Return:      {metrics['annualized_return']:.2f}%")
        print(f"Volatility:             {metrics['volatility']:.2f}%")
        print(f"Sharpe Ratio:           {metrics['sharpe_ratio']:.2f}")
        print(f"Sortino Ratio:          {metrics['sortino_ratio']:.2f}")
        print(f"Max Drawdown:           {metrics['max_drawdown']:.2f}%")
        print(f"Win Rate:               {metrics['win_rate']:.2f}%")
        print(f"Best Day:               {metrics['best_day']:.2f}%")
        print(f"Worst Day:              {metrics['worst_day']:.2f}%")
        
        if 'alpha' in metrics:
            print(f"\nBenchmark Comparison:")
            print(f"Alpha:                  {metrics['alpha']:.2f}%")
            print(f"Correlation:            {metrics['correlation_to_benchmark']:.2f}")
            print(f"Information Ratio:      {metrics['information_ratio']:.2f}")
        
        # Individual stock performance
        print(f"\n{'='*60}")
        print(f"INDIVIDUAL STOCK PERFORMANCE")
        print(f"{'='*60}\n")
        
        print(f"{'Ticker':<8} {'Return':<10} {'Volatility':<12} {'Sharpe':<10} {'Max DD':<10}")
        print(f"{'-'*60}")
        
        for ticker, stock_metrics in results['individual_metrics'].items():
            print(f"{ticker:<8} "
                  f"{stock_metrics['total_return']:>8.2f}%  "
                  f"{stock_metrics['volatility']:>10.2f}%  "
                  f"{stock_metrics['sharpe_ratio']:>8.2f}  "
                  f"{stock_metrics['max_drawdown']:>8.2f}%")
        
        # Portfolio weights if available
        if 'portfolio_weights' in results:
            print(f"\n{'='*60}")
            print(f"PORTFOLIO WEIGHTS")
            print(f"{'='*60}\n")
            for ticker, weight in results['portfolio_weights'].items():
                print(f"{ticker:<8} {weight*100:>6.2f}%")
        
        print(f"\n{'='*60}\n")
    
    def save_results(self, filename: str = "backtest_results.json"):
        """Save results to JSON file"""
        if not self.results:
            print("No results to save")
            return
        
        # Convert non-serializable objects
        save_data = {
            'portfolio_metrics': self.results['portfolio_metrics'],
            'individual_metrics': self.results['individual_metrics'],
            'portfolio_weights': self.results.get('portfolio_weights', {}),
            'final_value': self.results['final_value'],
            'total_return_pct': self.results['total_return_pct'],
            'tickers': self.results['tickers'],
            'start_date': self.results['start_date'],
            'end_date': self.results['end_date'],
            'trading_days': self.results['trading_days'],
            'correlation_matrix': self.results['correlation_matrix'].to_dict()
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"✓ Results saved to {filename}")


def run_example_backtest():
    """Run an example backtest"""
    
    # Define test parameters
    tickers = [
        "AAPL",  # Apple
        "MSFT",  # Microsoft
        "GOOGL", # Google
        "NVDA",  # NVIDIA
        "JPM",   # JPMorgan
        "JNJ",   # Johnson & Johnson
        "V",     # Visa
        "PG",    # Procter & Gamble
    ]
    
    # Date range - last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # ~2 years
    
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    # Initialize backtester
    backtester = PortfolioBacktester(initial_capital=100000)
    
    # Run equal-weight backtest
    print("\n" + "="*60)
    print("EXAMPLE 1: EQUAL-WEIGHT PORTFOLIO")
    print("="*60)
    
    results = backtester.backtest_equal_weight_portfolio(
        tickers=tickers,
        start_date=start_str,
        end_date=end_str,
        benchmark="SPY"
    )
    
    backtester.print_results(results)
    backtester.save_results("equal_weight_results.json")
    
    # Run weighted portfolio backtest
    print("\n" + "="*60)
    print("EXAMPLE 2: CUSTOM-WEIGHTED PORTFOLIO")
    print("="*60)
    
    custom_weights = {
        "AAPL": 0.20,
        "MSFT": 0.20,
        "GOOGL": 0.15,
        "NVDA": 0.15,
        "JPM": 0.10,
        "JNJ": 0.10,
        "V": 0.05,
        "PG": 0.05,
    }
    
    backtester2 = PortfolioBacktester(initial_capital=100000)
    results2 = backtester2.backtest_weighted_portfolio(
        portfolio_weights=custom_weights,
        start_date=start_str,
        end_date=end_str,
        benchmark="SPY"
    )
    
    backtester2.print_results(results2)
    backtester2.save_results("weighted_portfolio_results.json")


if __name__ == "__main__":
    run_example_backtest()
