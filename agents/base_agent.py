from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable
from utils.logger import get_logger

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the Snap2Cook AI system.
    Implements ADK Core Patterns.
    """
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.logger = get_logger(self.name)
        self.tools: Dict[str, Callable] = {}
        self.session = None

    def register_tool(self, tool_name: str, tool_func: Callable):
        """ADK Pattern: Registers a tool that this agent can execute."""
        self.tools[tool_name] = tool_func
        self.logger.debug(f"Registered tool: {tool_name}")

    def attach_session(self, session: Any):
        """ADK Pattern: Attaches the global session context to the agent."""
        self.session = session

    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """
        Process the input data and return the agent's specific output.
        Must be implemented by subclasses.
        """
        pass
