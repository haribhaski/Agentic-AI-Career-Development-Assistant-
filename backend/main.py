# ============================================
# backend/main.py
# FastAPI server with multi-agent orchestration
# ============================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import uvicorn

# Initialize FastAPI
app = FastAPI(title="Career AI Agent API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Data Models
# ============================================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    agent_used: str
    metadata: Optional[Dict[str, Any]] = None
    stats: Optional[Dict[str, int]] = None

# ============================================
# Simple Multi-Agent System (No Dependencies)
# ============================================

class Agent:
    """Base agent class"""
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    def process(self, message: str, context: Dict) -> str:
        """Process message and return response"""
        return f"[{self.name}] Processing: {message}"

class ProfileAgent(Agent):
    """Analyzes resumes and career profiles"""
    def __init__(self):
        super().__init__("Profile Agent", "Resume & Profile Analysis")
    
    def process(self, message: str, context: Dict) -> str:
        keywords = ["resume", "cv", "profile", "experience", "skills", "analyze"]
        if any(kw in message.lower() for kw in keywords):
            return """📊 **Profile Analysis Complete**

I've analyzed your profile and here's what I found:

**Strengths:**
- Strong technical foundation in Python, JavaScript, React
- 3+ years of relevant experience
- Good mix of frontend and backend skills

**Areas for Improvement:**
- Consider adding cloud certifications (AWS/Azure)
- Build more projects showcasing system design
- Strengthen data structures & algorithms

**Recommended Next Steps:**
1. Update LinkedIn with recent projects
2. Add quantifiable achievements to resume
3. Prepare a 2-minute elevator pitch

Would you like me to help with any specific area?"""
        return None

class MarketAgent(Agent):
    """Searches and matches job opportunities"""
    def __init__(self):
        super().__init__("Market Agent", "Job Search & Matching")
    
    def process(self, message: str, context: Dict) -> str:
        keywords = ["job", "hiring", "opportunity", "position", "openings", "find"]
        if any(kw in message.lower() for kw in keywords):
            return """💼 **Job Market Analysis**

I've found **47 matching opportunities** for you:

**Top Matches:**

1. **Senior Software Engineer** - TechCorp
   - 📍 Remote | 💰 $120k-150k
   - Match Score: 94%
   - Skills: Python, React, AWS
   
2. **Full Stack Developer** - StartupXYZ
   - 📍 San Francisco, CA | 💰 $110k-140k
   - Match Score: 89%
   - Skills: JavaScript, Node.js, MongoDB

3. **Backend Engineer** - InnovateAI
   - 📍 Hybrid (NY) | 💰 $130k-160k
   - Match Score: 87%
   - Skills: Python, FastAPI, PostgreSQL

**Market Insights:**
- Average salary for your skills: $135k
- 23% increase in remote positions
- High demand for AI/ML experience

Would you like me to help you apply to any of these?"""
        return None

class LearningAgent(Agent):
    """Creates personalized learning paths"""
    def __init__(self):
        super().__init__("Learning Agent", "Career Development & Learning")
    
    def process(self, message: str, context: Dict) -> str:
        keywords = ["learn", "course", "study", "improve", "skill", "path", "roadmap"]
        if any(kw in message.lower() for kw in keywords):
            return """📚 **Personalized Learning Roadmap**

Based on your goals, here's your 12-week plan:

**Phase 1: Foundation (Weeks 1-4)**
- System Design Fundamentals
- Advanced Data Structures
- Design Patterns in Python
- Resources: MIT OpenCourseWare, LeetCode

**Phase 2: Specialization (Weeks 5-8)**
- Cloud Architecture (AWS)
- Microservices & APIs
- Database Optimization
- Resources: AWS Skill Builder, Udemy

**Phase 3: Mastery (Weeks 9-12)**
- Build 3 portfolio projects
- Contribute to open source
- Mock interviews
- Resources: GitHub, CodeSignal

**Time Commitment:** 10-15 hours/week
**Estimated Cost:** Free (all resources available free)

Ready to start? I can send you specific links!"""
        return None

class InterviewAgent(Agent):
    """Helps with interview preparation"""
    def __init__(self):
        super().__init__("Interview Agent", "Interview Preparation")
    
    def process(self, message: str, context: Dict) -> str:
        keywords = ["interview", "practice", "questions", "prepare", "mock"]
        if any(kw in message.lower() for kw in keywords):
            return """🎯 **Interview Preparation Guide**

Let's get you ready! Here's what we'll cover:

**Technical Interview Prep:**
1. **Coding Challenges** (2-3 weeks)
   - 50 LeetCode problems (Easy → Medium)
   - Focus: Arrays, Strings, Trees, Graphs
   
2. **System Design** (1-2 weeks)
   - Design Twitter/Instagram/Uber
   - Learn: Load balancing, caching, databases

**Behavioral Interview Prep:**
- STAR method examples
- "Tell me about yourself" script
- Questions to ask interviewers

**Mock Interview Schedule:**
- Week 1: Coding practice
- Week 2: System design mock
- Week 3: Behavioral + final mock

**Practice Question:**
*"Describe a time you solved a difficult technical problem."*

Want to start with a coding problem or behavioral question?"""
        return None

class ApplicationAgent(Agent):
    """Assists with job applications"""
    def __init__(self):
        super().__init__("Application Agent", "Application Management")
    
    def process(self, message: str, context: Dict) -> str:
        keywords = ["apply", "application", "submit", "cover letter"]
        if any(kw in message.lower() for kw in keywords):
            return """✍️ **Application Assistant**

I'll help you craft a winning application!

**Current Applications:**
- Google - Software Engineer (Submitted 2 days ago)
- Amazon - SDE II (In Progress)
- Microsoft - Full Stack Dev (Draft)

**For Your Next Application:**

1. **Tailored Resume** ✓
   - Highlighted relevant skills
   - Added quantifiable achievements
   - ATS-optimized

2. **Cover Letter Template:**
   ```
   Dear Hiring Manager,
   
   I'm excited to apply for [Position] at [Company].
   With [X years] of experience in [Skills], I've [Achievement].
   
   At [Current Company], I [Specific accomplishment with numbers].
   I'm particularly drawn to [Company] because [Research-based reason].
   
   I'd love to discuss how my experience in [Skill] can contribute
   to [Company's goal/project].
   ```

3. **Application Checklist:**
   - [ ] Resume updated
   - [ ] Cover letter customized
   - [ ] LinkedIn profile current
   - [ ] Portfolio links working

Ready to apply? Give me the job posting URL!"""
        return None

class OrchestratorAgent:
    """Main orchestrator that routes to specialized agents"""
    def __init__(self):
        self.agents = {
            "profile": ProfileAgent(),
            "market": MarketAgent(),
            "learning": LearningAgent(),
            "interview": InterviewAgent(),
            "application": ApplicationAgent(),
        }
        self.default_response = """👋 I'm your AI career companion with multiple specialized agents:

🔹 **Profile Agent** - Resume analysis & career assessment
🔹 **Market Agent** - Job search & salary insights
🔹 **Learning Agent** - Personalized learning paths
🔹 **Interview Agent** - Interview preparation & practice
🔹 **Application Agent** - Application assistance & tracking

**Popular Commands:**
- "Analyze my resume"
- "Find software engineer jobs"
- "Create a learning roadmap"
- "Help me prepare for interviews"
- "Assist with my application"

What would you like help with today?"""
    
    def route_message(self, message: str, context: Dict) -> tuple:
        """Route message to appropriate agent"""
        # Try each agent
        for agent_name, agent in self.agents.items():
            response = agent.process(message, context)
            if response:
                return response, agent_name
        
        # Default response if no agent matches
        return self.default_response, "orchestrator"

# Initialize orchestrator
orchestrator = OrchestratorAgent()

# ============================================
# API Endpoints
# ============================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents_active": len(orchestrator.agents),
        "version": "1.0.0"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with multi-agent routing"""
    try:
        # Build context from conversation history
        context = {
            "user_id": request.user_id,
            "history": request.conversation_history,
            "timestamp": datetime.utcnow()
        }
        
        # Route message to appropriate agent
        response, agent_used = orchestrator.route_message(request.message, context)
        
        # Generate mock stats (in production, fetch from database)
        stats = {
            "skills_tracked": 12,
            "jobs_matched": 47,
            "learning_hours": 23,
            "applications": 8
        }
        
        return ChatResponse(
            response=response,
            agent_used=agent_used,
            metadata={
                "timestamp": datetime.utcnow().isoformat(),
                "processing_time": "0.8s"
            },
            stats=stats
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents")
async def list_agents():
    """List all available agents"""
    agents_info = []
    for name, agent in orchestrator.agents.items():
        agents_info.append({
            "name": name,
            "role": agent.role,
            "status": "active"
        })
    return {"agents": agents_info, "total": len(agents_info)}

@app.get("/api/stats/{user_id}")
async def get_user_stats(user_id: str):
    """Get user statistics"""
    # Mock data - replace with database query
    return {
        "user_id": user_id,
        "skills_tracked": 12,
        "jobs_matched": 47,
        "learning_hours": 23,
        "applications": 8,
        "interviews_scheduled": 3,
        "last_activity": datetime.utcnow().isoformat()
    }

# ============================================
# Run Server
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )