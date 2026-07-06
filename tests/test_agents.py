import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from agents.orchestrator import Snap2CookOrchestrator
from schemas.models import DishAnalysis, Recipe, Nutrition, NutritionBreakdown

@pytest.mark.asyncio
@patch("agents.runner.ADKRunner.execute_agent")
async def test_orchestrator_full_workflow(mock_execute):
    # Mock Vision Output
    mock_vision = DishAnalysis(
        chain_of_thought="Looks like pasta.",
        dish_name="Test Dish",
        alternate_names=[],
        cuisine="Italian",
        region="",
        visible_ingredients=[],
        estimated_hidden_ingredients=[],
        cooking_techniques=[],
        dish_category="Main",
        estimated_servings=4,
        top_3_possible_dishes=[],
        confidence=0.99
    )
    
    # Mock Recipe Output
    mock_recipe = Recipe(
        chain_of_thought="I will reconstruct the pasta.",
        dish_name="Test Dish",
        cuisine="Italian",
        description="Test",
        servings=4,
        prep_time=10,
        cook_time=20,
        resting_time=0,
        total_time=30,
        difficulty="Easy",
        ingredients=[],
        steps=[],
        chef_tips=[],
        common_mistakes=[],
        storage_instructions="",
        serving_suggestions="",
        nutrition=Nutrition(
            per_serving=NutritionBreakdown(calories=1, protein=1, carbs=1, fat=1, fiber=1, sugar=1, sodium=1),
            entire_recipe=NutritionBreakdown(calories=4, protein=4, carbs=4, fat=4, fiber=4, sugar=4, sodium=4)
        )
    )
    
    mock_execute.side_effect = [mock_vision, mock_recipe]
    
    orchestrator = Snap2CookOrchestrator()
    result = await orchestrator.run_full_workflow("dummy_path.jpg")
    
    assert result["dish_analysis"].dish_name == "Test Dish"
    assert result["original_recipe"].cuisine == "Italian"
    assert mock_execute.call_count == 2
