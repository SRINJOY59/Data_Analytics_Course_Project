"""
LangGraph workflow for orchestrating AlphaAgents
"""
from typing import Dict, List, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from agents.specialized_agents import (
    ResearchAgent,
    AnalysisAgent,
    RiskAgent,
    PortfolioAgent,
)


class PortfolioState(TypedDict):
    """State for the portfolio construction workflow"""
    # Input
    stock_universe: List[str]  # List of stock tickers to consider
    risk_tolerance: str  # low, moderate, high
    investment_horizon: str  # short_term, medium_term, long_term
    portfolio_size: int  # Number of stocks in final portfolio
    
    # Agent outputs
    research_results: Dict[str, Any]
    analysis_results: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    portfolio_recommendation: Dict[str, Any]
    
    # Workflow metadata
    current_step: str
    messages: Annotated[List, "append"]


class AlphaAgentsWorkflow:
    """LangGraph workflow orchestrating the AlphaAgents system"""
    
    def __init__(self):
        """Initialize the workflow with all agents"""
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.risk_agent = RiskAgent()
        self.portfolio_agent = PortfolioAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the state graph
        workflow = StateGraph(PortfolioState)
        
        # Add nodes for each agent
        workflow.add_node("research", self._research_node)
        workflow.add_node("analysis", self._analysis_node)
        workflow.add_node("risk_eval", self._risk_assessment_node)
        workflow.add_node("portfolio_construction", self._portfolio_construction_node)
        
        # Define the workflow edges
        workflow.set_entry_point("research")
        workflow.add_edge("research", "analysis")
        workflow.add_edge("analysis", "risk_eval")
        workflow.add_edge("risk_eval", "portfolio_construction")
        workflow.add_edge("portfolio_construction", END)
        
        return workflow.compile()
    
    def _research_node(self, state: PortfolioState) -> PortfolioState:
        """Research node - gather stock information"""
        print(f"\n{'='*60}")
        print(f"STEP 1: MARKET RESEARCH")
        print(f"{'='*60}")
        
        tickers = state["stock_universe"]
        
        task = f"""
        Research the following stocks: {', '.join(tickers)}
        
        For each stock, provide:
        1. Current price and recent performance
        2. Market capitalization and sector
        3. Key financial metrics (P/E ratio, volume)
        4. Recent news and developments
        5. Sector performance context
        
        Provide comprehensive research findings for all stocks.
        """
        
        response = self.research_agent.run(task, context={
            "investment_horizon": state["investment_horizon"],
            "risk_tolerance": state["risk_tolerance"],
        })
        
        # Store both the structured data and a summary
        from pydantic import BaseModel
        state["research_results"] = {
            "data": response if isinstance(response, BaseModel) else None,
            "summary": str(response) if isinstance(response, BaseModel) else response,
            "tickers_researched": tickers,
        }
        state["current_step"] = "research"
        state["messages"].append(f"Research Agent: Completed research on {len(tickers)} stocks")
        
        print(f"\n{state['research_results']['summary']}")

        
        return state
    
    def _analysis_node(self, state: PortfolioState) -> PortfolioState:
        """Analysis node - perform deep financial analysis"""
        print(f"\n{'='*60}")
        print(f"STEP 2: FINANCIAL ANALYSIS")
        print(f"{'='*60}")
        
        tickers = state["stock_universe"]
        research_summary = state["research_results"]["summary"]
        
        task = f"""
        Based on the research findings, perform detailed financial analysis on: {', '.join(tickers)}
        
        Research Summary:
        {research_summary}
        
        For each stock, evaluate:
        1. Fundamental strength (financial metrics, profitability)
        2. Valuation (is it fairly priced, undervalued, or overvalued?)
        3. Growth potential (revenue growth, market opportunity)
        4. Competitive position in sector
        5. Investment recommendation (Strong Buy / Buy / Hold / Sell)
        
        Rank the stocks by investment attractiveness and provide comprehensive analysis.
        """
        
        response = self.analysis_agent.run(task, context={
            "research_data": research_summary,
            "risk_tolerance": state["risk_tolerance"],
        })
        
        from pydantic import BaseModel
        state["analysis_results"] = {
            "data": response if isinstance(response, BaseModel) else None,
            "summary": str(response) if isinstance(response, BaseModel) else response,
            "tickers_analyzed": tickers,
        }
        state["current_step"] = "analysis"
        state["messages"].append(f"Analysis Agent: Completed analysis with recommendations")
        
        print(f"\n{state['analysis_results']['summary']}")

        
        return state
    
    def _risk_assessment_node(self, state: PortfolioState) -> PortfolioState:
        """Risk assessment node - evaluate risks"""
        print(f"\n{'='*60}")
        print(f"STEP 3: RISK ASSESSMENT")
        print(f"{'='*60}")
        
        tickers = state["stock_universe"]
        analysis_summary = state["analysis_results"]["summary"]
        
        task = f"""
        Perform comprehensive risk assessment for: {', '.join(tickers)}
        
        Analysis Summary:
        {analysis_summary}
        
        Investment Profile:
        - Risk Tolerance: {state["risk_tolerance"]}
        - Investment Horizon: {state["investment_horizon"]}
        
        For each stock, assess:
        1. Volatility and beta (market risk)
        2. Financial stability (debt, liquidity)
        3. Business risks (competition, industry headwinds)
        4. Risk rating: Low / Medium / High
        5. Risk-adjusted return potential (Sharpe ratio)
        
        Also evaluate portfolio-level risks:
        - Sector concentration
        - Correlation between stocks
        - Overall portfolio risk profile
        
        Provide comprehensive risk assessment and mitigation recommendations.
        """
        
        response = self.risk_agent.run(task, context={
            "analysis_data": analysis_summary,
            "risk_tolerance": state["risk_tolerance"],
        })
        
        from pydantic import BaseModel
        state["risk_assessment"] = {
            "data": response if isinstance(response, BaseModel) else None,
            "summary": str(response) if isinstance(response, BaseModel) else response,
            "tickers_assessed": tickers,
        }
        state["current_step"] = "risk_assessment"
        state["messages"].append(f"Risk Agent: Completed risk assessment")
        
        print(f"\n{state['risk_assessment']['summary']}")

        
        return state
    
    def _portfolio_construction_node(self, state: PortfolioState) -> PortfolioState:
        """Portfolio construction node - build final portfolio"""
        print(f"\n{'='*60}")
        print(f"STEP 4: PORTFOLIO CONSTRUCTION")
        print(f"{'='*60}")
        
        research_summary = state["research_results"]["summary"]
        analysis_summary = state["analysis_results"]["summary"]
        risk_summary = state["risk_assessment"]["summary"]
        
        task = f"""
        Construct an optimal equity portfolio based on all previous analysis.
        
        INPUTS:
        
        Research Findings:
        {research_summary}
        
        Financial Analysis:
        {analysis_summary}
        
        Risk Assessment:
        {risk_summary}
        
        Portfolio Requirements:
        - Number of stocks: {state["portfolio_size"]}
        - Risk tolerance: {state["risk_tolerance"]}
        - Investment horizon: {state["investment_horizon"]}
        
        YOUR TASK:
        Create a final portfolio recommendation including:
        
        1. PORTFOLIO COMPOSITION
           - Stock ticker and name
           - Allocation percentage
           - Rationale for inclusion
        
        2. PORTFOLIO CHARACTERISTICS
           - Expected risk level
           - Expected return profile
           - Sector diversification breakdown
        
        3. KEY RECOMMENDATIONS
           - Rebalancing strategy
           - Monitoring points
           - Exit criteria
        
        4. RISKS AND CONSIDERATIONS
           - Main portfolio risks
           - Assumptions made
           - Market conditions to watch
        
        Ensure allocations sum to 100% and the portfolio aligns with the investor's risk tolerance.
        """
        
        response = self.portfolio_agent.run(task)
        
        from pydantic import BaseModel
        state["portfolio_recommendation"] = {
            "data": response if isinstance(response, BaseModel) else None,
            "summary": str(response) if isinstance(response, BaseModel) else response,
            "portfolio_size": state["portfolio_size"],
        }
        state["current_step"] = "portfolio_construction"
        state["messages"].append(f"Portfolio Agent: Final portfolio constructed")
        
        print(f"\n{state['portfolio_recommendation']['summary']}")

        
        return state
    
    def run(
        self,
        stock_universe: List[str],
        risk_tolerance: str = "moderate",
        investment_horizon: str = "long_term",
        portfolio_size: int = 10,
    ) -> Dict[str, Any]:
        """
        Run the complete AlphaAgents workflow
        
        Args:
            stock_universe: List of stock tickers to consider
            risk_tolerance: Risk tolerance level (low, moderate, high)
            investment_horizon: Investment time horizon
            portfolio_size: Target number of stocks in portfolio
        
        Returns:
            Complete portfolio recommendation
        """
        # Initialize state
        initial_state: PortfolioState = {
            "stock_universe": stock_universe,
            "risk_tolerance": risk_tolerance,
            "investment_horizon": investment_horizon,
            "portfolio_size": min(portfolio_size, len(stock_universe)),
            "research_results": {},
            "analysis_results": {},
            "risk_assessment": {},
            "portfolio_recommendation": {},
            "current_step": "",
            "messages": [],
        }
        
        # Run the workflow
        print(f"\n{'#'*60}")
        print(f"ALPHAAGENTS PORTFOLIO CONSTRUCTION WORKFLOW")
        print(f"{'#'*60}")
        print(f"\nStock Universe: {', '.join(stock_universe)}")
        print(f"Risk Tolerance: {risk_tolerance}")
        print(f"Investment Horizon: {investment_horizon}")
        print(f"Target Portfolio Size: {portfolio_size}")
        
        final_state = self.workflow.invoke(initial_state)
        
        print(f"\n{'#'*60}")
        print(f"WORKFLOW COMPLETE")
        print(f"{'#'*60}\n")
        
        return {
            "portfolio": final_state["portfolio_recommendation"],
            "research": final_state["research_results"],
            "analysis": final_state["analysis_results"],
            "risk": final_state["risk_assessment"],
            "workflow_log": final_state["messages"],
        }
