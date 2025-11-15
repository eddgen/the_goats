"""
FastAPI Backend for FitCoach AI
Connects React UI to the Python agent
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from agent.fitness_agent import FitnessAgent
from dotenv import load_dotenv

# Load environment
load_dotenv()

app = FastAPI(title="FitCoach AI API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    global agent
    try:
        agent = FitnessAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")

class ChatResponse(BaseModel):
    response: str
    success: bool

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    message: str = Form(...),
    images: List[UploadFile] = File(None)
):
    """
    Handle chat messages with optional multiple image uploads
    """
    global agent
    
    if agent is None:
        return ChatResponse(
            response="❌ Agent not initialized. Check OpenAI API key.",
            success=False
        )
    
    try:
        # Handle multiple images if provided
        image_paths = []
        if images:
            # Save images temporarily
            upload_dir = Path("data/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            for idx, image in enumerate(images):
                image_path = upload_dir / f"{idx}_{image.filename}"
                with image_path.open("wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                image_paths.append(str(image_path))
            
            # Add image references to message
            if len(image_paths) == 1:
                message = f"{message}\n\n[Image uploaded: {image_paths[0]}]"
            elif len(image_paths) == 2:
                message = f"{message}\n\n[2 images uploaded for transformation comparison: before={image_paths[0]}, after={image_paths[1]}]"
            else:
                images_str = ", ".join(image_paths)
                message = f"{message}\n\n[{len(image_paths)} images uploaded: {images_str}]"
        
        # Get agent response
        response = agent.chat(message)
        
        return ChatResponse(response=response, success=True)
        
    except Exception as e:
        return ChatResponse(
            response=f"❌ Error: {str(e)}",
            success=False
        )

@app.post("/api/reset")
async def reset_chat():
    """Reset conversation history"""
    global agent
    if agent:
        agent.reset_conversation()
        return {"success": True, "message": "Chat reset"}
    return {"success": False, "message": "Agent not initialized"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_initialized": agent is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
