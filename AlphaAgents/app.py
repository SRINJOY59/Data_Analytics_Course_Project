"""
AlphaAgents Portfolio Optimization - Streamlit UI
A comprehensive web interface for AI-powered portfolio construction and backtesting
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import traceback

# Import AlphaAgents modules
from workflow.portfolio_workflow import AlphaAgentsWorkflow
from backtesting import PortfolioBacktester
from schemas import PortfolioOutput
from utils.portfolio_formatter import format_portfolio_output


# Page configuration
st.set_page_config(
    page_title="AlphaAgents - AI Portfolio Optimizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)


# Default stock universe
DEFAULT_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "META", "ADBE",  # Tech
    "JPM", "BAC", "V", "MA", "GS",  # Finance
    "JNJ", "UNH", "PFE", "ABBV", "TMO",  # Healthcare
    "AMZN", "TSLA", "HD", "NKE", "WMT", "PG",  # Consumer
    "XOM", "CVX", "COP",  # Energy
    "DIS", "NFLX", "CMCSA",  # Communication
]


def initialize_session_state():
    """Initialize session state variables"""
    if 'portfolio_generated' not in st.session_state:
        st.session_state.portfolio_generated = False
    if 'ai_results' not in st.session_state:
        st.session_state.ai_results = None
    if 'backtest_results' not in st.session_state:
        st.session_state.backtest_results = None
    if 'portfolio_weights' not in st.session_state:
        st.session_state.portfolio_weights = None


def create_portfolio_pie_chart(weights: Dict[str, float]) -> go.Figure:
    """Create pie chart for portfolio allocation"""
    fig = go.Figure(data=[go.Pie(
        labels=list(weights.keys()),
        values=[v*100 for v in weights.values()],
        hole=0.4,
        marker_colors=px.colors.qualitative.Set3,
        textinfo='label+percent',
        textposition='auto',
    )])
    
    fig.update_layout(
        title="Portfolio Allocation",
        height=500,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1)
    )
    
    return fig


def create_sector_allocation_chart(portfolio_data) -> go.Figure:
    """Create bar chart for sector allocation"""
    if not portfolio_data or not hasattr(portfolio_data, 'characteristics'):
        return None
    
    sectors = portfolio_data.characteristics.sector_breakdown
    
    fig = go.Figure(data=[go.Bar(
        x=[s.sector for s in sectors],
        y=[s.percentage for s in sectors],
        marker_color=px.colors.qualitative.Pastel,
        text=[f"{s.percentage:.1f}%" for s in sectors],
        textposition='auto',
    )])
    
    fig.update_layout(
        title="Sector Allocation",
        xaxis_title="Sector",
        yaxis_title="Allocation (%)",
        height=400,
        showlegend=False
    )
    
    return fig


def create_portfolio_value_chart(portfolio_value: pd.Series, initial_capital: float) -> go.Figure:
    """Create portfolio value over time chart"""
    fig = go.Figure()
    
    # Portfolio value
    fig.add_trace(go.Scatter(
        x=portfolio_value.index,
        y=portfolio_value.values,
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#2E86C1', width=2),
        fill='tonexty',
        fillcolor='rgba(46, 134, 193, 0.1)'
    ))
    
    # Initial capital line
    fig.add_trace(go.Scatter(
        x=[portfolio_value.index[0], portfolio_value.index[-1]],
        y=[initial_capital, initial_capital],
        mode='lines',
        name='Initial Capital',
        line=dict(color='#E74C3C', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Portfolio Value Over Time",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_returns_distribution_chart(returns: pd.Series) -> go.Figure:
    """Create returns distribution histogram"""
    fig = go.Figure(data=[go.Histogram(
        x=returns * 100,
        nbinsx=50,
        marker_color='#3498DB',
        name='Daily Returns'
    )])
    
    fig.update_layout(
        title="Daily Returns Distribution",
        xaxis_title="Return (%)",
        yaxis_title="Frequency",
        height=400,
        showlegend=False
    )
    
    return fig


def create_drawdown_chart(portfolio_value: pd.Series) -> go.Figure:
    """Create drawdown chart"""
    cumulative = portfolio_value
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=drawdown.index,
        y=drawdown.values,
        mode='lines',
        fill='tozeroy',
        line=dict(color='#E74C3C', width=1),
        fillcolor='rgba(231, 76, 60, 0.3)',
        name='Drawdown'
    ))
    
    fig.update_layout(
        title="Portfolio Drawdown Over Time",
        xaxis_title="Date",
        yaxis_title="Drawdown (%)",
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_correlation_heatmap(correlation_matrix: pd.DataFrame) -> go.Figure:
    """Create correlation heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdBu',
        zmid=0,
        text=np.round(correlation_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="Stock Correlation Matrix",
        height=600,
        xaxis={'side': 'bottom'},
    )
    
    return fig


def create_individual_performance_chart(individual_metrics: Dict[str, Dict]) -> go.Figure:
    """Create bar chart comparing individual stock performance"""
    tickers = list(individual_metrics.keys())
    returns = [individual_metrics[t]['total_return'] for t in tickers]
    sharpe = [individual_metrics[t]['sharpe_ratio'] for t in tickers]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Total Return (%)", "Sharpe Ratio")
    )
    
    fig.add_trace(
        go.Bar(x=tickers, y=returns, name='Return', marker_color='#2ECC71'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=tickers, y=sharpe, name='Sharpe', marker_color='#3498DB'),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_text="Individual Stock Performance"
    )
    
    return fig


def extract_weights_from_portfolio(portfolio_data) -> Dict[str, float]:
    """Extract portfolio weights from AI-generated portfolio data"""
    if not portfolio_data or isinstance(portfolio_data, str):
        return None
    
    holdings = None
    if hasattr(portfolio_data, 'holdings'):
        holdings = portfolio_data.holdings
    elif hasattr(portfolio_data, 'allocations'):
        holdings = portfolio_data.allocations
    
    if not holdings:
        return None
    
    weights = {}
    for holding in holdings:
        ticker = holding.ticker
        
        if hasattr(holding, 'allocation'):
            weight = holding.allocation / 100.0
        elif hasattr(holding, 'weight_percent'):
            weight = holding.weight_percent / 100.0
        elif hasattr(holding, 'weight'):
            weight = holding.weight / 100.0 if holding.weight > 1 else holding.weight
        else:
            weight = 1.0 / len(holdings)
        
        weights[ticker] = weight
    
    return weights


def display_portfolio_details(portfolio_data):
    """Display detailed portfolio information"""
    if not portfolio_data or isinstance(portfolio_data, str):
        st.warning("Portfolio data not available in structured format")
        return
    
    # Portfolio Overview
    st.subheader("📊 Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Number of Holdings",
            portfolio_data.characteristics.number_of_holdings
        )
    
    with col2:
        st.metric(
            "Risk Level",
            portfolio_data.characteristics.risk_level.upper()
        )
    
    with col3:
        st.metric(
            "Expected Return",
            portfolio_data.characteristics.expected_return
        )
    
    with col4:
        st.metric(
            "Largest Sector",
            portfolio_data.characteristics.largest_sector
        )
    
    # Holdings Table
    st.subheader("💼 Portfolio Holdings")
    
    holdings_data = []
    for holding in portfolio_data.holdings:
        holdings_data.append({
            "Ticker": holding.ticker,
            "Company": holding.company_name,
            "Sector": holding.sector,
            "Allocation (%)": f"{holding.allocation:.1f}",
            "Rationale": holding.rationale[:100] + "..." if len(holding.rationale) > 100 else holding.rationale
        })
    
    df_holdings = pd.DataFrame(holdings_data)
    st.dataframe(df_holdings, use_container_width=True, hide_index=True)
    
    # Sector Allocation
    col1, col2 = st.columns(2)
    
    with col1:
        sector_fig = create_sector_allocation_chart(portfolio_data)
        if sector_fig:
            st.plotly_chart(sector_fig, use_container_width=True)
    
    with col2:
        weights = extract_weights_from_portfolio(portfolio_data)
        if weights:
            pie_fig = create_portfolio_pie_chart(weights)
            st.plotly_chart(pie_fig, use_container_width=True)
    
    # Detailed Holdings Information
    with st.expander("📝 Detailed Holdings Information"):
        for holding in portfolio_data.holdings:
            st.markdown(f"**{holding.ticker} - {holding.company_name}**")
            st.markdown(f"*Allocation: {holding.allocation}%*")
            st.markdown(f"**Rationale:** {holding.rationale}")
            st.markdown(f"**Entry Criteria:** {holding.entry_criteria}")
            st.markdown(f"**Exit Criteria:** {holding.exit_criteria}")
            st.markdown("---")
    
    # Investment Strategy
    with st.expander("🎯 Investment Strategy"):
        st.write(portfolio_data.investment_strategy)
    
    # Risk Analysis
    with st.expander("⚠️ Key Risks"):
        for risk in portfolio_data.key_risks:
            st.markdown(f"- {risk}")
    
    # Rebalancing Guidelines
    with st.expander("🔄 Rebalancing Guidelines"):
        st.markdown(f"**Frequency:** {portfolio_data.rebalancing.frequency}")
        st.markdown(f"**Threshold:** {portfolio_data.rebalancing.threshold}")
        st.markdown("**Triggers:**")
        for trigger in portfolio_data.rebalancing.triggers:
            st.markdown(f"- {trigger}")


def display_backtest_results(backtest_results: Dict[str, Any], initial_capital: float):
    """Display comprehensive backtest results"""
    if not backtest_results:
        st.error("No backtest results available")
        return
    
    metrics = backtest_results['portfolio_metrics']
    
    # Key Metrics
    st.subheader("📊 Performance Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        profit = backtest_results['final_value'] - initial_capital
        st.metric(
            "Total Return",
            f"{metrics['total_return']:.2f}%",
            f"${profit:,.0f}"
        )
    
    with col2:
        st.metric(
            "Annualized Return",
            f"{metrics['annualized_return']:.2f}%"
        )
    
    with col3:
        st.metric(
            "Sharpe Ratio",
            f"{metrics['sharpe_ratio']:.2f}"
        )
    
    with col4:
        st.metric(
            "Max Drawdown",
            f"{metrics['max_drawdown']:.2f}%"
        )
    
    with col5:
        st.metric(
            "Win Rate",
            f"{metrics['win_rate']:.1f}%"
        )
    
    # Additional metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Volatility", f"{metrics['volatility']:.2f}%")
    
    with col2:
        st.metric("Sortino Ratio", f"{metrics['sortino_ratio']:.2f}")
    
    with col3:
        st.metric("Best Day", f"{metrics['best_day']:.2f}%")
    
    with col4:
        st.metric("Worst Day", f"{metrics['worst_day']:.2f}%")
    
    # Benchmark comparison if available
    if 'alpha' in metrics:
        st.subheader("📈 Benchmark Comparison")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Alpha", f"{metrics['alpha']:.2f}%")
        
        with col2:
            st.metric("Correlation", f"{metrics['correlation_to_benchmark']:.2f}")
        
        with col3:
            st.metric("Information Ratio", f"{metrics['information_ratio']:.2f}")
    
    # Performance Rating
    sharpe = metrics['sharpe_ratio']
    if sharpe > 2.0:
        rating = "🌟 EXCELLENT"
        color = "green"
    elif sharpe > 1.0:
        rating = "✅ GOOD"
        color = "blue"
    elif sharpe > 0.5:
        rating = "⚠️ FAIR"
        color = "orange"
    else:
        rating = "❌ POOR"
        color = "red"
    
    st.markdown(f"**Performance Rating:** :{color}[{rating}]")
    
    # Charts
    st.subheader("📉 Performance Charts")
    
    # Portfolio value chart
    portfolio_value_fig = create_portfolio_value_chart(
        backtest_results['portfolio_value'],
        initial_capital
    )
    st.plotly_chart(portfolio_value_fig, use_container_width=True)
    
    # Additional charts in columns
    col1, col2 = st.columns(2)
    
    with col1:
        returns_fig = create_returns_distribution_chart(backtest_results['portfolio_returns'])
        st.plotly_chart(returns_fig, use_container_width=True)
    
    with col2:
        drawdown_fig = create_drawdown_chart(backtest_results['portfolio_value'])
        st.plotly_chart(drawdown_fig, use_container_width=True)
    
    # Individual stock performance
    if 'individual_metrics' in backtest_results:
        st.subheader("📊 Individual Stock Performance")
        
        individual_fig = create_individual_performance_chart(backtest_results['individual_metrics'])
        st.plotly_chart(individual_fig, use_container_width=True)
        
        # Detailed table
        with st.expander("📋 Detailed Stock Metrics"):
            stock_data = []
            for ticker, stock_metrics in backtest_results['individual_metrics'].items():
                stock_data.append({
                    "Ticker": ticker,
                    "Return (%)": f"{stock_metrics['total_return']:.2f}",
                    "Volatility (%)": f"{stock_metrics['volatility']:.2f}",
                    "Sharpe": f"{stock_metrics['sharpe_ratio']:.2f}",
                    "Sortino": f"{stock_metrics['sortino_ratio']:.2f}",
                    "Max Drawdown (%)": f"{stock_metrics['max_drawdown']:.2f}",
                    "Win Rate (%)": f"{stock_metrics['win_rate']:.1f}"
                })
            
            df_stocks = pd.DataFrame(stock_data)
            st.dataframe(df_stocks, use_container_width=True, hide_index=True)
    
    # Correlation matrix
    if 'correlation_matrix' in backtest_results:
        with st.expander("🔗 Stock Correlation Matrix"):
            corr_fig = create_correlation_heatmap(backtest_results['correlation_matrix'])
            st.plotly_chart(corr_fig, use_container_width=True)


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.title("🤖 AlphaAgents Portfolio Optimizer")
    st.markdown("*AI-Powered Portfolio Construction and Backtesting System*")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Stock Universe
        st.subheader("📈 Stock Universe")
        
        use_default = st.checkbox("Use default stock universe", value=True)
        
        if use_default:
            stock_universe = DEFAULT_STOCKS
            st.info(f"Using {len(stock_universe)} default stocks")
        else:
            stock_input = st.text_area(
                "Enter stock tickers (comma-separated)",
                value=", ".join(DEFAULT_STOCKS[:10]),
                height=100
            )
            stock_universe = [s.strip().upper() for s in stock_input.split(",") if s.strip()]
        
        st.write(f"**Selected Stocks:** {len(stock_universe)}")
        
        # Portfolio Parameters
        st.subheader("💼 Portfolio Parameters")
        
        portfolio_size = st.slider(
            "Portfolio Size",
            min_value=3,
            max_value=min(20, len(stock_universe)),
            value=min(10, len(stock_universe)),
            help="Number of stocks to include in final portfolio"
        )
        
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            options=["low", "moderate", "high"],
            index=1
        )
        
        investment_horizon = st.selectbox(
            "Investment Horizon",
            options=["short_term", "medium_term", "long_term"],
            index=2
        )
        
        # Backtesting Parameters
        st.subheader("📊 Backtesting")
        
        initial_capital = st.number_input(
            "Initial Capital ($)",
            min_value=10000,
            max_value=10000000,
            value=100000,
            step=10000
        )
        
        backtest_years = st.slider(
            "Backtest Period (years)",
            min_value=1,
            max_value=5,
            value=2
        )
        
        benchmark = st.text_input(
            "Benchmark Ticker",
            value="SPY",
            help="Ticker to use as benchmark (e.g., SPY for S&P 500)"
        )
        
        st.markdown("---")
        
        # Action buttons
        generate_btn = st.button(
            "🚀 Generate AI Portfolio",
            type="primary",
            use_container_width=True
        )
        
        if st.session_state.portfolio_generated:
            backtest_btn = st.button(
                "📊 Run Backtest",
                type="secondary",
                use_container_width=True
            )
        else:
            backtest_btn = False
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📋 Portfolio", "📊 Backtest Results", "ℹ️ About"])
    
    # Generate Portfolio
    if generate_btn:
        with st.spinner("🤖 Generating AI portfolio... This may take a few minutes..."):
            try:
                workflow = AlphaAgentsWorkflow()
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Running market research...")
                progress_bar.progress(25)
                
                ai_results = workflow.run(
                    stock_universe=stock_universe,
                    risk_tolerance=risk_tolerance,
                    investment_horizon=investment_horizon,
                    portfolio_size=portfolio_size,
                )
                
                progress_bar.progress(100)
                status_text.text("Portfolio generation complete!")
                
                # Store results
                st.session_state.ai_results = ai_results
                st.session_state.portfolio_generated = True
                
                portfolio_data = ai_results["portfolio"]["data"]
                st.session_state.portfolio_weights = extract_weights_from_portfolio(portfolio_data)
                
                st.success("✅ AI Portfolio generated successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error generating portfolio: {str(e)}")
                st.code(traceback.format_exc())
    
    # Run Backtest
    if backtest_btn and st.session_state.portfolio_generated:
        with st.spinner("📊 Running backtest... Fetching historical data..."):
            try:
                if not st.session_state.portfolio_weights:
                    st.error("Could not extract portfolio weights. Please regenerate portfolio.")
                else:
                    # Calculate dates
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=backtest_years*365)
                    
                    # Run backtest
                    backtester = PortfolioBacktester(initial_capital=initial_capital)
                    
                    backtest_results = backtester.backtest_weighted_portfolio(
                        portfolio_weights=st.session_state.portfolio_weights,
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d"),
                        benchmark=benchmark
                    )
                    
                    if backtest_results:
                        st.session_state.backtest_results = backtest_results
                        st.success("✅ Backtest completed successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Backtesting failed. Check if tickers have sufficient historical data.")
                
            except Exception as e:
                st.error(f"❌ Error running backtest: {str(e)}")
                st.code(traceback.format_exc())
    
    # Tab 1: Portfolio Display
    with tab1:
        if st.session_state.portfolio_generated and st.session_state.ai_results:
            portfolio_data = st.session_state.ai_results["portfolio"]["data"]
            
            if portfolio_data and not isinstance(portfolio_data, str):
                st.success("✅ AI Portfolio Ready")
                
                # Executive Summary
                if hasattr(portfolio_data, 'executive_summary'):
                    st.info(portfolio_data.executive_summary)
                
                display_portfolio_details(portfolio_data)
                
                # Download option
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download as JSON
                    portfolio_json = {
                        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'parameters': {
                            'risk_tolerance': risk_tolerance,
                            'investment_horizon': investment_horizon,
                            'portfolio_size': portfolio_size
                        },
                        'portfolio': portfolio_data.model_dump() if hasattr(portfolio_data, 'model_dump') else str(portfolio_data)
                    }
                    
                    st.download_button(
                        label="📥 Download Portfolio (JSON)",
                        data=json.dumps(portfolio_json, indent=2),
                        file_name=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Download as formatted text
                    formatted_text = format_portfolio_output(portfolio_data)
                    st.download_button(
                        label="📄 Download Portfolio (TXT)",
                        data=formatted_text,
                        file_name=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
            else:
                st.warning("Portfolio data returned as text format")
                st.text(st.session_state.ai_results["portfolio"]["summary"])
        else:
            st.info("👈 Configure parameters in the sidebar and click 'Generate AI Portfolio' to start")
            
            # Show sample
            st.markdown("### 🎯 How It Works")
            st.markdown("""
            1. **Configure Parameters**: Set your stock universe, risk tolerance, and investment horizon
            2. **Generate Portfolio**: AI agents analyze stocks and construct an optimized portfolio
            3. **Review Portfolio**: Examine holdings, allocations, and strategy
            4. **Run Backtest**: Test portfolio performance on historical data
            5. **Analyze Results**: Review metrics, charts, and performance
            """)
    
    # Tab 2: Backtest Results
    with tab2:
        if st.session_state.backtest_results:
            st.success("✅ Backtest Results Available")
            
            display_backtest_results(
                st.session_state.backtest_results,
                initial_capital
            )
            
            # Download results
            st.markdown("---")
            
            results_to_save = {
                'backtest_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'parameters': {
                    'initial_capital': initial_capital,
                    'backtest_years': backtest_years,
                    'benchmark': benchmark
                },
                'portfolio_weights': st.session_state.backtest_results.get('portfolio_weights', {}),
                'metrics': st.session_state.backtest_results['portfolio_metrics'],
                'final_value': st.session_state.backtest_results['final_value'],
            }
            
            st.download_button(
                label="📥 Download Backtest Results (JSON)",
                data=json.dumps(results_to_save, indent=2),
                file_name=f"backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
        else:
            st.info("👈 Generate a portfolio and click 'Run Backtest' to see results here")
            
            st.markdown("### 📊 What You'll See")
            st.markdown("""
            - **Performance Metrics**: Returns, Sharpe ratio, drawdown, win rate
            - **Benchmark Comparison**: Alpha, correlation, information ratio
            - **Visual Analysis**: Portfolio value, returns distribution, drawdowns
            - **Individual Performance**: Each stock's contribution and metrics
            - **Risk Analysis**: Correlation matrix and diversification insights
            """)
    
    # Tab 3: About
    with tab3:
        st.markdown("## 🤖 About AlphaAgents")
        
        st.markdown("""
        AlphaAgents is an AI-powered portfolio optimization system that leverages multiple specialized 
        AI agents to construct and analyze investment portfolios.
        
        ### 🎯 Key Features
        
        - **Multi-Agent System**: Research, Analysis, Risk, and Portfolio agents work together
        - **Real-Time Data**: Fetches live market data for analysis
        - **Comprehensive Analysis**: Fundamental, technical, and sentiment analysis
        - **Risk Management**: Advanced risk assessment and diversification
        - **Backtesting**: Historical performance testing with detailed metrics
        - **Interactive UI**: Easy-to-use interface with rich visualizations
        
        ### 🔍 How It Works
        
        1. **Research Agent**: Gathers market data, news, and company information
        2. **Analysis Agent**: Performs fundamental and technical analysis
        3. **Risk Agent**: Assesses risks and ensures proper diversification
        4. **Portfolio Agent**: Constructs optimized portfolio with allocations
        5. **Backtester**: Tests portfolio on historical data
        
        ### 📊 Metrics Explained
        
        - **Sharpe Ratio**: Risk-adjusted return (higher is better, >1 is good)
        - **Sortino Ratio**: Like Sharpe but focuses on downside risk
        - **Max Drawdown**: Largest peak-to-trough decline
        - **Alpha**: Excess return vs. benchmark
        - **Information Ratio**: Risk-adjusted excess return vs. benchmark
        
        ### ⚠️ Disclaimer
        
        This tool is for educational and research purposes only. It does not constitute 
        financial advice. Always conduct your own research and consult with financial 
        professionals before making investment decisions.
        """)
        
        st.markdown("---")
        st.markdown("*Built with Streamlit, LangGraph, and Google Gemini*")


if __name__ == "__main__":
    main()
