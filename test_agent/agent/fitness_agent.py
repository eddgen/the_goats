"""
FitCoach AI - Personal Fitness & Nutrition Assistant
Main Agent Core
"""
import os
import json
from openai import OpenAI
from typing import Dict, List, Optional
from config.tools_config import get_all_tools, get_tool_function


class FitnessAgent:
    """
    Main Fitness Agent class that orchestrates all fitness and nutrition tools
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FitCoach AI agent
        
        Args:
            api_key: OpenAI API key (if not provided, will try to get from environment)
        """
        # Get API key from parameter or environment
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env file")
        
        # Use OpenAI API with GPT-4o-mini (cheap and efficient model)
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Cheapest GPT-4 model: ~$0.15/1M input tokens
        self.conversation_history = []
        self.user_profile = {}
        self.tools = self._initialize_tools()
        
    def _initialize_tools(self) -> List[Dict]:
        """
        Initialize and register all available tools for the agent
        
        Returns:
            List of tool definitions for OpenAI function calling
        """
        # Get all tool definitions from config
        return get_all_tools()
    
    def chat(self, user_message: str) -> str:
        """
        Main chat interface for the agent
        
        Args:
            user_message: User's input message
            
        Returns:
            Agent's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Create system message for the agent
        system_message = self._create_system_message()
        
        # Prepare messages for API call
        messages = [system_message] + self.conversation_history
        
        # Call OpenAI API with function calling
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools if self.tools else None,
            tool_choice="auto" if self.tools else None,
            temperature=0.7  # Balanced creativity
        )
        
        # Process response
        assistant_message = response.choices[0].message
        
        # Handle function calls if present
        if assistant_message.tool_calls:
            # Process tool calls
            tool_responses = self._process_tool_calls(assistant_message.tool_calls)
            
            # Add assistant message and tool responses to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls
            })
            
            for tool_response in tool_responses:
                self.conversation_history.append(tool_response)
            
            # Get final response after tool execution
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=[system_message] + self.conversation_history,
                temperature=0.7
            )
            
            final_message = final_response.choices[0].message.content
        else:
            final_message = assistant_message.content
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_message
        })
        
        return final_message
    
    def _create_system_message(self) -> Dict:
        """
        Create the system message that defines the agent's behavior
        
        Returns:
            System message dictionary
        """
        return {
            "role": "system",
            "content": """You are FitCoach AI, an expert personal fitness and nutrition assistant.

Your capabilities include:
- Analyzing body composition and calculating metrics (BMI, body fat estimation)
- Creating personalized meal plans based on TDEE and dietary preferences
- Generating customized workout plans for different goals and experience levels
- Tracking calories from meal descriptions or photos
- Suggesting running routes and finding nearby gyms using location data
- Integrating data from Hevy, Strava, and health apps
- Analyzing workout progress and suggesting improvements
- Managing fridge inventory and suggesting meals
- Exporting comprehensive reports (PDF/Excel)

Always be:
- Professional and encouraging
- Data-driven and precise with calculations
- Personalized based on user's profile and goals
- Supportive of sustainable fitness and nutrition habits

When gathering information:
- Ask for essential details (weight, height, age, gender, activity level, goals)
- Be conversational and don't overwhelm with too many questions at once
- Use emojis sparingly but appropriately to make interactions friendly

Current user profile: """ + json.dumps(self.user_profile, indent=2)
        }
    
    def _process_tool_calls(self, tool_calls) -> List[Dict]:
        """
        Execute tool calls and return their results
        
        Args:
            tool_calls: List of tool calls from OpenAI
            
        Returns:
            List of tool response messages
        """
        tool_responses = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Get the actual function to call
            function_to_call = get_tool_function(function_name)
            
            if function_to_call:
                try:
                    # Call the function with the provided arguments
                    result = function_to_call(**function_args)
                    
                    tool_responses.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })
                except Exception as e:
                    # Handle errors in tool execution
                    error_result = {
                        "status": "error",
                        "message": f"Error executing {function_name}: {str(e)}"
                    }
                    tool_responses.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(error_result)
                    })
            else:
                # Function not found
                error_result = {
                    "status": "error",
                    "message": f"Tool {function_name} not found"
                }
                tool_responses.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(error_result)
                })
        
        return tool_responses
    
    def update_user_profile(self, profile_data: Dict):
        """
        Update user profile information
        
        Args:
            profile_data: Dictionary containing user profile data
        """
        self.user_profile.update(profile_data)
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
    
    def save_conversation(self, filepath: str):
        """
        Save conversation history to file
        
        Args:
            filepath: Path to save the conversation
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'user_profile': self.user_profile,
                'conversation': self.conversation_history
            }, f, indent=2, ensure_ascii=False)
    
    def load_conversation(self, filepath: str):
        """
        Load conversation history from file
        
        Args:
            filepath: Path to load the conversation from
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.user_profile = data.get('user_profile', {})
            self.conversation_history = data.get('conversation', [])
