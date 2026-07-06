from typing import Dict, Any, Optional
from utils.logger import get_logger
from agents.runner import ADKRunner
from agents.vision_agent import VisionAnalysisAgent
from agents.recipe_agent import RecipeReconstructionAgent
from agents.pantry_agent import PantryInventoryAgent
from agents.adaptation_agent import RecipeAdaptationAgent

class Snap2CookOrchestrator:
    """
    Orchestrates the workflow between the different agents using Google ADK patterns.
    """
    def __init__(self):
        self.logger = get_logger("Snap2CookOrchestrator")
        self.runner = ADKRunner()
        
        # Register Agents
        self.runner.register_agent(VisionAnalysisAgent())
        self.runner.register_agent(RecipeReconstructionAgent())
        self.runner.register_agent(PantryInventoryAgent())
        self.runner.register_agent(RecipeAdaptationAgent())

    async def run_full_workflow(self, dish_image_path: str) -> Dict[str, Any]:
        """
        Executes the main dish analysis workflow.
        """
        self.logger.info("Starting Snap2Cook workflow via ADK Runner")
        
        # Handoff to Vision Agent
        dish_analysis = await self.runner.execute_agent("VisionAnalysisAgent", dish_image_path)
        
        # Handoff to Recipe Agent
        recipe = await self.runner.execute_agent("RecipeReconstructionAgent", dish_analysis)
        
        return {
            "dish_analysis": dish_analysis,
            "original_recipe": recipe
        }
        
    async def run_adaptation_workflow(self, pantry_image_path: str, recipe: Any) -> Dict[str, Any]:
        """
        Executes the pantry adaptation workflow.
        """
        self.logger.info("Starting Adaptation workflow via ADK Runner")
        
        # Handoff to Pantry Agent
        pantry_inventory = await self.runner.execute_agent("PantryInventoryAgent", pantry_image_path)
        
        # Handoff to Adaptation Agent
        adaptation_input = {
            "recipe": recipe,
            "inventory": pantry_inventory
        }
        adaptation_result = await self.runner.execute_agent("RecipeAdaptationAgent", adaptation_input)
        
        return {
            "pantry_inventory": pantry_inventory,
            "adaptation_result": adaptation_result
        }
