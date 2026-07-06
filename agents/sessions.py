import uuid
import time
from typing import Dict, Any, List

class ADKMemory:
    """ADK Pattern: Ephemeral and persistent memory store."""
    def __init__(self):
        self.store: Dict[str, Any] = {}
        
    def set(self, key: str, value: Any):
        self.store[key] = value
        
    def get(self, key: str, default: Any = None) -> Any:
        return self.store.get(key, default)

class ADKContext:
    """ADK Pattern: Shared context for agent handoffs and tool execution."""
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.tool_results: List[Dict[str, Any]] = []

class ADKSession:
    """ADK Pattern: Manages state across a multi-agent orchestration session."""
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.memory = ADKMemory()
        self.context = ADKContext()
        self.history: List[Dict[str, Any]] = []
        self.start_time = time.time()
        
    def log_interaction(self, agent_name: str, payload: Any, result: Any, metadata: Dict[str, Any] = None):
        entry = {
            "timestamp": time.time(),
            "agent": agent_name,
            "payload": payload,
            "result": result,
            "metadata": metadata or {}
        }
        self.history.append(entry)
        
    def get_session_duration(self) -> float:
        return time.time() - self.start_time
