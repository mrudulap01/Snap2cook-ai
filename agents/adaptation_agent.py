import json
from pydantic import ValidationError
from typing import Dict, Any

from agents.base_agent import BaseAgent
from schemas.models import Recipe, PantryInventory, AdaptationResult
from agents.prompts import ADAPTATION_AGENT_PROMPT
from utils.ai_client import AIClient, ModelUnavailableError

class RecipeAdaptationAgent(BaseAgent):
    """
    Agent responsible for adapting a recipe based on available pantry ingredients.
    """
    def __init__(self):
        super().__init__(name="RecipeAdaptationAgent")
        self.client = AIClient()

    async def process(self, input_data: Dict[str, Any]) -> AdaptationResult:
        recipe: Recipe = input_data.get("recipe")
        inventory: PantryInventory = input_data.get("inventory")
        
        self.logger.info(f"Adapting recipe '{recipe.dish_name}' with {len(inventory.available_ingredients)} available ingredients.")
        
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
        
        try:
            adaptation_result = await self.client.generate_text(
                messages=messages, 
                response_model=AdaptationResult
            )
            
            self.logger.info(f"Successfully adapted recipe. Compatibility: {adaptation_result.compatibility_score}%")
            return adaptation_result
        except ModelUnavailableError as e:
            self.logger.error(f"Model Unavailable: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during API call: {e}")
            raise e
