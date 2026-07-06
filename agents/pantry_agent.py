import json
from pathlib import Path
from pydantic import ValidationError
from openai import AsyncOpenAI

from agents.base_agent import BaseAgent
from schemas.models import PantryInventory
from agents.prompts import PANTRY_AGENT_PROMPT
from config.settings import settings
from utils.image_utils import encode_image_to_base64

class PantryInventoryAgent(BaseAgent):
    """
    Agent responsible for analyzing pantry/fridge images to detect available ingredients using OpenRouter.
    """
    def __init__(self):
        super().__init__(name="PantryInventoryAgent")
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY
        )
        self.model_id = "google/gemini-2.5-flash"

    async def process(self, image_path: str) -> PantryInventory:
        self.logger.info("Starting pantry inventory analysis via OpenRouter.")
        
        base64_image = encode_image_to_base64(image_path)
        
        attempt = 0
        max_attempts = 2
        
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
        
        while attempt < max_attempts:
            attempt += 1
            try:
                self.logger.info(f"Calling OpenRouter API for Pantry (Attempt {attempt}/{max_attempts})")
                
                response = await self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    response_format={"type": "json_object"},
                    max_tokens=8000
                )
                
                response_text = response.choices[0].message.content.strip()
                
                parsed_data = json.loads(response_text)
                inventory = PantryInventory(**parsed_data)
                
                self.logger.info(f"Successfully detected {len(inventory.available_ingredients)} ingredients.")
                return inventory
                
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON Parsing Error on attempt {attempt}: {e}")
                if attempt >= max_attempts:
                    raise ValueError(f"Failed to parse OpenRouter JSON response after {max_attempts} attempts.")
            except ValidationError as e:
                self.logger.error(f"Pydantic Validation Error on attempt {attempt}: {e}")
                if attempt >= max_attempts:
                    raise ValueError(f"Failed to validate OpenRouter JSON response after {max_attempts} attempts.")
            except Exception as e:
                self.logger.error(f"Unexpected error during API call: {e}")
                if attempt >= max_attempts:
                    raise e
