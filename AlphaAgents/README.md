# AlphaAgents - AI-Powered Portfolio Construction System# AlphaAgents: Multi-Agent Portfolio Construction System



An intelligent multi-agent system for portfolio construction using Google's Gemini AI. AlphaAgents analyzes stocks, assesses risks, and builds optimized portfolios tailored to your investment goals.An advanced equity portfolio construction system powered by AI agents using **Agno** framework and **LangGraph** orchestration with **Google Gemini** as the underlying LLM.



## 🌟 Features## Overview



- **Multi-Agent AI System**: Research, Analysis, Risk Assessment, and Portfolio Construction agentsAlphaAgents implements a multi-agent system for equity portfolio construction, inspired by research in AI-driven investment management. The system uses specialized agents that collaborate to research, analyze, assess risks, and construct optimal portfolios.

- **Structured Outputs**: Pydantic-validated responses for reliable data

- **Comprehensive Analysis**: Fundamental analysis, valuation, risk metrics, and sector allocation## Architecture

- **Backtesting**: Test AI-generated portfolios on historical data

- **Customizable**: Configure risk tolerance, time horizon, and stock universe### Agent Framework

- **LangGraph Orchestration**: Sequential agent workflow with state management- **Framework**: Agno (for agent implementation)

- **Orchestration**: LangGraph (for workflow management)

## 🚀 Quick Start- **LLM**: Google Gemini 1.5 Pro

- **Data**: Yahoo Finance (via yfinance)

### Installation

### Specialized Agents

1. **Clone the repository**

```bash1. **Research Agent**

cd AlphaAgents   - Discovers and evaluates investment opportunities

```   - Gathers fundamental data and market sentiment

   - Tracks sector performance and trends

2. **Create virtual environment**

```bash2. **Analysis Agent**

python -m venv venv   - Performs deep financial analysis

venv\Scripts\activate  # Windows   - Evaluates valuation metrics and growth potential

# or   - Provides buy/hold/sell recommendations

source venv/bin/activate  # Mac/Linux

```3. **Risk Agent**

   - Assesses individual stock and portfolio risks

3. **Install dependencies**   - Calculates volatility and risk-adjusted returns

```bash   - Ensures proper diversification

pip install -r requirements.txt

```4. **Portfolio Agent**

   - Synthesizes all agent inputs

4. **Set up API key**   - Constructs optimal portfolio allocation

   - Balances risk-return tradeoffs

Create a `.env` file:

```env## Workflow

GOOGLE_API_KEY=your_gemini_api_key_here

``````

┌─────────────────┐

Get your API key from: https://makersuite.google.com/app/apikey│  Stock Universe │

└────────┬────────┘

### Basic Usage         │

         ▼

#### 1. Generate AI Portfolio┌─────────────────┐

│ Research Agent  │ ──► Gather market data, news, fundamentals

```bash└────────┬────────┘

python main.py         │

```         ▼

┌─────────────────┐

This will:│ Analysis Agent  │ ──► Financial analysis, valuation, rankings

- Analyze your stock universe└────────┬────────┘

- Generate optimal portfolio with AI-recommended weights         │

- Save results to JSON file         ▼

┌─────────────────┐

#### 2. Backtest AI Portfolio│  Risk Agent     │ ──► Risk assessment, volatility, diversification

└────────┬────────┘

```bash         │

python backtest.py         ▼

```┌─────────────────┐

│Portfolio Agent  │ ──► Final allocation and recommendations

This will:└────────┬────────┘

- Generate AI portfolio with optimized weights         │

- Backtest the portfolio on historical data         ▼

- Show performance metrics (Sharpe ratio, alpha, returns, etc.)┌─────────────────┐

- Compare against benchmark (S&P 500)│ Final Portfolio │

└─────────────────┘

### Customization```



Edit `main.py` to customize:## Installation



```python### Prerequisites

stock_universe = [- Python 3.9 or higher

    "AAPL", "MSFT", "GOOGL", "NVDA",  # Your stocks- Google API Key (for Gemini)

    "JPM", "V", "JNJ", "WMT"

]### Setup



results = run_alphaagents(1. Clone or download the project:

    stock_universe=stock_universe,```bash

    risk_tolerance="moderate",      # low, moderate, highcd AlphaAgents

    investment_horizon="long_term", # short_term, medium_term, long_term```

    portfolio_size=8,               # Number of stocks

    save_results=True2. Create a virtual environment:

)```bash

```python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

Edit `backtest.py` to customize backtesting:```



```python3. Install dependencies:

results = run_backtest(```bash

    stock_universe=stock_universe,pip install -r requirements.txt

    risk_tolerance="moderate",```

    investment_horizon="long_term",

    portfolio_size=10,4. Configure API keys:

    initial_capital=100000,         # Starting capital```bash

    backtest_years=2,               # Backtest period# Create .env file from example

    benchmark="SPY"                 # Benchmark (S&P 500)cp .env.example .env

)

```# Edit .env and add your Google API key

GOOGLE_API_KEY=your_google_api_key_here

## 📁 Project Structure```



```## Usage

AlphaAgents/

├── main.py                      # Main portfolio generation script### Basic Example

├── backtest.py                  # Backtesting script

├── backtesting.py              # Backtesting engine (core)```python

├── config.py                    # Configuration settingsfrom workflow.portfolio_workflow import AlphaAgentsWorkflow

├── schemas.py                   # Pydantic schemas for structured outputs

├── requirements.txt             # Python dependencies# Define stock universe

├── .env                         # API keys (create this)stocks = ["AAPL", "MSFT", "GOOGL", "JPM", "JNJ"]

│

├── agents/# Initialize workflow

│   ├── base_agent.py           # Base agent classworkflow = AlphaAgentsWorkflow()

│   └── specialized_agents.py   # Research, Analysis, Risk, Portfolio agents

│# Run portfolio construction

├── workflow/results = workflow.run(

│   └── portfolio_workflow.py   # LangGraph workflow orchestration    stock_universe=stocks,

│    risk_tolerance="moderate",

├── tools/    investment_horizon="long_term",

│   └── market_tools.py         # Market data tools (yfinance)    portfolio_size=5

│)

└── utils/

    └── portfolio_formatter.py  # Portfolio output formatting# Access results

```print(results["portfolio"]["summary"])

```

## 🤖 How It Works

### Running the Main Script

### Agent Pipeline

```bash

```python main.py

1. Research Agent```

   ↓

   Gathers stock data, news, financials### Parameters

   

2. Analysis Agent- **stock_universe**: List of stock tickers to consider

   ↓- **risk_tolerance**: `low`, `moderate`, or `high`

   Performs fundamental analysis, valuations- **investment_horizon**: `short_term`, `medium_term`, or `long_term`

   - **portfolio_size**: Number of stocks in final portfolio

3. Risk Agent

   ↓## Project Structure

   Assesses risks, calculates volatility

   ```

4. Portfolio AgentAlphaAgents/

   ↓├── agents/

   Constructs optimized portfolio with weights│   ├── base_agent.py           # Base agent implementation

```│   └── specialized_agents.py   # Research, Analysis, Risk, Portfolio agents

├── tools/

### Key Components│   └── market_tools.py          # Market data and analysis tools

├── workflow/

**Research Agent**│   └── portfolio_workflow.py    # LangGraph workflow orchestration

- Fetches current prices and market data├── config.py                    # Configuration settings

- Analyzes recent news and developments├── main.py                      # Main execution script

- Evaluates sector performance├── requirements.txt             # Project dependencies

- Provides comprehensive stock research├── .env.example                 # Environment variables template

└── README.md                    # This file

**Analysis Agent**```

- Fundamental analysis (P/E, growth, margins)

- Valuation assessment (undervalued/overvalued)## Configuration

- Competitive position analysis

- Investment recommendations with scoresEdit `config.py` to customize:



**Risk Agent**```python

- Calculates volatility and beta# Model settings

- Assesses market, financial, and business risksGEMINI_MODEL = "gemini-1.5-pro"

- Evaluates sector concentrationTEMPERATURE = 0.7

- Provides risk mitigation strategies

# Agent configurations

**Portfolio Agent**AGENT_SETTINGS = {

- Constructs optimized portfolio    "research_agent": {"temperature": 0.5},

- Allocates weights based on analysis and risk    "analysis_agent": {"temperature": 0.3},

- Ensures diversification    # ... etc

- Provides rebalancing guidelines}



## 📊 Backtesting Features# Portfolio defaults

DEFAULT_PORTFOLIO_SIZE = 10

The backtesting module provides:DEFAULT_RISK_TOLERANCE = "moderate"

```

- **Portfolio Performance**: Total return, annualized return

- **Risk Metrics**: Volatility, max drawdown, Sharpe ratio, Sortino ratio## Features

- **Benchmark Comparison**: Alpha, correlation, information ratio

- **Individual Stock Analysis**: Performance breakdown by ticker### Market Data Tools

- **Correlation Matrix**: Stock relationship analysis- Real-time stock prices and metrics

- Financial fundamentals (P/E, ROE, debt ratios)

### Sample Output- Volatility and risk calculations

- News and sentiment analysis

```- Sector performance tracking

Portfolio Performance:

Initial Capital:        $100,000.00### Agent Capabilities

Final Value:            $156,234.50- Multi-source research and data gathering

Total Return:           56.23%- Fundamental and technical analysis

Annualized Return:      24.89%- Risk-adjusted return optimization

Sharpe Ratio:           1.35- Sector diversification

Alpha:                  +8.45% (Beat S&P 500!)- Portfolio rebalancing recommendations

```

### Workflow Orchestration

## 🎯 Use Cases- Sequential agent execution

- State management via LangGraph

1. **Portfolio Generation**: Let AI build an optimized portfolio- Context passing between agents

2. **Strategy Validation**: Backtest AI recommendations on historical data- Comprehensive logging and tracking

3. **Risk Assessment**: Understand portfolio risks before investing

4. **Rebalancing**: Get AI recommendations for portfolio rebalancing## Example Output

5. **Research**: Deep dive into stock fundamentals and analysis

```

## ⚙️ ConfigurationPORTFOLIO COMPOSITION:

1. AAPL (Apple Inc.) - 15%

### Risk Tolerance Levels   Rationale: Strong fundamentals, consistent growth, tech leader

   

- **Low**: Conservative, lower volatility, defensive stocks2. MSFT (Microsoft) - 15%

- **Moderate**: Balanced risk-return, diversified allocation   Rationale: Cloud dominance, diverse revenue streams, low risk

- **High**: Growth-focused, higher volatility, aggressive allocation   

3. JPM (JPMorgan) - 12%

### Investment Horizons   Rationale: Financial sector exposure, solid dividend



- **Short-term**: < 1 year, focus on momentum and technicals...

- **Medium-term**: 1-3 years, balanced approach

- **Long-term**: > 3 years, focus on fundamentals and growthRISK PROFILE: Moderate

EXPECTED RETURN: 8-12% annually

## 📈 Performance Metrics ExplainedSHARPE RATIO: 1.2



| Metric | Description | Good Value |SECTOR BREAKDOWN:

|--------|-------------|------------|- Technology: 40%

| **Sharpe Ratio** | Risk-adjusted return | > 1.0 |- Financials: 20%

| **Alpha** | Excess return vs benchmark | > 0 |- Healthcare: 15%

| **Max Drawdown** | Worst peak-to-trough decline | Smaller is better |...

| **Volatility** | Standard deviation of returns | Lower for stability |```

| **Correlation** | Relationship with benchmark | 0.7-0.9 typical |

## Limitations & Disclaimers

## 🔧 Advanced Usage

⚠️ **Important**: This system is for educational and research purposes only.

### Custom Stock Universe

- Not financial advice - consult with licensed professionals

```python- Historical data doesn't guarantee future performance

# Focus on specific sectors- AI agents can make errors or biased decisions

tech_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "META"]- Market data may be delayed or incomplete

finance_stocks = ["JPM", "BAC", "GS", "MS", "C"]- Always conduct your own due diligence

healthcare_stocks = ["JNJ", "UNH", "PFE", "ABBV", "TMO"]

## Contributing

stock_universe = tech_stocks + finance_stocks + healthcare_stocks

Contributions are welcome! Areas for improvement:

results = run_alphaagents(- Additional data sources and APIs

    stock_universe=stock_universe,- More sophisticated risk models

    portfolio_size=12- Backtesting capabilities

)- Performance tracking

```- Alternative portfolio strategies



### Multiple Backtests## License



```pythonMIT License - See LICENSE file for details

# Test different time periods

for years in [1, 2, 3, 5]:## Acknowledgments

    print(f"\n{'='*70}")

    print(f"Testing {years}-year backtest")- Inspired by research in AI-driven portfolio management

    print(f"{'='*70}")- Built with Agno, LangGraph, and Google Gemini

    - Market data provided by Yahoo Finance

    run_backtest(

        stock_universe=my_stocks,---

        backtest_years=years

    )**Disclaimer**: This software is provided "as is" without warranty. Use at your own risk. Not intended as investment advice.

```

## 📝 Output Files

- **Portfolio Generation**: `portfolio_YYYYMMDD_HHMMSS.json`
- **Backtesting**: `backtest_results_YYYYMMDD_HHMMSS.json`

## 🛠️ Requirements

- Python 3.8+
- Google Gemini API key
- Internet connection for market data

## 📚 Dependencies

- `agno` - Agent framework
- `langgraph` - Workflow orchestration
- `langchain` - LLM integration
- `google-generativeai` - Google Gemini API
- `yfinance` - Market data
- `pandas` - Data analysis
- `pydantic` - Data validation

## ⚠️ Disclaimer

This software is for educational and research purposes only. It is not financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.

Past performance does not guarantee future results. Backtesting results may not reflect actual trading performance.

## 🤝 Contributing

This is a demonstration project showing multi-agent AI systems for portfolio construction. Feel free to extend and customize for your needs.

## 📄 License

See LICENSE file for details.

## 🎓 Learn More

For more information about the components used:
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Google Gemini**: https://ai.google.dev/
- **Agno Framework**: https://github.com/agno-framework

---

**Built with ❤️ using Google Gemini and LangGraph**
