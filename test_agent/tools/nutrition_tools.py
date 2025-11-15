"""
Nutrition Tools for FitCoach AI
Handles meal planning, calorie tracking, and nutrition calculations
"""
import os
import re
import requests
from typing import Dict, List, Optional, Tuple


def calculate_tdee(
    weight: float,
    height: float,
    age: int,
    gender: str,
    activity_level: str
) -> Dict:
    """
    Calculate Total Daily Energy Expenditure (TDEE)
    
    Args:
        weight: Weight in kg
        height: Height in cm
        age: Age in years
        gender: 'male' or 'female'
        activity_level: 'sedentary', 'light', 'moderate', 'active', 'very_active'
    
    Returns:
        Dictionary with BMR, TDEE, and calorie recommendations
    """
    print(f"\n🔧 [TOOL] calculate_tdee(weight={weight}kg, height={height}cm, age={age}, gender={gender}, activity={activity_level})")
    
    # Mifflin-St Jeor equation for BMR
    # BMR = 10*weight + 6.25*height - 5*age + s (s=5 for male, -161 for female)
    gender_offset = 5 if gender.lower() in ['male', 'm'] else -161
    bmr = 10 * weight + 6.25 * height - 5 * age + gender_offset
    
    # Activity level multipliers
    activity_multipliers = {
        'sedentary': 1.2,      # Little/no exercise
        'light': 1.375,        # Light exercise 1-3 days/week
        'moderate': 1.55,      # Moderate exercise 3-5 days/week
        'active': 1.725,       # Hard exercise 6-7 days/week
        'very_active': 1.9     # Physical job + exercise
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
    tdee = bmr * multiplier
    
    # Calculate calorie targets
    maintenance = round(tdee)
    weight_loss = round(tdee - 500)      # 500 cal deficit for ~0.5kg/week loss
    weight_gain = round(tdee + 300)      # 300 cal surplus for lean gain
    
    result = {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "maintenance_calories": maintenance,
        "weight_loss_calories": weight_loss,
        "weight_gain_calories": weight_gain,
        "activity_multiplier": multiplier
    }
    
    print(f"✅ [RESULT] BMR: {result['bmr']} cal, TDEE: {result['tdee']} cal\n")
    
    return result


def generate_meal_plan(
    calories: int,
    diet_preference: str = "balanced",
    restrictions: Optional[List[str]] = None
) -> Dict:
    """
    Generate a personalized meal plan
    
    Args:
        calories: Target daily calories
        diet_preference: 'balanced', 'keto', 'vegan', 'vegetarian', 'paleo'
        restrictions: List of food restrictions (e.g., ['dairy', 'nuts'])
    
    Returns:
        Dictionary with meal plan for the week
    """
    print(f"\n🔧 [TOOL] generate_meal_plan(calories={calories}, diet={diet_preference}, restrictions={restrictions})")
    
    if restrictions is None:
        restrictions = []
    
    # Macro distribution based on diet preference
    macro_ratios = {
        'balanced': {'protein': 0.30, 'carbs': 0.40, 'fats': 0.30},
        'keto': {'protein': 0.25, 'carbs': 0.05, 'fats': 0.70},
        'vegan': {'protein': 0.20, 'carbs': 0.50, 'fats': 0.30},
        'vegetarian': {'protein': 0.25, 'carbs': 0.45, 'fats': 0.30},
        'paleo': {'protein': 0.35, 'carbs': 0.30, 'fats': 0.35}
    }
    
    ratios = macro_ratios.get(diet_preference.lower(), macro_ratios['balanced'])
    
    # Calculate macros in grams (protein: 4 cal/g, carbs: 4 cal/g, fats: 9 cal/g)
    protein_grams = round((calories * ratios['protein']) / 4)
    carbs_grams = round((calories * ratios['carbs']) / 4)
    fats_grams = round((calories * ratios['fats']) / 9)
    
    # Generate sample meals (template-based for now)
    meals = _generate_sample_meals(calories, diet_preference, restrictions)
    
    result = {
        "target_calories": calories,
        "diet_preference": diet_preference,
        "macros": {
            "protein_grams": protein_grams,
            "carbs_grams": carbs_grams,
            "fats_grams": fats_grams,
            "protein_percentage": int(ratios['protein'] * 100),
            "carbs_percentage": int(ratios['carbs'] * 100),
            "fats_percentage": int(ratios['fats'] * 100)
        },
        "restrictions": restrictions,
        "meals": meals
    }
    
    print(f"✅ [RESULT] Generated {diet_preference} meal plan: P:{protein_grams}g C:{carbs_grams}g F:{fats_grams}g\n")
    
    return result


def _generate_sample_meals(calories: int, diet: str, restrictions: List[str]) -> List[Dict]:
    """Generate sample meals based on diet preference"""
    # Split calories across meals
    breakfast_cal = round(calories * 0.25)
    lunch_cal = round(calories * 0.35)
    dinner_cal = round(calories * 0.30)
    snacks_cal = round(calories * 0.10)
    
    # Template meals based on diet type
    if diet == 'keto':
        meals = [
            {"meal": "Breakfast", "calories": breakfast_cal, "description": "Ouă scrambled cu bacon și avocado"},
            {"meal": "Lunch", "calories": lunch_cal, "description": "Salată Caesar cu pui și parmezan"},
            {"meal": "Dinner", "calories": dinner_cal, "description": "Somon la grătar cu broccoli și unt"},
            {"meal": "Snacks", "calories": snacks_cal, "description": "Nuci și brânză"}
        ]
    elif diet == 'vegan':
        meals = [
            {"meal": "Breakfast", "calories": breakfast_cal, "description": "Ovăz cu banană și unt de arahide"},
            {"meal": "Lunch", "calories": lunch_cal, "description": "Bowl cu quinoa, năut și legume"},
            {"meal": "Dinner", "calories": dinner_cal, "description": "Tofu stir-fry cu orez brun"},
            {"meal": "Snacks", "calories": snacks_cal, "description": "Fructe și semințe"}
        ]
    else:  # balanced
        meals = [
            {"meal": "Breakfast", "calories": breakfast_cal, "description": "Ouă + ovăz cu fructe"},
            {"meal": "Lunch", "calories": lunch_cal, "description": "Piept de pui + orez + legume"},
            {"meal": "Dinner", "calories": dinner_cal, "description": "Pește + cartofi dulci + salată"},
            {"meal": "Snacks", "calories": snacks_cal, "description": "Iaurt grecesc cu fructe"}
        ]
    
    return meals


def track_calories(meal_description: str) -> Dict:
    """
    Track calories from a meal description using USDA FoodData Central API (FREE)
    Parses multiple ingredients and searches each separately for accuracy
    
    Args:
        meal_description: Description of the meal (e.g., "100g oats, 300ml milk, 5 eggs")
    
    Returns:
        Dictionary with estimated calories and macros, or request for more details
    """
    print(f"\n🔧 [TOOL] track_calories(meal='{meal_description}')")
    
    # Get USDA API key from environment
    api_key = os.getenv("USDA_API_KEY")
    
    if not api_key:
        result = {
            "meal": meal_description,
            "calories": 0,
            "protein_grams": 0,
            "carbs_grams": 0,
            "fats_grams": 0,
            "error": "USDA_API_KEY not found in .env file. Get free key at: https://fdc.nal.usda.gov/api-key-signup.html",
            "status": "error"
        }
        print(f"❌ [ERROR] No USDA API key found\n")
        return result
    
    # Parse ingredients from description
    ingredients = _parse_ingredients(meal_description)
    
    if not ingredients:
        result = {
            "meal": meal_description,
            "status": "need_clarification",
            "message": "I need more details about the meal. Please specify:",
            "questions": [
                "What foods did you eat? (e.g., 'chicken', 'rice', 'eggs')",
                "How much of each? (e.g., '100g', '2 pieces', '1 cup')",
                "If applicable: cooked or raw? (e.g., 'rice cooked', 'chicken raw')"
            ],
            "example": "Try: '100g oats, 300ml milk, 5 eggs' or 'grilled chicken breast 150g, cooked rice 200g'"
        }
        print(f"⚠️ [WARNING] Need clarification on meal details\n")
        return result
    
    # Check for missing details (foods without quantities or preparation)
    needs_clarification = _check_missing_details(ingredients)
    if needs_clarification:
        result = {
            "meal": meal_description,
            "status": "need_clarification",
            "message": "I found these foods but need more details:",
            "missing_details": needs_clarification,
            "example": "For rice, please specify: 'cooked rice 200g' or 'raw rice 50g'"
        }
        print(f"⚠️ [WARNING] Missing details: {needs_clarification}\n")
        return result
    
    # Search USDA API for each ingredient
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0
    foods_breakdown = []
    
    for ingredient in ingredients:
        food_name = ingredient['food']
        quantity = ingredient.get('quantity', 100)  # default 100g
        unit = ingredient.get('unit', 'g')
        
        # Search USDA for this specific food
        nutrition = _search_usda_food(api_key, food_name)
        
        if nutrition:
            # Calculate based on quantity
            multiplier = _calculate_multiplier(quantity, unit, nutrition.get('serving_size', 100))
            
            cal = nutrition['calories'] * multiplier
            prot = nutrition['protein'] * multiplier
            carb = nutrition['carbs'] * multiplier
            fat = nutrition['fats'] * multiplier
            
            total_calories += cal
            total_protein += prot
            total_carbs += carb
            total_fats += fat
            
            foods_breakdown.append({
                "food": nutrition['name'],
                "quantity": f"{quantity}{unit}",
                "calories": round(cal),
                "protein": round(prot, 1),
                "carbs": round(carb, 1),
                "fats": round(fat, 1)
            })
        else:
            # Food not found in USDA
            foods_breakdown.append({
                "food": food_name,
                "quantity": f"{quantity}{unit}",
                "error": "Not found in USDA database",
                "suggestion": f"Try being more specific: '{food_name} cooked' or '{food_name} raw'"
            })
    
    result = {
        "meal": meal_description,
        "total_calories": round(total_calories),
        "total_protein_grams": round(total_protein, 1),
        "total_carbs_grams": round(total_carbs, 1),
        "total_fats_grams": round(total_fats, 1),
        "foods_breakdown": foods_breakdown,
        "status": "success" if total_calories > 0 else "partial",
        "source": "USDA FoodData Central"
    }
    
    print(f"✅ [RESULT] Total: {result['total_calories']} cal (P:{result['total_protein_grams']}g C:{result['total_carbs_grams']}g F:{result['total_fats_grams']}g)\n")
    
    return result


def _parse_ingredients(description: str) -> List[Dict]:
    """
    Parse meal description into individual ingredients with quantities
    Examples:
        "100g oats, 300ml milk, 5 eggs" -> [{"food": "oats", "quantity": 100, "unit": "g"}, ...]
        "2 chicken breast, rice" -> [{"food": "chicken breast", "quantity": 2, "unit": "piece"}, ...]
    """
    # Split by common separators
    parts = re.split(r',|\band\b|\+', description.lower())
    
    ingredients = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Try to extract quantity and unit
        # Patterns: "100g oats", "300ml milk", "5 eggs", "2 chicken breast"
        match = re.match(r'(\d+\.?\d*)\s*(g|kg|ml|l|oz|cup|piece|pieces|tbsp|tsp)?\s*(.+)', part)
        
        if match:
            quantity = float(match.group(1))
            unit = match.group(2) or 'g'
            food_name = match.group(3).strip()
            
            # Convert units to grams/ml
            if unit in ['kg']:
                quantity *= 1000
                unit = 'g'
            elif unit in ['l']:
                quantity *= 1000
                unit = 'ml'
            elif unit in ['piece', 'pieces']:
                # Keep as count
                pass
            
            ingredients.append({
                "food": food_name,
                "quantity": quantity,
                "unit": unit
            })
        else:
            # No quantity found - just food name
            ingredients.append({
                "food": part,
                "quantity": None,
                "unit": None
            })
    
    return ingredients


def _check_missing_details(ingredients: List[Dict]) -> List[str]:
    """
    Check if ingredients are missing important details (quantity, preparation method)
    """
    missing = []
    
    for ing in ingredients:
        food = ing['food']
        quantity = ing.get('quantity')
        
        # Check if quantity is missing
        if quantity is None:
            missing.append(f"'{food}' - needs quantity (e.g., '100g {food}' or '2 {food}')")
            continue
        
        # Check for ambiguous foods that need preparation details
        ambiguous_foods = ['rice', 'pasta', 'oats', 'oatmeal', 'chicken', 'potato', 'beans']
        
        for ambiguous in ambiguous_foods:
            if ambiguous in food and 'cooked' not in food and 'raw' not in food and 'grilled' not in food:
                missing.append(f"'{food}' - is it cooked or raw? (e.g., 'cooked {food}' or 'raw {food}')")
                break
    
    return missing


def _search_usda_food(api_key: str, food_name: str) -> Optional[Dict]:
    """
    Search USDA FoodData Central for a specific food
    Returns nutrition per 100g
    """
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    
    # Improve search terms for better matches
    improved_query = food_name
    if 'egg' in food_name.lower() and 'white' not in food_name.lower():
        improved_query = "egg whole raw"
    elif 'chicken' in food_name.lower():
        improved_query = f"{food_name} raw"
    elif 'rice' in food_name.lower():
        improved_query = f"{food_name} cooked"
    
    params = {
        "api_key": api_key,
        "query": improved_query,
        "pageSize": 5,  # Get top 5 to find best match
        "dataType": ["Foundation", "SR Legacy"]
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        print(f"   🔍 USDA API Response for '{food_name}': Found {len(result.get('foods', []))} results")
        
        if not result.get('foods'):
            print(f"   ❌ No results found for '{food_name}'")
            return None
        
        # Select best match (prefer "whole" for eggs, avoid "white" or "yolk")
        foods = result['foods']
        best_food = None
        
        for food in foods:
            desc = food.get('description', '').lower()
            print(f"   🔎 Option: {food.get('description', 'N/A')}")
            
            # Skip egg whites/yolks if looking for whole eggs
            if 'egg' in food_name.lower():
                if 'white' in desc or 'yolk' in desc:
                    continue
                if 'whole' in desc:
                    best_food = food
                    break
            
            if best_food is None:
                best_food = food
        
        if best_food is None:
            best_food = foods[0]
        
        food_desc = best_food.get('description', food_name)
        print(f"   ✅ Selected: {food_desc}")
        
        # Extract nutrients per 100g
        calories = 0
        protein = 0
        carbs = 0
        fats = 0
        
        nutrients_found = []
        for nutrient in best_food.get('foodNutrients', []):
            nutrient_name = nutrient.get('nutrientName', '').lower()
            value = nutrient.get('value', 0)
            
            if 'energy' in nutrient_name and 'kcal' in nutrient_name.lower():
                calories = value
                nutrients_found.append(f"Energy: {value}")
            elif 'protein' in nutrient_name and 'total lipid' not in nutrient_name:
                protein = value
                nutrients_found.append(f"Protein: {value}g")
            elif 'carbohydrate' in nutrient_name and 'by difference' in nutrient_name:
                carbs = value
                nutrients_found.append(f"Carbs: {value}g")
            elif ('total lipid' in nutrient_name or 'fat, total' in nutrient_name):
                fats = value
                nutrients_found.append(f"Fats: {value}g")
        
        print(f"   📊 Nutrients extracted (per 100g): {', '.join(nutrients_found) if nutrients_found else 'NONE FOUND!'}")
        
        return {
            "name": food_desc,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats,
            "serving_size": 100  # USDA returns per 100g
        }
        
    except Exception as e:
        print(f"   ⚠️ Error searching '{food_name}': {str(e)}")
        return None


def _calculate_multiplier(quantity: float, unit: str, base_serving: float = 100) -> float:
    """
    Calculate multiplier based on quantity and unit
    USDA returns per 100g, so we need to adjust
    """
    if unit == 'g' or unit == 'ml':
        return quantity / base_serving
    elif unit in ['piece', 'pieces']:
        # 1 egg ≈ 50g, 1 chicken breast ≈ 150g
        # For eggs: 5 pieces = 250g → multiplier = 2.5
        # Using 50g per piece as default (works well for eggs)
        grams = quantity * 50  # 1 piece = 50g
        return grams / base_serving
    elif unit == 'cup':
        return quantity * 2.4  # 1 cup ≈ 240ml ≈ 240g
    elif unit == 'tbsp':
        return quantity * 0.15  # 1 tbsp ≈ 15ml
    elif unit == 'tsp':
        return quantity * 0.05  # 1 tsp ≈ 5ml
    else:
        return quantity / base_serving


def check_fridge_inventory(
    products_list: List[Dict],
    expiry_dates: Optional[Dict] = None
) -> Dict:
    """
    Check fridge inventory and manage expiration dates
    
    Args:
        products_list: List of products with quantities
        expiry_dates: Optional dictionary of product: expiry_date pairs
    
    Returns:
        Dictionary with inventory status and expiring items
    """
    # TODO: Implement fridge inventory management
    # - Track products and quantities
    # - Identify expiring items
    # - Suggest meals to use expiring ingredients
    
    return {
        "inventory": products_list,
        "expiring_soon": [],
        "expired": []
    }


def suggest_meals_from_fridge(fridge_contents: List[str]) -> List[Dict]:
    """
    Suggest meals based on available ingredients
    
    Args:
        fridge_contents: List of available ingredients
    
    Returns:
        List of suggested meals with recipes
    """
    # TODO: Implement meal suggestions
    # - Match ingredients with recipes
    # - Calculate nutrition info
    # - Prioritize meals using expiring ingredients
    
    return []


# Tool definitions for OpenAI function calling
NUTRITION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_tdee",
            "description": "Calculate Total Daily Energy Expenditure based on user's physical characteristics and activity level",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight": {"type": "number", "description": "Weight in kilograms"},
                    "height": {"type": "number", "description": "Height in centimeters"},
                    "age": {"type": "integer", "description": "Age in years"},
                    "gender": {"type": "string", "enum": ["male", "female"]},
                    "activity_level": {
                        "type": "string",
                        "enum": ["sedentary", "light", "moderate", "active", "very_active"],
                        "description": "Activity level: sedentary (little/no exercise), light (1-3 days/week), moderate (3-5 days/week), active (6-7 days/week), very_active (physical job + exercise)"
                    }
                },
                "required": ["weight", "height", "age", "gender", "activity_level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_meal_plan",
            "description": "Generate a personalized meal plan based on calorie target and dietary preferences",
            "parameters": {
                "type": "object",
                "properties": {
                    "calories": {"type": "integer", "description": "Target daily calories"},
                    "diet_preference": {
                        "type": "string",
                        "enum": ["balanced", "keto", "vegan", "vegetarian", "paleo"],
                        "description": "Dietary preference"
                    },
                    "restrictions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of food restrictions (e.g., dairy, nuts, gluten)"
                    }
                },
                "required": ["calories"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "track_calories",
            "description": "Track calories and macros from a meal description",
            "parameters": {
                "type": "object",
                "properties": {
                    "meal_description": {
                        "type": "string",
                        "description": "Description of the meal or food items"
                    }
                },
                "required": ["meal_description"]
            }
        }
    }
]
