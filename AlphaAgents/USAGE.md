# Quick Start Guide

## Two Main Scripts

### 1. `main.py` - Generate AI Portfolio

Runs the AlphaAgents pipeline to generate an optimized portfolio.

**Usage:**
```bash
python main.py
```

**What it does:**
- Analyzes your stock universe using 4 AI agents
- Generates optimal portfolio with recommended weights
- Saves results to `portfolio_YYYYMMDD_HHMMSS.json`

**Customize:**
```python
# Edit main.py
stock_universe = ["AAPL", "MSFT", "GOOGL", ...]
risk_tolerance = "moderate"      # low, moderate, high
investment_horizon = "long_term" # short_term, medium_term, long_term
portfolio_size = 8               # Number of stocks to select
```

---

### 2. `backtest.py` - Backtest AI Portfolio

Generates AI portfolio AND backtests it on historical data.

**Usage:**
```bash
python backtest.py
```

**What it does:**
- Runs AlphaAgents to get AI portfolio weights
- Backtests those weights on historical data
- Shows performance metrics (Sharpe, alpha, returns)
- Compares against S&P 500
- Saves results to `backtest_results_YYYYMMDD_HHMMSS.json`

**Customize:**
```python
# Edit backtest.py
stock_universe = ["AAPL", "MSFT", ...]
risk_tolerance = "moderate"
investment_horizon = "long_term"
portfolio_size = 10
initial_capital = 100000  # Starting amount
backtest_years = 2        # How far back to test
benchmark = "SPY"         # S&P 500
```

---

## Quick Examples

### Example 1: Generate Tech-Heavy Portfolio
```python
# Edit main.py
stock_universe = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "META",  # Tech heavy
    "JPM", "V"  # Some diversification
]
risk_tolerance = "high"
portfolio_size = 5
```

Then run:
```bash
python main.py
```

### Example 2: Conservative Backtest
```python
# Edit backtest.py
stock_universe = [
    "JNJ", "PG", "KO", "WMT",  # Defensive stocks
    "V", "MA", "JPM"  # Stable financials
]
risk_tolerance = "low"
investment_horizon = "long_term"
backtest_years = 5  # Test over 5 years
```

Then run:
```bash
python backtest.py
```

---

## Understanding the Output

### Portfolio Generation Output
```
FINAL PORTFOLIO RECOMMENDATION
==============================================================
Ticker   Weight    Rationale
------   ------    ---------
AAPL     15.0%     Strong fundamentals, innovation leader
MSFT     18.0%     Cloud growth, stable earnings
...
```

### Backtest Output
```
Portfolio Performance:
Initial Capital:        $100,000.00
Final Value:            $156,234.50
Total Return:           56.23%
Sharpe Ratio:           1.35        ← Risk-adjusted return
Alpha:                  +8.45%      ← Beat S&P 500!
```

---

## Key Metrics

- **Sharpe Ratio > 1.0**: Good risk-adjusted returns
- **Alpha > 0**: Portfolio beat the benchmark
- **Max Drawdown**: Largest decline (can you handle it?)
- **Win Rate**: Percentage of profitable days

---

## Troubleshooting

**Error: No API key**
- Create `.env` file with `GOOGLE_API_KEY=your_key`

**Error: No data for ticker**
- Check ticker symbols are correct
- Some tickers may not have historical data

**Error: Portfolio extraction failed**
- The AI returned text instead of structured data
- Check your API key and internet connection
- Try running again

---

## Files Generated

- `portfolio_*.json` - AI portfolio recommendation
- `backtest_results_*.json` - Backtest results with metrics

---

## That's It!

Two simple commands:
- `python main.py` - Generate AI portfolio
- `python backtest.py` - Generate + backtest AI portfolio

Everything else is in the code for you to customize!
