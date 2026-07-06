from typing import Dict, Any

def get_substitutes(ingredient: str) -> Dict[str, Any]:
    """
    Looks up substitutes for a given ingredient.
    """
    # TODO: Implement actual lookup logic or API call
    return {
        "ingredient": ingredient,
        "substitutes": [f"Substitute 1 for {ingredient}", f"Substitute 2 for {ingredient}"]
    }
