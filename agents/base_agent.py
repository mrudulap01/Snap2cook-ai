from abc import ABC, abstractmethod
from typing import Any
from utils.logger import get_logger

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the Snap2Cook AI system.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(self.name)

    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """
        Process the input data and return the agent's specific output.
        Must be implemented by subclasses.
        """
        pass
