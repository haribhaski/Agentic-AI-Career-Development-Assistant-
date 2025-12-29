from typing import Dict, List, Any
from datetime import datetime
from services.supabase_client import supabase_client
import json

class MemoryService:
    """Service for managing user memory and conversation history using Supabase + pgvector"""
    
    def __init__(self):
        self.client = supabase_client
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile from Supabase"""
        if not self.client:
            return self._default_profile()
            
        try:
            result = self.client.table("profiles").select("*").eq("user_id", user_id).single().execute()
            return result.data if result.data else self._default_profile()
        except:
            return self._default_profile()
    
    async def save_user_profile(self, user_id: str, profile: Dict[str, Any]):
        """Save user profile to Supabase"""
        if not self.client:
            return
            
        profile["user_id"] = user_id
        profile["updated_at"] = datetime.utcnow().isoformat()
        
        try:
            self.client.table("profiles").upsert(profile).execute()
        except Exception as e:
            print(f"Error saving profile: {e}")
    
    async def get_conversation_history(
        self,
        user_id: str,
        session_id: str,
        limit: int = 10
    ) -> List[Any]:
        """Get conversation history from Supabase"""
        if not self.client:
            return []
            
        try:
            result = self.client.table("conversations") \
                .select("*") \
                .eq("user_id", user_id) \
                .eq("session_id", session_id) \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            
            # Format for LangChain
            from langchain_core.messages import HumanMessage, AIMessage
            history = []
            for msg in reversed(result.data):
                history.append(HumanMessage(content=msg["user_message"]))
                history.append(AIMessage(content=msg["ai_response"]))
            return history
        except:
            return []
    
    async def save_message(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        ai_response: str
    ):
        """Save conversation message to Supabase"""
        if not self.client:
            return
            
        data = {
            "user_id": user_id,
            "session_id": session_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "created_at": datetime.utcnow().isoformat()
        }
        
        try:
            self.client.table("conversations").insert(data).execute()
        except Exception as e:
            print(f"Error saving message: {e}")

    def _default_profile(self) -> Dict[str, Any]:
        return {
            "skills": [],
            "experience_level": "entry",
            "target_roles": [],
            "career_goal": None
        }
