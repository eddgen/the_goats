"""
Simple AI Agent Demo
This agent can answer questions, perform calculations, and check the weather.
"""

import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class SimpleAIAgent:
    """A simple AI agent with tool-using capabilities."""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
        self.conversation_history: List[Dict[str, str]] = []
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Perform basic mathematical calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "The mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather for a location (simulated)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]
    
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
    
    def chat(self, user_message: str) -> str:
        """
        Main agent loop: receives a message, thinks, uses tools if needed, and responds.
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        print(f"\n🤔 Agent is thinking...")
        
        # Get response from LLM
        response = self.client.chat.completions.create(
            model="llama3.2:3b",
            messages=self.conversation_history,
            tools=self.tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        # If the agent wants to use tools
        if tool_calls:
            print(f"🔧 Agent is using {len(tool_calls)} tool(s)...")
            
            # Add assistant's response to history
            self.conversation_history.append(response_message)
            
            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"   → Calling {function_name} with args: {function_args}")
                
                # Execute the tool
                tool_result = self.execute_tool(function_name, function_args)
                
                # Add tool result to conversation
                self.conversation_history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_result
                })
            
            # Get final response after tool execution
            final_response = self.client.chat.completions.create(
                model="llama3.2:3b",
                messages=self.conversation_history
            )
            
            assistant_message = final_response.choices[0].message.content
        else:
            # No tools needed, direct response
            assistant_message = response_message.content
        
        # Add assistant's final response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message


def main():
    """Run the AI agent in an interactive loop."""
    print("=" * 60)
    print("🤖 Simple AI Agent Demo")
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
            
            if user_input.lower() in ['quit', 'exit', 'bye' , ' pa']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = agent.chat(user_input)
            print(f"\n🤖 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
