import json
from pydantic import ValidationError
from openai import AsyncOpenAI
from typing import Dict, Any

from agents.base_agent import BaseAgent
from schemas.models import Recipe, PantryInventory, AdaptationResult
from agents.prompts import ADAPTATION_AGENT_PROMPT
from config.settings import settings

class RecipeAdaptationAgent(BaseAgent):
    """
    Agent responsible for adapting a recipe based on available pantry ingredients via OpenRouter.
    """
    def __init__(self):
        super().__init__(name="RecipeAdaptationAgent")
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY
        )
        self.model_id = "google/gemini-2.5-flash"

    async def process(self, input_data: Dict[str, Any]) -> AdaptationResult:
        recipe: Recipe = input_data.get("recipe")
        inventory: PantryInventory = input_data.get("inventory")
        
        self.logger.info(f"Adapting recipe '{recipe.dish_name}' with {len(inventory.available_ingredients)} available ingredients.")
        
        attempt = 0
        max_attempts = 2
        
        recipe_context = recipe.model_dump_json(indent=2)
        inventory_context = inventory.model_dump_json(indent=2)
        
        prompt = ADAPTATION_AGENT_PROMPT.replace(
            "{recipe_context}", recipe_context
        ).replace(
            "{inventory_context}", inventory_context
        )
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        while attempt < max_attempts:
            attempt += 1
            try:
                self.logger.info(f"Calling OpenRouter API for Adaptation (Attempt {attempt}/{max_attempts})")
                
                response = await self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    response_format={"type": "json_object"},
                    max_tokens=8000
                )
                
                response_text = response.choices[0].message.content.strip()
                
                parsed_data = json.loads(response_text)
                adaptation_result = AdaptationResult(**parsed_data)
                
                self.logger.info(f"Successfully adapted recipe. Compatibility: {adaptation_result.compatibility_score}%")
                return adaptation_result
                
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
