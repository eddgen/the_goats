"""
Configuration for FitCoach AI Tools
Consolidates all tool definitions from different modules
"""
from tools.nutrition_tools import (
    NUTRITION_TOOLS,
    calculate_tdee,
    generate_meal_plan,
    track_calories
)
from tools.workout_tools import (
    WORKOUT_TOOLS,
    generate_workout_plan,
    analyze_workout_progress
)
from tools.body_analysis_tools import (
    BODY_ANALYSIS_TOOLS,
    calculate_bmi,
    estimate_body_fat
)
from tools.route_tools import (
    ROUTE_TOOLS,
    generate_running_routes,
    find_nearby_gyms
)
from tools.data_integration_tools import (
    DATA_INTEGRATION_TOOLS,
    import_strava_data,
    import_hevy_workout
)
from tools.export_tools import (
    EXPORT_TOOLS,
    export_meal_plan_pdf,
    export_workout_plan_pdf,
    export_progress_report_excel
)


# Combine all tools
ALL_TOOLS = (
    NUTRITION_TOOLS +
    WORKOUT_TOOLS +
    BODY_ANALYSIS_TOOLS +
    ROUTE_TOOLS +
    DATA_INTEGRATION_TOOLS +
    EXPORT_TOOLS
)


# Tool function mapping - maps function names to actual Python functions
TOOL_FUNCTIONS = {
    # Nutrition tools
    "calculate_tdee": calculate_tdee,
    "generate_meal_plan": generate_meal_plan,
    "track_calories": track_calories,
    
    # Workout tools
    "generate_workout_plan": generate_workout_plan,
    "analyze_workout_progress": analyze_workout_progress,
    
    # Body analysis tools
    "calculate_bmi": calculate_bmi,
    "estimate_body_fat": estimate_body_fat,
    
    # Route tools
    "generate_running_routes": generate_running_routes,
    "find_nearby_gyms": find_nearby_gyms,
    
    # Data integration tools
    "import_strava_data": import_strava_data,
    "import_hevy_workout": import_hevy_workout,
    
    # Export tools
    "export_meal_plan_pdf": export_meal_plan_pdf,
    "export_workout_plan_pdf": export_workout_plan_pdf,
    "export_progress_report_excel": export_progress_report_excel,
}


def get_all_tools():
    """Get all tool definitions"""
    return ALL_TOOLS


def get_tool_function(function_name: str):
    """Get the actual function implementation for a tool"""
    return TOOL_FUNCTIONS.get(function_name)
