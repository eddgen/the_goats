"""
Simple AI Agent Demo - Gemini Version
This agent can answer questions, perform calculations, and check the weather.
"""

import os
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class SimpleAIAgent:
    """A simple AI agent with tool-using capabilities using Google Gemini."""
    
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Initialize the model with tools
        self.model = genai.GenerativeModel(
            'models/gemini-2.0-flash',
            tools=[
                {
                    'function_declarations': [
                        {
                            'name': 'calculate',
                            'description': 'Perform basic mathematical calculations',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'expression': {
                                        'type': 'string',
                                        'description': 'The mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")'
                                    }
                                },
                                'required': ['expression']
                            }
                        },
                        {
                            'name': 'get_weather',
                            'description': 'Get the current weather for a location (simulated)',
                            'parameters': {
                                'type': 'object',
                                'properties': {
                                    'location': {
                                        'type': 'string',
                                        'description': 'The city name'
                                    }
                                },
                                'required': ['location']
                            }
                        }
                    ]
                }
            ]
        )
        
        self.chat = self.model.start_chat(enable_automatic_function_calling=False)
    
    def calculate(self, expression: str) -> str:
        """Safely evaluate a mathematical expression."""
        try:
            # Only allow basic math operations for safety
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"
    
    def get_weather(self, location: str) -> str:
        """Simulate getting weather data."""
        # This is a mock function - in a real agent, you'd call a weather API
        import random
        temps = [15, 18, 22, 25, 28, 30]
        conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
        
        temp = random.choice(temps)
        condition = random.choice(conditions)
        
        return f"Weather in {location}: {condition}, {temp}°C"
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool based on its name."""
        if tool_name == "calculate":
            return self.calculate(arguments["expression"])
        elif tool_name == "get_weather":
            return self.get_weather(arguments["location"])
        else:
            return f"Unknown tool: {tool_name}"
    
    def chat_with_agent(self, user_message: str) -> str:
        """
        Main agent loop: receives a message, thinks, uses tools if needed, and responds.
        """
        print(f"\n🤔 Agent is thinking...")
        
        # Send message to Gemini
        response = self.chat.send_message(user_message)
        
        # Check if the model wants to use function calls
        if response.candidates[0].content.parts:
            parts = response.candidates[0].content.parts
            
            # Check for function calls
            function_calls = [part for part in parts if hasattr(part, 'function_call') and part.function_call]
            
            if function_calls:
                print(f"🔧 Agent is using {len(function_calls)} tool(s)...")
                
                # Execute each function call
                function_responses = []
                for part in function_calls:
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    print(f"   → Calling {function_name} with args: {function_args}")
                    
                    # Execute the tool
                    tool_result = self.execute_tool(function_name, function_args)
                    
                    # Prepare function response
                    function_responses.append(
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_name,
                                response={'result': tool_result}
                            )
                        )
                    )
                
                # Send function responses back to get final answer
                final_response = self.chat.send_message(function_responses)
                assistant_message = final_response.text
            else:
                # No function calls, just get the text response
                assistant_message = response.text
        else:
            assistant_message = response.text
        
        return assistant_message


def main():
    """Run the AI agent in an interactive loop."""
    print("=" * 60)
    print("🤖 Simple AI Agent Demo (Gemini Version)")
    print("=" * 60)
    print("\nThis agent can:")
    print("  • Answer questions")
    print("  • Perform calculations")
    print("  • Check the weather (simulated)")
    print("\nType 'quit' or 'exit' to stop.\n")
    print("=" * 60)
    
    agent = SimpleAIAgent()
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = agent.chat_with_agent(user_input)
            print(f"\n🤖 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
