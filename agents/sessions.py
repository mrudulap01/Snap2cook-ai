import uuid
from typing import Dict, Any

class ADKSession:
    """ADK Pattern: Manages state across a multi-agent orchestration session."""
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.memory: Dict[str, Any] = {}
        self.history: list = []
        
    def set(self, key: str, value: Any):
        self.memory[key] = value
        
    def get(self, key: str) -> Any:
        return self.memory.get(key)
        
    def log_interaction(self, agent_name: str, payload: Any, result: Any):
        self.history.append({
            "agent": agent_name,
            "payload": payload,
            "result": result
        })
