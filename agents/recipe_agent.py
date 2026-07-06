import json
from pydantic import ValidationError
from openai import AsyncOpenAI

from agents.base_agent import BaseAgent
from schemas.models import DishAnalysis, Recipe
from agents.prompts import RECIPE_AGENT_PROMPT
from config.settings import settings

class RecipeReconstructionAgent(BaseAgent):
    """
    Agent responsible for reconstructing a full recipe from dish analysis via OpenRouter.
    """
    def __init__(self):
        super().__init__(name="RecipeReconstructionAgent")
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY
        )
        self.model_id = "google/gemini-2.5-flash"

    async def process(self, dish_analysis: DishAnalysis) -> Recipe:
        self.logger.info(f"Reconstructing recipe for: {dish_analysis.dish_name}")
        
        attempt = 0
        max_attempts = 2
        
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
        
        while attempt < max_attempts:
            attempt += 1
            try:
                self.logger.info(f"Calling OpenRouter API for Recipe (Attempt {attempt}/{max_attempts})")
                
                response = await self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    response_format={"type": "json_object"},
                    max_tokens=8000
                )
                
                response_text = response.choices[0].message.content.strip()
                
                parsed_data = json.loads(response_text)
                recipe = Recipe(**parsed_data)
                
                self.logger.info(f"Successfully reconstructed recipe: {recipe.dish_name}")
                return recipe
                
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
