"""
FitCoach AI - Gradio UI
Simple web interface for the fitness agent with image upload
"""
import os
import sys
import gradio as gr
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import agent
sys.path.append(str(Path(__file__).parent.parent))
from agent.fitness_agent import FitnessAgent

# Load environment variables
load_dotenv()

# Initialize agent globally
agent = None

def initialize_agent():
    """Initialize the fitness agent"""
    global agent
    try:
        agent = FitnessAgent()
        return "✅ Agent initialized successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def chat_with_agent(message, history, image_path=None):
    """
    Handle chat with optional image
    
    Args:
        message: User message
        history: Chat history
        image_path: Path to uploaded image (if any)
    """
    global agent
    
    if agent is None:
        return history + [("Agent not initialized", "❌ Please check your OpenAI API key in .env file")]
    
    # Build message with image reference if provided
    if image_path:
        # Save image to data folder
        image_name = os.path.basename(image_path)
        save_path = os.path.join("data", "uploads", image_name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Copy image
        import shutil
        shutil.copy(image_path, save_path)
        
        # Add image reference to message
        full_message = f"{message}\n\n[Image uploaded: {save_path}]"
    else:
        full_message = message
    
    try:
        # Get agent response
        response = agent.chat(full_message)
        
        # Add to history
        history.append((message, response))
        
        return history
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append((message, error_msg))
        return history

def reset_conversation():
    """Reset the conversation history"""
    global agent
    if agent:
        agent.reset_conversation()
    return []

def create_ui():
    """Create Gradio interface"""
    
    with gr.Blocks(title="FitCoach AI", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🏋️ FitCoach AI - Personal Fitness & Nutrition Assistant
            
            **Capabilities:**
            - 📊 Body Analysis (BMI, body fat %, measurements, transformations)
            - 🍽️ Nutrition Planning (TDEE, meal plans, calorie tracking)
            - 💪 Workout Planning (coming soon)
            - 📸 Image Analysis (upload photos for body fat estimation or transformation tracking)
            
            **Using:** OpenAI GPT-4o-mini (cost-efficient) + GPT-4o Vision (for images)
            """
        )
        
        with gr.Row():
            with gr.Column(scale=7):
                chatbot = gr.Chatbot(
                    label="Chat",
                    height=500,
                    show_label=True,
                    avatar_images=(None, "🏋️")
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        label="Your message",
                        placeholder="Type your message here... (e.g., 'I'm 75kg and 175cm, calculate my BMI')",
                        scale=9
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
            
            with gr.Column(scale=3):
                gr.Markdown("### 📸 Image Upload")
                image_input = gr.Image(
                    label="Upload Image",
                    type="filepath",
                    height=300
                )
                
                gr.Markdown(
                    """
                    **Upload images for:**
                    - Body fat analysis
                    - Before/after transformation
                    - Progress tracking
                    
                    Mention in your message what you want analyzed!
                    """
                )
                
                with gr.Row():
                    clear_btn = gr.Button("Clear Image", size="sm")
                    reset_btn = gr.Button("Reset Chat", size="sm", variant="stop")
        
        # Example prompts
        gr.Markdown("### 💡 Example Prompts:")
        with gr.Row():
            example1 = gr.Button("Calculate my BMI (75kg, 175cm)", size="sm")
            example2 = gr.Button("Generate meal plan (2000 cal, balanced)", size="sm")
            example3 = gr.Button("Track: 100g oats, 300ml milk, 5 eggs", size="sm")
        
        with gr.Row():
            example4 = gr.Button("Calculate TDEE (75kg, 175cm, 25yo, male, active)", size="sm")
            example5 = gr.Button("Analyze body fat from uploaded image", size="sm")
        
        # Status
        status = gr.Markdown("")
        
        # Initialize agent on load
        demo.load(initialize_agent, outputs=status)
        
        # Event handlers
        def submit_message(message, history, image):
            return chat_with_agent(message, history, image), ""
        
        msg.submit(
            submit_message,
            inputs=[msg, chatbot, image_input],
            outputs=[chatbot, msg]
        )
        
        submit_btn.click(
            submit_message,
            inputs=[msg, chatbot, image_input],
            outputs=[chatbot, msg]
        )
        
        clear_btn.click(lambda: None, outputs=image_input)
        reset_btn.click(reset_conversation, outputs=chatbot)
        
        # Example button handlers
        example1.click(lambda: "Calculate my BMI for 75kg and 175cm", outputs=msg)
        example2.click(lambda: "Generate a meal plan for 2000 calories with balanced diet", outputs=msg)
        example3.click(lambda: "Track calories for: 100g oats, 300ml milk, 5 eggs", outputs=msg)
        example4.click(lambda: "Calculate TDEE for 75kg, 175cm, 25 years old, male, active lifestyle", outputs=msg)
        example5.click(lambda: "Analyze body fat percentage from the uploaded image", outputs=msg)
    
    return demo

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("data/uploads", exist_ok=True)
    
    # Create and launch UI
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
