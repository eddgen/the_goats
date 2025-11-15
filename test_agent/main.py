"""
FitCoach AI - Main Entry Point
Personal Fitness & Nutrition Assistant
"""
import os
from dotenv import load_dotenv
from agent import FitnessAgent


def main():
    """Main function to run the FitCoach AI agent"""
    
    # Load environment variables
    load_dotenv()
    
    # Check if Ollama is running
    print("🔍 Checking Ollama server...")
    print("Make sure Ollama is running with: ollama serve")
    print("And the model is pulled with: ollama pull llama3.1:8b")
    print()
    
    # Initialize agent
    print("🏋️ FitCoach AI - Personal Fitness & Nutrition Assistant")
    print("Using local Llama3.1:8b model via Ollama")
    print("=" * 60)
    print("Welcome! I'm your AI fitness coach.")
    print("I can help you with:")
    print("  • Personalized meal plans and nutrition tracking")
    print("  • Custom workout plans and progress analysis")
    print("  • Body composition analysis")
    print("  • Running routes and gym locations")
    print("  • Integration with Hevy, Strava, and health apps")
    print("  • Export reports to PDF/Excel")
    print("=" * 60)
    print("\nType 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'reset' to start a new conversation")
    print("Type 'save' to save the current conversation")
    print("-" * 60)
    
    agent = FitnessAgent()
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("\n You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Goodbye! Keep crushing your fitness goals!")
                break
            
            # Check for reset command
            if user_input.lower() == 'reset':
                agent.reset_conversation()
                print("\n🔄 Conversation reset. Let's start fresh!")
                continue
            
            # Check for save command
            if user_input.lower() == 'save':
                filename = f"data/users/conversation_{agent.user_profile.get('name', 'user')}.json"
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                agent.save_conversation(filename)
                print(f"\n💾 Conversation saved to {filename}")
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Get agent response
            print("\n🤖 FitCoach:", end=" ")
            response = agent.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Keep crushing your fitness goals!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit")


if __name__ == "__main__":
    main()
