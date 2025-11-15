"""
Fridge Analysis Tools for FitCoach AI
Analyzes fridge contents from photos and suggests meals
"""
import os
import base64
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from pathlib import Path
import json


def analyze_fridge(image_path: str, remaining_calories: Optional[int] = None) -> Dict:
    """
    Analyze fridge contents from photo using OpenAI Vision API
    
    Args:
        image_path: Path to fridge photo
        remaining_calories: Optional - how many calories user has left for the day
    
    Returns:
        Dictionary with identified foods, quantities, and nutritional estimates
    """
    print(f"\n🔍 [FRIDGE_ANALYSIS] Analyzing fridge contents from: {image_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"❌ [FRIDGE_ANALYSIS] Image file not found: {image_path}")
            return {
                "success": False,
                "error": "Image file not found",
                "foods": [],
                "notes": f"File does not exist: {image_path}"
            }
        
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ [FRIDGE_ANALYSIS] OpenAI API key not found in environment")
            return {
                "success": False,
                "error": "OpenAI API key not configured",
                "foods": [],
                "notes": "Please set OPENAI_API_KEY in .env file"
            }
        
        # Encode image to base64
        print("📸 [FRIDGE_ANALYSIS] Encoding fridge photo...")
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Determine image format
        file_extension = Path(image_path).suffix.lower()
        mime_type = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }.get(file_extension, 'image/jpeg')
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        print("🤖 [FRIDGE_ANALYSIS] Calling OpenAI Vision API for food identification...")
        
        # Build prompt based on whether calories were provided
        calorie_context = ""
        if remaining_calories:
            calorie_context = f"\n\nIMPORTANT: The user has {remaining_calories} calories remaining for today. Keep this in mind for meal suggestions."
        
        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Analyze this refrigerator photo and identify all visible food items.

CRITICAL INSTRUCTIONS:
- Return ONLY raw JSON, no markdown formatting
- Do NOT use ``` code blocks
- Do NOT use ** bold ** or ### headers
- Do NOT add any text before or after the JSON
- Output must be pure, valid JSON only

For each food item, provide:
1. Food name
2. Estimated quantity (e.g., "3 eggs", "500ml milk", "1 pack chicken breast")
3. Estimated calories per serving (numeric value only)
4. Food category (protein/carbs/fats/vegetables/dairy/fruits/other)
5. Freshness estimate (fresh/consume_soon/check_expiry)

Also provide:
- Overall inventory assessment
- Any missing staples{calorie_context}

Return your response as pure JSON with this EXACT structure:
{{
    "foods": [
        {{
            "name": "Eggs",
            "quantity": "6 eggs",
            "calories_per_serving": 70,
            "category": "protein",
            "freshness": "fresh"
        }}
    ],
    "inventory_summary": {{
        "total_items": 0,
        "proteins": 0,
        "carbs": 0,
        "vegetables": 0,
        "dairy": 0
    }},
    "meal_potential": [],
    "missing_staples": [],
    "notes": ""
}}

REMEMBER: Output must be pure JSON only, no markdown, no code blocks, no formatting."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000,  # Increased even more to ensure complete JSON
            temperature=0.3  # Lower temperature for more consistent output
        )
        
        # Parse response
        result_text = response.choices[0].message.content
        print(f"✅ [FRIDGE_ANALYSIS] Received response from OpenAI Vision API")
        print(f"📄 [FRIDGE_ANALYSIS] Full response length: {len(result_text)} characters")
        
        # Try to parse JSON from response
        try:
            # Extract JSON if it's wrapped in markdown code blocks
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                if json_end == -1:  # No closing backticks, try to find end of JSON
                    json_end = len(result_text)
                result_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                if json_end == -1:
                    json_end = len(result_text)
                result_text = result_text[json_start:json_end].strip()
            
            # Remove any trailing incomplete data
            # Find the last complete closing brace
            last_brace = result_text.rfind('}')
            if last_brace != -1:
                result_text = result_text[:last_brace + 1]
            
            print(f"🔍 [FRIDGE_ANALYSIS] Attempting to parse JSON ({len(result_text)} chars)")
            analysis = json.loads(result_text)
            
            # Print summary
            print(f"📊 [FRIDGE_ANALYSIS] Found {len(analysis.get('foods', []))} food items")
            for food in analysis.get('foods', [])[:5]:  # Print first 5
                print(f"  ✓ {food.get('name')}: {food.get('quantity')} ({food.get('category')})")
            
            return {
                "success": True,
                "foods": analysis.get("foods", []),
                "inventory_summary": analysis.get("inventory_summary", {}),
                "meal_potential": analysis.get("meal_potential", []),
                "missing_staples": analysis.get("missing_staples", []),
                "notes": analysis.get("notes", ""),
                "remaining_calories": remaining_calories,
                "timestamp": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            print(f"⚠️ [FRIDGE_ANALYSIS] Could not parse JSON: {e}")
            print(f"📄 Raw response preview: {result_text[:300]}...")
            print(f"📄 Last 100 chars: ...{result_text[-100:]}")
            
            # Try to salvage partial data by fixing common issues
            try:
                # Strategy 1: Try to complete incomplete JSON by adding closing braces
                # Count opening vs closing braces
                open_braces = result_text.count('{')
                close_braces = result_text.count('}')
                open_brackets = result_text.count('[')
                close_brackets = result_text.count(']')
                
                fixed_text = result_text
                # Add missing closing brackets
                if open_brackets > close_brackets:
                    fixed_text += ']' * (open_brackets - close_brackets)
                # Add missing closing braces
                if open_braces > close_braces:
                    fixed_text += '}' * (open_braces - close_braces)
                
                print(f"🔧 [FRIDGE_ANALYSIS] Attempting to fix JSON with {open_braces - close_braces} missing braces")
                analysis = json.loads(fixed_text)
                print(f"✅ [FRIDGE_ANALYSIS] Successfully parsed fixed JSON with {len(analysis.get('foods', []))} foods")
                
                return {
                    "success": True,
                    "foods": analysis.get("foods", []),
                    "inventory_summary": analysis.get("inventory_summary", {}),
                    "meal_potential": analysis.get("meal_potential", []),
                    "missing_staples": analysis.get("missing_staples", []),
                    "notes": analysis.get("notes", ""),
                    "remaining_calories": remaining_calories,
                    "timestamp": datetime.now().isoformat()
                }
            except:
                # Strategy 2: Extract just the foods array if main JSON fails
                try:
                    if '"foods"' in result_text:
                        foods_start = result_text.find('"foods"')
                        # Find the opening bracket
                        bracket_start = result_text.find('[', foods_start)
                        if bracket_start != -1:
                            # Find matching closing bracket
                            bracket_count = 0
                            for i in range(bracket_start, len(result_text)):
                                if result_text[i] == '[':
                                    bracket_count += 1
                                elif result_text[i] == ']':
                                    bracket_count -= 1
                                    if bracket_count == 0:
                                        foods_json = result_text[bracket_start:i+1]
                                        foods = json.loads(foods_json)
                                        print(f"✅ [FRIDGE_ANALYSIS] Recovered {len(foods)} foods from partial JSON")
                                        return {
                                            "success": True,
                                            "foods": foods,
                                            "inventory_summary": {},
                                            "meal_potential": [],
                                            "missing_staples": [],
                                            "notes": "Partial data recovered from incomplete response",
                                            "remaining_calories": remaining_calories,
                                            "timestamp": datetime.now().isoformat()
                                        }
                except Exception as inner_e:
                    print(f"⚠️ [FRIDGE_ANALYSIS] Recovery also failed: {inner_e}")
            
            return {
                "success": False,
                "raw_analysis": result_text,
                "foods": [],
                "notes": f"JSON parsing failed: {str(e)}. Please try again or use a clearer photo.",
                "remaining_calories": remaining_calories,
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        print(f"❌ [FRIDGE_ANALYSIS] Error analyzing fridge: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "foods": [],
            "notes": f"Analysis failed: {str(e)}"
        }


def suggest_meal_from_fridge(
    fridge_contents: Dict,
    remaining_calories: int,
    dietary_restrictions: Optional[List[str]] = None,
    meal_type: Optional[str] = None
) -> Dict:
    """
    Suggest meal based on fridge contents and calorie budget
    
    Args:
        fridge_contents: Dictionary from analyze_fridge() with food inventory
        remaining_calories: How many calories user has left
        dietary_restrictions: Optional list (e.g., ["no dairy", "vegetarian"])
        meal_type: Optional - "breakfast", "lunch", "dinner", or "snack"
    
    Returns:
        Dictionary with meal suggestion, recipe, and macros
    """
    print(f"\n🍳 [MEAL_SUGGESTION] Generating meal for {remaining_calories} calories")
    
    try:
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "OpenAI API key not configured"
            }
        
        # Extract food list from fridge contents
        foods = fridge_contents.get("foods", [])
        if not foods:
            print("⚠️ [MEAL_SUGGESTION] No foods found in fridge contents")
            return {
                "success": False,
                "error": "No foods available in fridge",
                "suggestion": "Please analyze your fridge first or go shopping!"
            }
        
        # Build food inventory string
        food_list = "\n".join([
            f"- {food.get('name')}: {food.get('quantity')} ({food.get('category')})"
            for food in foods
        ])
        
        # Build constraints
        constraints = []
        if remaining_calories:
            constraints.append(f"Maximum {remaining_calories} calories")
        if dietary_restrictions:
            constraints.append(f"Dietary restrictions: {', '.join(dietary_restrictions)}")
        if meal_type:
            constraints.append(f"Meal type: {meal_type}")
        
        constraints_text = "\n".join(constraints) if constraints else "No specific constraints"
        
        print(f"🤖 [MEAL_SUGGESTION] Calling OpenAI for meal suggestion...")
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Call OpenAI for meal suggestion
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cheaper model for text generation
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative nutrition chef who creates delicious, healthy meals from available ingredients while respecting calorie budgets and dietary restrictions."
                },
                {
                    "role": "user",
                    "content": f"""Create a meal suggestion using ONLY these available ingredients:

{food_list}

Constraints:
{constraints_text}

Provide:
1. Meal name
2. Ingredients with exact quantities to use
3. Step-by-step cooking instructions
4. Total calories
5. Macros breakdown (protein, carbs, fats in grams)
6. Estimated prep time

Format as JSON:
{{
    "meal_name": "<creative name>",
    "ingredients": [
        {{"item": "<name>", "amount": "<quantity>", "calories": <number>}}
    ],
    "instructions": ["<step 1>", "<step 2>", ...],
    "total_calories": <number>,
    "macros": {{
        "protein_g": <number>,
        "carbs_g": <number>,
        "fats_g": <number>
    }},
    "prep_time_minutes": <number>,
    "tips": "<cooking tips>"
}}

REMEMBER: Output must be pure JSON only, no markdown, no code blocks, no formatting."""
                }
            ],
            temperature=0.8,  # More creative
            max_tokens=800
        )
        
        result_text = response.choices[0].message.content
        print("✅ [MEAL_SUGGESTION] Received meal suggestion")
        
        # Parse JSON
        try:
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            
            meal = json.loads(result_text)
            
            print(f"🍽️ [MEAL_SUGGESTION] Suggested: {meal.get('meal_name')}")
            print(f"   Calories: {meal.get('total_calories')} / {remaining_calories}")
            print(f"   Macros: P:{meal.get('macros', {}).get('protein_g')}g C:{meal.get('macros', {}).get('carbs_g')}g F:{meal.get('macros', {}).get('fats_g')}g")
            
            return {
                "success": True,
                "meal": meal,
                "calories_remaining_after": remaining_calories - meal.get('total_calories', 0),
                "fits_budget": meal.get('total_calories', 0) <= remaining_calories,
                "timestamp": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError:
            return {
                "success": True,
                "raw_suggestion": result_text,
                "notes": "Meal suggestion provided (JSON parsing failed)"
            }
        
    except Exception as e:
        print(f"❌ [MEAL_SUGGESTION] Error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


# Tool definitions for OpenAI function calling
FRIDGE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "analyze_fridge",
            "description": "Analyze refrigerator contents from a photo. Identifies all visible food items, estimates quantities, calories, and freshness. Perfect for meal planning based on available ingredients.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Absolute path to the refrigerator photo"
                    },
                    "remaining_calories": {
                        "type": "integer",
                        "description": "Optional - how many calories the user has left for the day. Helps with meal suggestions."
                    }
                },
                "required": ["image_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_meal_from_fridge",
            "description": "Suggest a meal recipe based on available fridge contents and remaining calorie budget. Creates practical recipes using only available ingredients.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fridge_contents": {
                        "type": "object",
                        "description": "The result from analyze_fridge() containing food inventory"
                    },
                    "remaining_calories": {
                        "type": "integer",
                        "description": "How many calories the user has left for this meal/day"
                    },
                    "dietary_restrictions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of dietary restrictions (e.g., ['no dairy', 'vegetarian', 'gluten-free'])"
                    },
                    "meal_type": {
                        "type": "string",
                        "enum": ["breakfast", "lunch", "dinner", "snack"],
                        "description": "Optional - type of meal to suggest"
                    }
                },
                "required": ["fridge_contents", "remaining_calories"]
            }
        }
    }
]
