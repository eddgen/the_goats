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
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OpenAI API key not found!")
        print("\nPlease set up your API key:")
        print("1. Copy .env.example to .env")
        print("2. Get your API key from: https://platform.openai.com/api-keys")
        print("3. Add to .env file: OPENAI_API_KEY=sk-your-key-here")
        print("\nPress Enter to exit...")
        input()
        return
    
    # Initialize agent
    print("🏋️ FitCoach AI - Personal Fitness & Nutrition Assistant")
    print("Using OpenAI GPT-4o-mini (efficient & cost-effective model)")
    print("=" * 60)
    print("Welcome! I'm your AI fitness coach.")
    print("I can help you with:")
    print("  • Body analysis (BMI, body fat %, measurements, transformation)")
    print("  • Personalized meal plans and nutrition tracking")
    print("  • Custom workout plans and progress analysis")
    print("  • Running routes and gym locations")
    print("  • Integration with Hevy, Strava, and health apps")
    print("  • Export reports to PDF/Excel")
    print("=" * 60)
    print("\n💡 Cost-efficient model: ~$0.15 per 1M tokens")
    print("   Average conversation: ~$0.001-0.01")
    print("\nType 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'reset' to start a new conversation")
    print("Type 'save' to save the current conversation")
    print("-" * 60)
    
    try:
        agent = FitnessAgent()
    except ValueError as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nPress Enter to exit...")
        input()
        return
    
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
