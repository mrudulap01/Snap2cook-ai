from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List
from pydantic import BaseModel
import random

# Create an MCP server
mcp = FastMCP("Snap2Cook MCP Tools")

# --- Tool 1: Ingredient Substitution ---
class SubstitutionResponse(BaseModel):
    substitutes: List[str]
    explanation: str

@mcp.tool()
def suggest_substitution(ingredient: str) -> SubstitutionResponse:
    """Provides common culinary substitutions for a given ingredient."""
    substitutions = {
        "chicken": {"subs": ["Paneer", "Tofu", "Seitan", "Mushroom"], "exp": "These absorb marinades well and provide a hearty texture."},
        "butter": {"subs": ["Olive Oil", "Coconut Oil", "Ghee", "Applesauce"], "exp": "Provides similar fat content. Applesauce works for baking moisture."},
        "heavy cream": {"subs": ["Milk and Cornstarch", "Coconut Milk", "Cashew Cream"], "exp": "These alternatives mimic the thickness and creaminess of heavy cream."},
        "egg": {"subs": ["Flax egg", "Applesauce", "Mashed banana"], "exp": "Acts as a binder in baking recipes."},
        "sugar": {"subs": ["Honey", "Maple Syrup", "Agave", "Stevia"], "exp": "Adds sweetness. Liquid sweeteners may require adjusting dry ingredients."}
    }
    
    match = substitutions.get(ingredient.lower().strip())
    if match:
        return SubstitutionResponse(substitutes=match["subs"], explanation=match["exp"])
    else:
        return SubstitutionResponse(substitutes=["No direct substitute found in DB"], explanation="Try researching flavor profiles online.")

# --- Tool 2: Nutrition Lookup ---
class NutritionData(BaseModel):
    calories: int
    protein: int
    fat: int
    carbs: int
    fiber: int
    sugar: int

@mcp.tool()
def get_nutrition(ingredient: str, quantity: float, unit: str) -> NutritionData:
    """Simulates a USDA nutrition database lookup for a specific ingredient."""
    # Simplified simulation logic
    base_cal = random.randint(20, 200)
    multiplier = quantity if unit in ["g", "ml", "cup", "tbsp"] else 1.0
    
    return NutritionData(
        calories=int(base_cal * multiplier),
        protein=int((base_cal * 0.1) * multiplier),
        fat=int((base_cal * 0.05) * multiplier),
        carbs=int((base_cal * 0.2) * multiplier),
        fiber=int((base_cal * 0.02) * multiplier),
        sugar=int((base_cal * 0.03) * multiplier)
    )

# --- Tool 3: Unit Conversion ---
@mcp.tool()
def convert_unit(value: float, from_unit: str, to_unit: str) -> str:
    """Converts volume and weight units (e.g. cups to ml, g to oz)."""
    conversions = {
        ("cup", "ml"): 240.0,
        ("ml", "cup"): 1 / 240.0,
        ("g", "oz"): 0.035274,
        ("oz", "g"): 28.3495,
        ("tbsp", "ml"): 15.0,
        ("ml", "tbsp"): 1 / 15.0,
        ("tsp", "ml"): 5.0,
        ("ml", "tsp"): 1 / 5.0
    }
    
    key = (from_unit.lower().strip(), to_unit.lower().strip())
    factor = conversions.get(key)
    
    if factor:
        converted = value * factor
        return f"{converted:.2f} {to_unit}"
    else:
        return "Conversion not supported in basic DB."

# --- Tool 4: Recipe Scaling ---
@mcp.tool()
def scale_recipe(original_servings: int, target_servings: int, ingredient_quantity: float) -> float:
    """Calculates the new quantity of an ingredient based on serving size changes."""
    if original_servings <= 0:
        return ingredient_quantity
    ratio = target_servings / original_servings
    return ingredient_quantity * ratio

# --- Tool 5: Cooking Technique Helper ---
@mcp.tool()
def explain_technique(technique: str) -> Dict[str, str]:
    """Explains a cooking technique and lists common mistakes."""
    techniques = {
        "braise": {
            "explanation": "To fry food lightly and then stew it slowly in a closed container.",
            "mistakes": ["Not searing the meat first.", "Using too much liquid."]
        },
        "blanch": {
            "explanation": "To scald in boiling water for a short time, then plunge into ice water.",
            "mistakes": ["Leaving in boiling water too long.", "Skipping the ice bath."]
        },
        "saute": {
            "explanation": "To fry quickly in a little hot fat.",
            "mistakes": ["Crowding the pan.", "Not preheating the pan enough."]
        }
    }
    
    return techniques.get(technique.lower().strip(), {
        "explanation": "Basic cooking technique.",
        "mistakes": ["Check temperature", "Monitor closely"]
    })

if __name__ == "__main__":
    # This enables running the server locally via stdio or SSE
    mcp.run()
