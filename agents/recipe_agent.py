import json
from pydantic import ValidationError

from agents.base_agent import BaseAgent
from schemas.models import DishAnalysis, Recipe
from agents.prompts import RECIPE_AGENT_PROMPT
from utils.ai_client import AIClient, ModelUnavailableError

class RecipeReconstructionAgent(BaseAgent):
    """
    Agent responsible for reconstructing a full recipe from dish analysis.
    """
    def __init__(self):
        super().__init__(name="RecipeReconstructionAgent")
        self.client = AIClient()

    async def process(self, dish_analysis: DishAnalysis) -> Recipe:
        self.logger.info(f"Reconstructing recipe for: {dish_analysis.dish_name}")
        
        context_data = {
            "dish_name": dish_analysis.dish_name,
            "alternate_names": dish_analysis.alternate_names,
            "cuisine": dish_analysis.cuisine,
            "region": dish_analysis.region,
            "visible_ingredients": dish_analysis.visible_ingredients,
            "cooking_techniques": dish_analysis.cooking_techniques,
            "dish_category": dish_analysis.dish_category
        }
        
        prompt = RECIPE_AGENT_PROMPT.replace("{context}", json.dumps(context_data, indent=2))
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        try:
            recipe = await self.client.generate_text(
                messages=messages, 
                response_model=Recipe
            )
            
            self.logger.info(f"Successfully reconstructed recipe: {recipe.dish_name}")
            return recipe
        except ModelUnavailableError as e:
            self.logger.error(f"Model Unavailable: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during API call: {e}")
            raise e
