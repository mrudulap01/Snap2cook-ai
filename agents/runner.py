import time
from typing import Dict, Any, Type
from agents.base_agent import BaseAgent
from agents.sessions import ADKSession
from agents.callbacks import AgentCallbackHandler

class ADKRunner:
    """ADK Pattern: Central orchestrator that handles execution, sessions, and handoffs."""
    def __init__(self):
        self.session = ADKSession()
        self.callbacks = AgentCallbackHandler()
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent):
        self.agents[agent.name] = agent

    async def execute_agent(self, agent_name: str, payload: Any) -> Any:
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not registered in ADK Runner.")
            
        agent = self.agents[agent_name]
        
        self.callbacks.on_agent_start(agent_name, payload)
        start_time = time.time()
        
        try:
            result = await agent.process(payload)
            execution_time = time.time() - start_time
            self.callbacks.on_agent_end(agent_name, result, execution_time)
            self.session.log_interaction(agent_name, payload, result)
            return result
        except Exception as e:
            self.callbacks.on_agent_error(agent_name, e)
            raise e
