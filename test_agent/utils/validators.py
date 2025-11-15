"""
Input Validators for FitCoach AI
"""


def validate_weight(weight: float) -> bool:
    """Validate weight is in reasonable range (30-300 kg)"""
    return 30 <= weight <= 300


def validate_height(height: float) -> bool:
    """Validate height is in reasonable range (100-250 cm)"""
    return 100 <= height <= 250


def validate_age(age: int) -> bool:
    """Validate age is in reasonable range (13-100 years)"""
    return 13 <= age <= 100


def validate_gender(gender: str) -> bool:
    """Validate gender value"""
    return gender.lower() in ['male', 'female', 'm', 'f']


def validate_activity_level(level: str) -> bool:
    """Validate activity level"""
    valid_levels = ['sedentary', 'light', 'moderate', 'active', 'very_active']
    return level.lower() in valid_levels
