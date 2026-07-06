import pytest
from mcp_server.server import get_nutrition, convert_unit, scale_recipe, suggest_substitution

def test_get_nutrition():
    # Test butter
    nut = get_nutrition("butter", 1, "tbsp")
    assert nut.fat > 10
    
    # Test sugar
    nut2 = get_nutrition("sugar", 100, "g")
    assert nut2.carbs > 80
    assert nut2.fat == 0

def test_convert_unit():
    assert "240.0" in convert_unit(1, "cup", "ml")
    assert "28.3" in convert_unit(1, "oz", "g")
    
def test_scale_recipe():
    assert scale_recipe(2, 4, 100) == 200
    assert scale_recipe(4, 2, 100) == 50

def test_suggest_substitution():
    sub = suggest_substitution("butter")
    assert "Olive Oil" in sub.substitutes
    
    sub2 = suggest_substitution("unknown_item")
    assert "No direct substitute found" in sub2.substitutes[0]
