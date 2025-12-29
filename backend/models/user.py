from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: EmailStr
    created_at: Optional[datetime] = None

class CareerProfile(BaseModel):
    user_id: str
    skills: List[str] = []
    experience_level: str = "entry"
    career_goal: Optional[str] = None
    target_roles: List[str] = []
    resume_url: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123",
                "skills": ["Python", "FastAPI", "React"],
                "experience_level": "mid",
                "career_goal": "Senior Software Engineer",
                "target_roles": ["Backend Developer", "Full Stack Engineer"]
            }
        }
