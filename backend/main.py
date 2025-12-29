# ============================================
# backend/main.py
# FastAPI Server with Multi-Agent System
# ============================================

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

from agents.orchestrator import CareerOrchestrator
from services.auth import get_current_user
from models.user import User, CareerProfile
from config import get_settings

app = FastAPI(title="Agentic Career AI", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()
orchestrator = CareerOrchestrator()

# ============================================
# MODELS
# ============================================

class ChatMessage(BaseModel):
    message: str
    session_id: str

class ProfileUpdate(BaseModel):
    skills: List[str]
    experience_level: str
    career_goal: str
    resume_url: Optional[str] = None

class JobQuery(BaseModel):
    keywords: Optional[str] = None
    location: Optional[str] = None
    limit: int = 10

# ============================================
# ROUTES
# ============================================

@app.get("/")
async def root():
    return {"message": "Agentic Career AI API", "status": "running"}

@app.post("/api/chat")
async def chat(
    message: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Main chat endpoint - handles all user interactions"""
    try:
        response = await orchestrator.process_message(
            user_id=current_user.id,
            message=message.message,
            session_id=message.session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/profile/analyze")
async def analyze_profile(
    profile: ProfileUpdate,
    current_user: User = Depends(get_current_user)
):
    """Analyze user profile and generate insights"""
    try:
        result = await orchestrator.analyze_profile(
            user_id=current_user.id,
            profile_data=profile.dict()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jobs/match")
async def get_job_matches(
    current_user: User = Depends(get_current_user)
):
    """Get personalized job matches"""
    try:
        jobs = await orchestrator.find_job_matches(
            user_id=current_user.id
        )
        return {"jobs": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/learning/roadmap")
async def get_learning_roadmap(
    current_user: User = Depends(get_current_user)
):
    """Get personalized learning roadmap"""
    try:
        roadmap = await orchestrator.generate_learning_roadmap(
            user_id=current_user.id
        )
        return roadmap
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview/practice")
async def start_interview_practice(
    role: str,
    current_user: User = Depends(get_current_user)
):
    """Start AI interview practice session"""
    try:
        session = await orchestrator.start_interview_practice(
            user_id=current_user.id,
            target_role=role
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
