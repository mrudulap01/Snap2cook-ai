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
        """Register an agent and attach the global session context."""
        agent.attach_session(self.session)
        self.agents[agent.name] = agent

    def get_agent(self, agent_name: str) -> BaseAgent:
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not registered in ADK Runner.")
        return self.agents[agent_name]

    async def execute_agent(self, agent_name: str, payload: Any) -> Any:
        agent = self.get_agent(agent_name)
        
        self.callbacks.on_agent_start(agent_name, payload)
        start_time = time.time()
        
        try:
            # Set Active Agent Context
            self.session.context.variables["active_agent"] = agent_name
            
            result = await agent.process(payload)
            
            execution_time = time.time() - start_time
            self.callbacks.on_agent_end(agent_name, result, execution_time)
            
            # Log to Session History
            self.session.log_interaction(
                agent_name=agent_name, 
                payload=payload, 
                result=result,
                metadata={"execution_time": execution_time}
            )
            
            return result
        except Exception as e:
            self.callbacks.on_agent_error(agent_name, e)
            raise e

    async def execute_handoff(self, from_agent: str, to_agent: str, payload: Any) -> Any:
        """ADK Pattern: Execute a smooth handoff between agents, preserving context."""
        self.callbacks.on_agent_end(from_agent, "HANDOFF_INITIATED", 0)
        self.session.log_interaction(from_agent, payload, f"HANDOFF TO {to_agent}")
        return await self.execute_agent(to_agent, payload)
