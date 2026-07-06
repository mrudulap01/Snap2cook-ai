import time
from typing import Dict, Any, Callable
from utils.logger import get_logger

class AgentCallbackHandler:
    """ADK Pattern: Handles events across the agent lifecycle."""
    def __init__(self):
        self.logger = get_logger("CallbackHandler")
        self.callbacks: Dict[str, list[Callable]] = {}

    def register_callback(self, event: str, callback: Callable):
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)

    def trigger(self, event: str, **kwargs):
        if event in self.callbacks:
            for cb in self.callbacks[event]:
                cb(**kwargs)

    def on_agent_start(self, agent_name: str, payload: Any):
        self.logger.info(f"[ADK] Agent {agent_name} started.")
        self.trigger("agent_start", agent_name=agent_name, payload=payload)
        
    def on_agent_end(self, agent_name: str, result: Any, execution_time: float):
        self.logger.info(f"[ADK] Agent {agent_name} finished in {execution_time:.2f}s.")
        self.trigger("agent_end", agent_name=agent_name, result=result, time=execution_time)

    def on_agent_error(self, agent_name: str, error: Exception):
        self.logger.error(f"[ADK] Agent {agent_name} failed: {error}")
        self.trigger("agent_error", agent_name=agent_name, error=error)
