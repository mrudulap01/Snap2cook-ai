import json
from pathlib import Path
from pydantic import ValidationError

from agents.base_agent import BaseAgent
from schemas.models import DishAnalysis
from agents.prompts import VISION_AGENT_PROMPT
from utils.ai_client import AIClient, ModelUnavailableError
from utils.image_utils import encode_image_to_base64

class VisionAnalysisAgent(BaseAgent):
    """
    Agent responsible for analyzing food images to detect the dish name,
    cuisine, ingredients, and confidence scores.
    """
    def __init__(self):
        super().__init__(name="VisionAnalysisAgent")
        self.client = AIClient()

    async def process(self, image_path: str) -> DishAnalysis:
        self.logger.info("Starting vision analysis.")
        
        base64_image = encode_image_to_base64(image_path)
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": VISION_AGENT_PROMPT
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base64_image
                        }
                    }
                ]
            }
        ]
        
        try:
            dish_analysis = await self.client.generate_vision(
                messages=messages, 
                response_model=DishAnalysis
            )
            
            self.logger.info(f"Successfully analyzed dish: {dish_analysis.dish_name} with {dish_analysis.confidence} confidence.")
            return dish_analysis
        except ModelUnavailableError as e:
            self.logger.error(f"Model Unavailable: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during API call: {e}")
            raise e
