"""
Configuration settings for AlphaAgents
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")

# Model Configuration
GEMINI_MODEL = "gemini-2.0-flash"
TEMPERATURE = 0.7
MAX_TOKENS = 4096

# Agent Configuration
AGENT_SETTINGS = {
    "research_agent": {
        "name": "Research Agent",
        "role": "Market Research Specialist",
        "temperature": 0.5,
    },
    "analysis_agent": {
        "name": "Analysis Agent",
        "role": "Financial Analyst",
        "temperature": 0.3,
    },
    "risk_agent": {
        "name": "Risk Agent",
        "role": "Risk Management Specialist",
        "temperature": 0.2,
    },
    "portfolio_agent": {
        "name": "Portfolio Agent",
        "role": "Portfolio Manager",
        "temperature": 0.4,
    }
}

# Portfolio Configuration
DEFAULT_PORTFOLIO_SIZE = 10
DEFAULT_RISK_TOLERANCE = "moderate"  # low, moderate, high
DEFAULT_INVESTMENT_HORIZON = "long_term"  # short_term, medium_term, long_term
