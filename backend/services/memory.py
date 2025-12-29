from typing import Dict, List, Any
import json
from datetime import datetime

class MemoryService:
    """Service for managing user memory and conversation history"""
    
    def __init__(self):
        self.user_profiles = {}
        self.conversations = {}
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile from memory/database"""
        return self.user_profiles.get(user_id, {
            "skills": [],
            "experience_level": "entry",
            "target_roles": [],
            "career_goal": None
        })
    
    async def save_user_profile(self, user_id: str, profile: Dict[str, Any]):
        """Save user profile"""
        self.user_profiles[user_id] = profile
    
    async def get_conversation_history(
        self,
        user_id: str,
        session_id: str,
        limit: int = 10
    ) -> List[Any]:
        """Get conversation history"""
        key = f"{user_id}:{session_id}"
        return self.conversations.get(key, [])[-limit:]
    
    async def save_message(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        ai_response: str
    ):
        """Save conversation message"""
        key = f"{user_id}:{session_id}"
        if key not in self.conversations:
            self.conversations[key] = []
        
        self.conversations[key].append({
            "user": user_message,
            "assistant": ai_response,
            "timestamp": datetime.utcnow().isoformat()
        })
