"""
Data Formatters for FitCoach AI
"""
from typing import Dict, Any


def format_tdee_result(data: Dict) -> str:
    """Format TDEE calculation results for display"""
    return f"""
📊 Your Metabolic Results:
  • BMR (Basal Metabolic Rate): {data.get('bmr', 0):.0f} calories/day
  • TDEE (Total Daily Energy Expenditure): {data.get('tdee', 0):.0f} calories/day
  
🎯 Calorie Targets:
  • Maintain weight: {data.get('maintenance_calories', 0):.0f} cal/day
  • Lose weight: {data.get('weight_loss_calories', 0):.0f} cal/day (-500 deficit)
  • Gain weight: {data.get('weight_gain_calories', 0):.0f} cal/day (+300 surplus)
"""


def format_meal_plan(data: Dict) -> str:
    """Format meal plan for display"""
    macros = data.get('macros', {})
    return f"""
🍽️ Your Meal Plan:
  • Target Calories: {data.get('target_calories', 0)} cal/day
  • Protein: {macros.get('protein', 0)}g
  • Carbs: {macros.get('carbs', 0)}g
  • Fats: {macros.get('fats', 0)}g
"""


def format_workout_plan(data: Dict) -> str:
    """Format workout plan for display"""
    return f"""
🏋️ Your Workout Plan:
  • Goal: {data.get('goal', 'Not specified').title()}
  • Experience Level: {data.get('experience', 'Not specified').title()}
  • Training Days: {data.get('days_per_week', 0)} days/week
"""
