import pytest
import json
from unittest.mock import MagicMock, patch
from pydantic import ValidationError
from PIL import Image

from agents.vision_agent import VisionAnalysisAgent
from schemas.models import DishAnalysis

@pytest.fixture
def mock_genai_client():
    with patch('agents.vision_agent.genai.Client') as MockClient:
        mock_client_instance = MockClient.return_value
        yield mock_client_instance

@pytest.fixture
def mock_valid_json():
    return json.dumps({
        "dish_name": "Test Pizza",
        "cuisine": "Italian",
        "visible_ingredients": ["cheese", "tomato", "dough"],
        "cooking_techniques": ["baked"],
        "confidence": 0.95
    })

@pytest.mark.asyncio
async def test_vision_agent_success(sample_image, mock_genai_client, mock_valid_json):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.text = mock_valid_json
    mock_genai_client.models.generate_content.return_value = mock_response

    # Initialize agent
    agent = VisionAnalysisAgent()
    
    # Process
    result = await agent.process(sample_image)
    
    # Verify
    assert isinstance(result, DishAnalysis)
    assert result.dish_name == "Test Pizza"
    assert result.cuisine == "Italian"
    assert len(result.visible_ingredients) == 3
    assert result.confidence == 0.95
    
    # Verify gemini API was called exactly once
    assert mock_genai_client.models.generate_content.call_count == 1

@pytest.mark.asyncio
async def test_vision_agent_retry_on_invalid_json(sample_image, mock_genai_client, mock_valid_json):
    # Setup mock responses: first invalid, second valid
    mock_response_invalid = MagicMock()
    mock_response_invalid.text = "This is not valid JSON"
    
    mock_response_valid = MagicMock()
    mock_response_valid.text = mock_valid_json
    
    # Side effect allows returning different values on consecutive calls
    mock_genai_client.models.generate_content.side_effect = [
        mock_response_invalid,
        mock_response_valid
    ]

    # Initialize agent
    agent = VisionAnalysisAgent()
    
    # Process
    result = await agent.process(sample_image)
    
    # Verify
    assert isinstance(result, DishAnalysis)
    assert result.dish_name == "Test Pizza"
    
    # Verify gemini API was called exactly twice due to the retry logic
    assert mock_genai_client.models.generate_content.call_count == 2

@pytest.mark.asyncio
async def test_vision_agent_fails_after_max_retries(sample_image, mock_genai_client):
    # Setup mock response: always invalid
    mock_response_invalid = MagicMock()
    mock_response_invalid.text = "Still not valid JSON"
    
    mock_genai_client.models.generate_content.return_value = mock_response_invalid

    # Initialize agent
    agent = VisionAnalysisAgent()
    
    # Process and expect exception
    with pytest.raises(ValueError, match="Failed to parse Gemini JSON response after 2 attempts"):
        await agent.process(sample_image)
        
    assert mock_genai_client.models.generate_content.call_count == 2
