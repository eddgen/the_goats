"""
Body Analysis Tools for FitCoach AI
Handles body composition analysis and measurements
"""
import os
import base64
from typing import Dict, Optional
from datetime import datetime
from openai import OpenAI
from pathlib import Path


def estimate_body_fat(image_path: str) -> Dict:
    """
    Estimate body fat percentage from image using OpenAI Vision API
    
    Args:
        image_path: Path to body image
    
    Returns:
        Dictionary with body fat estimation
    """
    print(f"\n🔍 [BODY_ANALYSIS] Analyzing body fat from image: {image_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"❌ [BODY_ANALYSIS] Image file not found: {image_path}")
            return {
                "success": False,
                "error": "Image file not found",
                "body_fat_percentage": None,
                "confidence": "low",
                "notes": f"File does not exist: {image_path}"
            }
        
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ [BODY_ANALYSIS] OpenAI API key not found in environment")
            return {
                "success": False,
                "error": "OpenAI API key not configured",
                "body_fat_percentage": None,
                "confidence": "low",
                "notes": "Please set OPENAI_API_KEY in .env file"
            }
        
        # Encode image to base64
        print("📸 [BODY_ANALYSIS] Encoding image to base64...")
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
        
        print("🤖 [BODY_ANALYSIS] Calling OpenAI Vision API for body composition analysis...")
        
        # Call OpenAI Vision API with detailed prompt
        response = client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4 Turbo with Vision
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this body composition photo and provide an estimate of body fat percentage. 
                            
Please provide:
1. Estimated body fat percentage (give a specific number or range)
2. Confidence level (high/medium/low) based on photo quality and visibility
3. Body composition category (athlete/fit/average/above average/high)
4. Visible muscle definition assessment
5. Any recommendations for more accurate assessment

Be professional, objective, and helpful. If the photo is unclear or doesn't show enough of the body, mention that in your assessment.

Format your response as JSON with these exact keys:
{
    "body_fat_percentage": <number or range like "12-15">,
    "confidence": "<high/medium/low>",
    "category": "<athlete/fit/average/above average/high>",
    "muscle_definition": "<description>",
    "recommendations": "<text>",
    "analysis_notes": "<additional observations>"
}

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
            max_tokens=500
        )
        
        # Parse response
        result_text = response.choices[0].message.content
        print(f"✅ [BODY_ANALYSIS] Received response from OpenAI Vision API")
        print(f"📊 [BODY_ANALYSIS] Analysis result:\n{result_text}")
        
        # Try to parse JSON from response
        import json
        try:
            # Extract JSON if it's wrapped in markdown code blocks
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            
            analysis = json.loads(result_text)
            
            return {
                "success": True,
                "body_fat_percentage": analysis.get("body_fat_percentage", "unknown"),
                "confidence": analysis.get("confidence", "medium"),
                "category": analysis.get("category", "unknown"),
                "muscle_definition": analysis.get("muscle_definition", ""),
                "recommendations": analysis.get("recommendations", ""),
                "analysis_notes": analysis.get("analysis_notes", ""),
                "timestamp": datetime.now().isoformat()
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw text
            print("⚠️ [BODY_ANALYSIS] Could not parse JSON, returning raw analysis")
            return {
                "success": True,
                "body_fat_percentage": "See analysis",
                "confidence": "medium",
                "raw_analysis": result_text,
                "notes": "Full text analysis provided",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        print(f"❌ [BODY_ANALYSIS] Error during body fat estimation: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "body_fat_percentage": None,
            "confidence": "low",
            "notes": f"Error occurred during analysis: {str(e)}"
        }


def calculate_bmi(weight: float, height: float) -> Dict:
    """
    Calculate Body Mass Index
    
    Args:
        weight: Weight in kg
        height: Height in cm
    
    Returns:
        Dictionary with BMI and classification
    """
    print(f"\n📊 [BODY_ANALYSIS] Calculating BMI for weight={weight}kg, height={height}cm")
    
    try:
        # Validate inputs
        if weight <= 0 or height <= 0:
            print("❌ [BODY_ANALYSIS] Invalid input: weight and height must be positive")
            return {
                "success": False,
                "error": "Invalid input values",
                "bmi": None,
                "classification": "Error"
            }
        
        # Convert height to meters and calculate BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        print(f"✅ [BODY_ANALYSIS] BMI calculated: {bmi:.1f}")
        
        # Classify BMI according to WHO standards
        if bmi < 16.0:
            classification = "Severe Thinness"
            health_risk = "High"
        elif 16.0 <= bmi < 17.0:
            classification = "Moderate Thinness"
            health_risk = "Moderate"
        elif 17.0 <= bmi < 18.5:
            classification = "Mild Thinness"
            health_risk = "Low"
        elif 18.5 <= bmi < 25.0:
            classification = "Normal weight"
            health_risk = "Minimal"
        elif 25.0 <= bmi < 30.0:
            classification = "Overweight"
            health_risk = "Moderate"
        elif 30.0 <= bmi < 35.0:
            classification = "Obese Class I"
            health_risk = "High"
        elif 35.0 <= bmi < 40.0:
            classification = "Obese Class II"
            health_risk = "Very High"
        else:
            classification = "Obese Class III"
            health_risk = "Extremely High"
        
        print(f"📋 [BODY_ANALYSIS] Classification: {classification} (Health Risk: {health_risk})")
        
        return {
            "success": True,
            "bmi": round(bmi, 1),
            "classification": classification,
            "health_risk": health_risk,
            "healthy_range": "18.5 - 24.9",
            "your_height_m": round(height_m, 2),
            "healthy_weight_range_kg": f"{round(18.5 * height_m**2, 1)} - {round(24.9 * height_m**2, 1)}",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ [BODY_ANALYSIS] Error calculating BMI: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "bmi": None,
            "classification": "Error"
        }


def track_measurements(measurements: Dict) -> Dict:
    """
    Track body measurements and store in database
    
    Args:
        measurements: Dictionary with body measurements (chest, waist, arms, hips, thighs, etc.)
    
    Returns:
        Dictionary with tracked measurements and analysis
    """
    print(f"\n📏 [BODY_ANALYSIS] Tracking body measurements: {list(measurements.keys())}")
    
    try:
        # Validate measurements
        valid_measurements = {}
        for key, value in measurements.items():
            if isinstance(value, (int, float)) and value > 0:
                valid_measurements[key] = round(value, 1)
                print(f"  ✓ {key}: {value} cm")
            else:
                print(f"  ⚠️ Skipping invalid measurement: {key}={value}")
        
        if not valid_measurements:
            print("❌ [BODY_ANALYSIS] No valid measurements provided")
            return {
                "success": False,
                "error": "No valid measurements provided",
                "measurements": {}
            }
        
        # Calculate some derived metrics
        analysis = {}
        
        # Waist-to-Hip Ratio (WHR) - health indicator
        if "waist" in valid_measurements and "hips" in valid_measurements:
            whr = valid_measurements["waist"] / valid_measurements["hips"]
            analysis["waist_hip_ratio"] = round(whr, 2)
            
            # Health assessment based on WHR (general guidelines)
            if whr < 0.85:
                whr_assessment = "Low health risk"
            elif 0.85 <= whr < 0.90:
                whr_assessment = "Moderate health risk"
            else:
                whr_assessment = "High health risk"
            analysis["whr_assessment"] = whr_assessment
            print(f"📊 [BODY_ANALYSIS] Waist-to-Hip Ratio: {whr:.2f} ({whr_assessment})")
        
        # Body symmetry check (comparing left vs right measurements if available)
        symmetry = {}
        if "left_arm" in valid_measurements and "right_arm" in valid_measurements:
            arm_diff = abs(valid_measurements["left_arm"] - valid_measurements["right_arm"])
            symmetry["arms"] = f"{arm_diff:.1f} cm difference"
            print(f"📏 [BODY_ANALYSIS] Arm symmetry: {arm_diff:.1f} cm difference")
        
        if "left_thigh" in valid_measurements and "right_thigh" in valid_measurements:
            thigh_diff = abs(valid_measurements["left_thigh"] - valid_measurements["right_thigh"])
            symmetry["thighs"] = f"{thigh_diff:.1f} cm difference"
            print(f"📏 [BODY_ANALYSIS] Thigh symmetry: {thigh_diff:.1f} cm difference")
        
        # Store timestamp
        timestamp = datetime.now().isoformat()
        
        print(f"✅ [BODY_ANALYSIS] Successfully tracked {len(valid_measurements)} measurements")
        
        return {
            "success": True,
            "measurements": valid_measurements,
            "analysis": analysis,
            "symmetry": symmetry if symmetry else None,
            "timestamp": timestamp,
            "total_measurements": len(valid_measurements),
            "notes": "Measurements successfully recorded. Track regularly to monitor progress."
        }
        
    except Exception as e:
        print(f"❌ [BODY_ANALYSIS] Error tracking measurements: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "measurements": {}
        }


def visualize_transformation(before_photo: str, after_photo: str) -> Dict:
    """
    Create transformation visualization and analysis using AI vision
    
    Args:
        before_photo: Path to before photo
        after_photo: Path to after photo
    
    Returns:
        Dictionary with transformation analysis
    """
    print(f"\n🔄 [BODY_ANALYSIS] Analyzing transformation between photos")
    print(f"   Before: {before_photo}")
    print(f"   After: {after_photo}")
    
    try:
        # Check if both files exist
        if not os.path.exists(before_photo):
            print(f"❌ [BODY_ANALYSIS] Before photo not found: {before_photo}")
            return {
                "success": False,
                "error": "Before photo not found",
                "comparison_created": False
            }
        
        if not os.path.exists(after_photo):
            print(f"❌ [BODY_ANALYSIS] After photo not found: {after_photo}")
            return {
                "success": False,
                "error": "After photo not found",
                "comparison_created": False
            }
        
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ [BODY_ANALYSIS] OpenAI API key not found")
            return {
                "success": False,
                "error": "OpenAI API key not configured",
                "comparison_created": False
            }
        
        # Encode both images
        print("📸 [BODY_ANALYSIS] Encoding images...")
        with open(before_photo, "rb") as f:
            before_data = base64.b64encode(f.read()).decode('utf-8')
        with open(after_photo, "rb") as f:
            after_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Determine mime types
        before_mime = 'image/jpeg' if before_photo.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
        after_mime = 'image/jpeg' if after_photo.lower().endswith(('.jpg', '.jpeg')) else 'image/png'
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        print("🤖 [BODY_ANALYSIS] Calling OpenAI Vision API for transformation analysis...")
        
        # Call Vision API with both images
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Compare these two body transformation photos (BEFORE and AFTER) and provide a detailed analysis.

Analyze and provide:
1. Visible muscle development or fat loss
2. Postural improvements
3. Overall body composition changes
4. Specific areas showing most improvement
5. Estimated timeframe for such transformation (if assessable)
6. Motivational feedback and recommendations

Be encouraging, specific, and professional.

Format as JSON:
{
    "muscle_gain": "<description>",
    "fat_loss": "<description>",
    "postural_changes": "<description>",
    "key_improvements": ["<area1>", "<area2>", ...],
    "estimated_timeframe": "<estimate>",
    "overall_assessment": "<detailed assessment>",
    "motivation": "<encouraging message>",
    "recommendations": "<next steps>"
}

REMEMBER: Output must be pure JSON only, no markdown, no code blocks, no formatting."""
                        },
                        {
                            "type": "text",
                            "text": "BEFORE photo:"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{before_mime};base64,{before_data}"}
                        },
                        {
                            "type": "text",
                            "text": "AFTER photo:"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{after_mime};base64,{after_data}"}
                        }
                    ]
                }
            ],
            max_tokens=700
        )
        
        # Parse response
        result_text = response.choices[0].message.content
        print(f"✅ [BODY_ANALYSIS] Transformation analysis complete")
        print(f"📊 [BODY_ANALYSIS] Analysis:\n{result_text}")
        
        # Try to parse JSON
        import json
        try:
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            
            analysis = json.loads(result_text)
            
            return {
                "success": True,
                "comparison_created": True,
                "muscle_gain": analysis.get("muscle_gain", ""),
                "fat_loss": analysis.get("fat_loss", ""),
                "postural_changes": analysis.get("postural_changes", ""),
                "key_improvements": analysis.get("key_improvements", []),
                "estimated_timeframe": analysis.get("estimated_timeframe", "unknown"),
                "overall_assessment": analysis.get("overall_assessment", ""),
                "motivation": analysis.get("motivation", ""),
                "recommendations": analysis.get("recommendations", ""),
                "timestamp": datetime.now().isoformat()
            }
        except json.JSONDecodeError:
            print("⚠️ [BODY_ANALYSIS] Could not parse JSON, returning raw analysis")
            return {
                "success": True,
                "comparison_created": True,
                "raw_analysis": result_text,
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        print(f"❌ [BODY_ANALYSIS] Error during transformation analysis: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "comparison_created": False
        }


# Tool definitions for OpenAI function calling
BODY_ANALYSIS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_bmi",
            "description": "Calculate Body Mass Index and provide detailed health classification with risk assessment",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight": {
                        "type": "number", 
                        "description": "Weight in kilograms (kg)"
                    },
                    "height": {
                        "type": "number", 
                        "description": "Height in centimeters (cm)"
                    }
                },
                "required": ["weight", "height"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "estimate_body_fat",
            "description": "Estimate body fat percentage from a body photo using AI vision analysis. Provides detailed body composition assessment including muscle definition and recommendations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Absolute path to the body image file (jpg, png, etc.)"
                    }
                },
                "required": ["image_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "track_measurements",
            "description": "Track and analyze body measurements (chest, waist, arms, hips, thighs). Calculates waist-to-hip ratio and symmetry analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "measurements": {
                        "type": "object",
                        "description": "Dictionary of body measurements in centimeters. Keys can include: chest, waist, hips, left_arm, right_arm, left_thigh, right_thigh, neck, shoulders, etc.",
                        "properties": {
                            "chest": {"type": "number"},
                            "waist": {"type": "number"},
                            "hips": {"type": "number"},
                            "left_arm": {"type": "number"},
                            "right_arm": {"type": "number"},
                            "left_thigh": {"type": "number"},
                            "right_thigh": {"type": "number"},
                            "neck": {"type": "number"},
                            "shoulders": {"type": "number"}
                        }
                    }
                },
                "required": ["measurements"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "visualize_transformation",
            "description": "Analyze body transformation by comparing before and after photos using AI vision. Provides detailed assessment of muscle gain, fat loss, and improvements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "before_photo": {
                        "type": "string",
                        "description": "Absolute path to the 'before' transformation photo"
                    },
                    "after_photo": {
                        "type": "string",
                        "description": "Absolute path to the 'after' transformation photo"
                    }
                },
                "required": ["before_photo", "after_photo"]
            }
        }
    }
]
