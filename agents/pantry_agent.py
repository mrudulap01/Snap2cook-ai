import json
from pathlib import Path
from pydantic import ValidationError

from agents.base_agent import BaseAgent
from schemas.models import PantryInventory
from agents.prompts import PANTRY_AGENT_PROMPT
from utils.ai_client import AIClient, ModelUnavailableError
from utils.image_utils import encode_image_to_base64

class PantryInventoryAgent(BaseAgent):
    """
    Agent responsible for analyzing pantry/fridge images to detect available ingredients.
    """
    def __init__(self):
        super().__init__(name="PantryInventoryAgent")
        self.client = AIClient()

    async def process(self, image_path: str) -> PantryInventory:
        self.logger.info("Starting pantry inventory analysis.")
        
        base64_image = encode_image_to_base64(image_path)
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": PANTRY_AGENT_PROMPT
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
            inventory = await self.client.generate_vision(
                messages=messages, 
                response_model=PantryInventory
            )
            
            self.logger.info(f"Successfully detected {len(inventory.available_ingredients)} ingredients.")
            return inventory
        except ModelUnavailableError as e:
            self.logger.error(f"Model Unavailable: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during API call: {e}")
            raise e
