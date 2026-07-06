from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class DetectedIngredient(BaseModel):
    name: str
    confidence: float
    category: Optional[str] = None # Vegetables, Fruits, Dairy, Spices, Condiments, Dry Goods, Frozen Items, Canned Items

class DishAnalysis(BaseModel):
    chain_of_thought: str = Field(description="Step-by-step reasoning for identifying the dish and estimating hidden ingredients")
    dish_name: str
    alternate_names: List[str]
    cuisine: Optional[str]
    region: Optional[str]
    visible_ingredients: List[str]
    estimated_hidden_ingredients: List[str]
    cooking_techniques: List[str]
    dish_category: Optional[str]
    estimated_servings: int
    top_3_possible_dishes: Optional[List[str]] = Field(default_factory=list, description="Populated if confidence is below 70%")
    confidence: float

class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: str

class NutritionBreakdown(BaseModel):
    calories: int
    protein: int
    carbs: int
    fat: int
    fiber: int
    sugar: int
    sodium: int

class Nutrition(BaseModel):
    per_serving: NutritionBreakdown
    entire_recipe: NutritionBreakdown

class RecipeStep(BaseModel):
    step_number: int
    instruction: str
    duration_minutes: Optional[int]
    expected_outcome: str

class Recipe(BaseModel):
    chain_of_thought: str = Field(description="Step-by-step reasoning for reconstructing the recipe and calculating nutrition")
    dish_name: str
    cuisine: str
    description: str
    servings: int
    prep_time: int
    cook_time: int
    resting_time: int
    total_time: int
    difficulty: str
    ingredients: List[Ingredient]
    steps: List[RecipeStep]
    chef_tips: List[str]
    common_mistakes: List[str]
    storage_instructions: str
    serving_suggestions: str
    nutrition: Nutrition

class PantryInventory(BaseModel):
    available_ingredients: List[DetectedIngredient]

class Substitution(BaseModel):
    original_ingredient: str
    substitute: str
    reason: str

class AdaptationResult(BaseModel):
    chain_of_thought: str = Field(description="Step-by-step reasoning for ingredient substitutions and recipe adjustments")
    available_ingredients: List[str]
    missing_ingredients: List[Ingredient]
    substitutions: List[Substitution]
    shopping_list: List[str]
    compatibility_score: int
    compatibility_explanation: str
    adapted_recipe: Recipe
