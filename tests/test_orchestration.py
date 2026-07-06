import pytest
import asyncio
from agents.orchestrator import Snap2CookOrchestrator
from agents.runner import ADKRunner
from agents.sessions import ADKSession

@pytest.mark.asyncio
async def test_runner_registration():
    runner = ADKRunner()
    assert runner.agents == {}
    
    # Test orchestrator sets up agents
    orchestrator = Snap2CookOrchestrator()
    assert "VisionAnalysisAgent" in orchestrator.runner.agents
    assert "RecipeReconstructionAgent" in orchestrator.runner.agents
    
    # Test session attached
    agent = orchestrator.runner.agents["VisionAnalysisAgent"]
    assert agent.session is not None
    assert isinstance(agent.session, ADKSession)

def test_session_logging():
    session = ADKSession()
    session.log_interaction("TestAgent", "payload1", "result1")
    assert len(session.history) == 1
    assert session.history[0]["agent"] == "TestAgent"
