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


# ============================================
# backend/agents/orchestrator.py
# Main Orchestrator - Routes to specialized agents
# ============================================

from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agents.profile_agent import ProfileAgent
from agents.market_agent import MarketIntelligenceAgent
from agents.learning_agent import LearningPathAgent
from agents.application_agent import ApplicationAgent
from agents.interview_agent import InterviewAgent
from agents.feedback_agent import FeedbackAgent
from services.memory import MemoryService
from services.supabase_client import supabase_client
from config import get_settings

settings = get_settings()

class AgentState(dict):
    """State shared across all agents"""
    user_id: str
    messages: List[Any]
    user_profile: Dict
    current_skills: List[str]
    skill_gaps: List[str]
    target_roles: List[str]
    job_matches: List[Dict]
    learning_plan: Dict
    next_agent: str
    final_response: str

class CareerOrchestrator:
    """Main orchestrator that coordinates all specialized agents"""
    
    def __init__(self):
        # Initialize LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            groq_api_key=settings.groq_api_key
        )
        
        # Initialize specialized agents
        self.profile_agent = ProfileAgent(self.llm)
        self.market_agent = MarketIntelligenceAgent(self.llm)
        self.learning_agent = LearningPathAgent(self.llm)
        self.application_agent = ApplicationAgent(self.llm)
        self.interview_agent = InterviewAgent(self.llm)
        self.feedback_agent = FeedbackAgent(self.llm)
        
        # Memory service for long-term storage
        self.memory = MemoryService()
        
        # Build LangGraph workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the agent workflow graph"""
        workflow = StateGraph(AgentState)
        
        # Add nodes (agents)
        workflow.add_node("router", self._route_request)
        workflow.add_node("profile", self.profile_agent.process)
        workflow.add_node("market", self.market_agent.process)
        workflow.add_node("learning", self.learning_agent.process)
        workflow.add_node("application", self.application_agent.process)
        workflow.add_node("interview", self.interview_agent.process)
        workflow.add_node("feedback", self.feedback_agent.process)
        
        # Set entry point
        workflow.set_entry_point("router")
        
        # Add conditional edges based on routing
        workflow.add_conditional_edges(
            "router",
            self._determine_next_agent,
            {
                "profile": "profile",
                "market": "market",
                "learning": "learning",
                "application": "application",
                "interview": "interview",
                "feedback": "feedback",
                "end": END
            }
        )
        
        # All agents can route back to router or end
        for agent in ["profile", "market", "learning", "application", "interview", "feedback"]:
            workflow.add_conditional_edges(
                agent,
                self._determine_next_agent,
                {
                    "profile": "profile",
                    "market": "market",
                    "learning": "learning",
                    "application": "application",
                    "interview": "interview",
                    "feedback": "feedback",
                    "router": "router",
                    "end": END
                }
            )
        
        # Compile with memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    async def _route_request(self, state: AgentState) -> AgentState:
        """Intelligent routing based on user message"""
        last_message = state["messages"][-1] if state["messages"] else ""
        
        routing_prompt = f"""Based on this user message, determine which agent should handle it:
        
        Message: {last_message}
        
        Available agents:
        - profile: Resume analysis, skill extraction, profile updates
        - market: Job search, market trends, salary research
        - learning: Skill gaps, learning paths, course recommendations
        - application: Resume tailoring, cover letters, application tracking
        - interview: Mock interviews, interview prep, feedback
        - feedback: Application outcomes, rejection analysis, strategy updates
        
        Respond with ONLY the agent name (no explanation)."""
        
        response = await self.llm.ainvoke([HumanMessage(content=routing_prompt)])
        state["next_agent"] = response.content.strip().lower()
        
        return state
    
    def _determine_next_agent(self, state: AgentState) -> str:
        """Determine next agent or end"""
        return state.get("next_agent", "end")
    
    async def process_message(
        self,
        user_id: str,
        message: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Process user message through agent system"""
        
        # Load user profile and history
        user_profile = await self.memory.get_user_profile(user_id)
        conversation_history = await self.memory.get_conversation_history(user_id, session_id)
        
        # Initialize state
        state = AgentState(
            user_id=user_id,
            messages=conversation_history + [HumanMessage(content=message)],
            user_profile=user_profile,
            current_skills=user_profile.get("skills", []),
            skill_gaps=[],
            target_roles=user_profile.get("target_roles", []),
            job_matches=[],
            learning_plan={},
            next_agent="",
            final_response=""
        )
        
        # Run through workflow
        config = {"configurable": {"thread_id": session_id}}
        result = await self.workflow.ainvoke(state, config)
        
        # Save conversation
        await self.memory.save_message(user_id, session_id, message, result["final_response"])
        
        return {
            "response": result["final_response"],
            "agent_used": result.get("next_agent"),
            "metadata": {
                "skills_identified": result.get("current_skills", []),
                "jobs_found": len(result.get("job_matches", [])),
                "learning_items": len(result.get("learning_plan", {}).get("items", []))
            }
        }
    
    async def analyze_profile(self, user_id: str, profile_data: Dict) -> Dict:
        """Full profile analysis"""
        state = AgentState(
            user_id=user_id,
            messages=[],
            user_profile=profile_data,
            current_skills=profile_data.get("skills", []),
            skill_gaps=[],
            target_roles=[],
            job_matches=[],
            learning_plan={},
            next_agent="profile",
            final_response=""
        )
        
        result = await self.profile_agent.process(state)
        return result
    
    async def find_job_matches(self, user_id: str) -> List[Dict]:
        """Find matching jobs"""
        user_profile = await self.memory.get_user_profile(user_id)
        
        state = AgentState(
            user_id=user_id,
            messages=[],
            user_profile=user_profile,
            current_skills=user_profile.get("skills", []),
            skill_gaps=[],
            target_roles=user_profile.get("target_roles", []),
            job_matches=[],
            learning_plan={},
            next_agent="market",
            final_response=""
        )
        
        result = await self.market_agent.process(state)
        return result.get("job_matches", [])
    
    async def generate_learning_roadmap(self, user_id: str) -> Dict:
        """Generate personalized learning roadmap"""
        user_profile = await self.memory.get_user_profile(user_id)
        
        state = AgentState(
            user_id=user_id,
            messages=[],
            user_profile=user_profile,
            current_skills=user_profile.get("skills", []),
            skill_gaps=[],
            target_roles=user_profile.get("target_roles", []),
            job_matches=[],
            learning_plan={},
            next_agent="learning",
            final_response=""
        )
        
        result = await self.learning_agent.process(state)
        return result.get("learning_plan", {})
    
    async def start_interview_practice(self, user_id: str, target_role: str) -> Dict:
        """Start interview practice session"""
        user_profile = await self.memory.get_user_profile(user_id)
        
        state = AgentState(
            user_id=user_id,
            messages=[HumanMessage(content=f"Practice interview for {target_role}")],
            user_profile=user_profile,
            current_skills=user_profile.get("skills", []),
            skill_gaps=[],
            target_roles=[target_role],
            job_matches=[],
            learning_plan={},
            next_agent="interview",
            final_response=""
        )
        
        result = await self.interview_agent.process(state)
        return result