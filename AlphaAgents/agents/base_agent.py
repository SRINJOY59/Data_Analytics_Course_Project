"""
Base agents implementation using Agno framework
"""
from typing import List, Dict, Any, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.google import Gemini
from config import GOOGLE_API_KEY, GEMINI_MODEL, AGENT_SETTINGS
from dotenv import load_dotenv

load_dotenv()

T = TypeVar('T', bound=BaseModel)

class BaseAlphaAgent:
    """Base class for all AlphaAgents"""
    
    def __init__(
        self, 
        name: str, 
        role: str, 
        instructions: str, 
        tools: Optional[List] = None, 
        temperature: float = 0.7,
        response_model: Optional[Type[BaseModel]] = None
    ):
        """
        Initialize an AlphaAgent
        
        Args:
            name: Agent name
            role: Agent role description
            instructions: Detailed instructions for the agent
            tools: List of tools the agent can use
            temperature: Model temperature for responses
            response_model: Pydantic model for structured output
        """
        self.name = name
        self.role = role
        self.response_model = response_model
        
        # Build agent configuration
        agent_config = {
            "name": name,
            "model": Gemini(id=GEMINI_MODEL),
            "instructions": instructions,
            "tools": tools or [],
            "markdown": True,
            "output_schema": response_model
        }
        
        self.agent = Agent(**agent_config)
    
    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Union[str, BaseModel]:
        """
        Execute a task with the agent
        
        Args:
            task: Task description
            context: Additional context information
        
        Returns:
            Agent's response (string or Pydantic model if response_model is set)
        """
        prompt = task
        if context:
            prompt = f"Context: {context}\n\nTask: {task}"
        
        response = self.agent.run(prompt)
        print("response:", response)
        # If using structured output, return the Pydantic model directly
        if self.response_model and isinstance(response, BaseModel):
            return response
        
        # Otherwise return string content
        return response.content if hasattr(response, 'content') else str(response)
    
    def run_structured(self, task: str, context: Optional[Dict[str, Any]] = None) -> BaseModel:
        """
        Execute a task with the agent and ensure structured output
        
        Args:
            task: Task description
            context: Additional context information
        
        Returns:
            Pydantic model instance
        
        Raises:
            ValueError: If response_model is not configured
        """
        if not self.response_model:
            raise ValueError(f"Agent {self.name} does not have a response_model configured for structured output")
        
        response = self.run(task, context)
        
        if not isinstance(response, BaseModel):
            raise ValueError(f"Expected structured output but got {type(response)}")
        
        return response
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', role='{self.role}')>"
