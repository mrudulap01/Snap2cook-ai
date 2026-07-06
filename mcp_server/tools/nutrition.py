from typing import Dict, Any

def get_nutrition_info(ingredient: str) -> Dict[str, Any]:
    """
    Retrieves nutritional information for a given ingredient.
    """
    # TODO: Implement external API call (e.g. USDA)
    return {
        "ingredient": ingredient,
        "calories_per_100g": 0,
        "protein_g": 0.0,
        "fat_g": 0.0,
        "carbs_g": 0.0
    }
