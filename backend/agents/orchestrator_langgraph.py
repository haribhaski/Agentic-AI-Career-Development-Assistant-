# ============================================
# backend/agents/orchestrator_langgraph.py
# Advanced LangGraph-based multi-agent orchestration
# Install: pip install langgraph langchain-groq langchain-core
# ============================================

from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
import os
from datetime import datetime

# ============================================
# State Definition
# ============================================

class AgentState(TypedDict):
    """State shared across all agents"""
    messages: List[Dict[str, str]]
    user_id: str
    current_agent: str
    intent: str
    context: Dict[str, Any]
    final_response: str
    metadata: Dict[str, Any]

# ============================================
# LLM Configuration
# ============================================

def get_llm():
    """Initialize LLM (Groq or DeepSeek)"""
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
    
    if os.getenv("GROQ_API_KEY"):
        return ChatGroq(
            api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1000
        )
    else:
        # Fallback to mock for demo
        return None

# ============================================
# Agent Nodes
# ============================================

class IntentClassifier:
    """Classifies user intent and routes to appropriate agent"""
    
    def __init__(self, llm):
        self.llm = llm
        self.intents = {
            "profile": ["resume", "cv", "experience", "skills", "analyze profile"],
            "market": ["job", "hiring", "salary", "market", "opportunities"],
            "learning": ["learn", "course", "study", "roadmap", "skill development"],
            "interview": ["interview", "practice", "preparation", "mock interview"],
            "application": ["apply", "application", "cover letter", "submit"]
        }
    
    def classify(self, state: AgentState) -> AgentState:
        """Classify user intent"""
        user_message = state["messages"][-1]["content"].lower()
        
        # Simple keyword matching (can be replaced with LLM classification)
        for intent, keywords in self.intents.items():
            if any(kw in user_message for kw in keywords):
                state["intent"] = intent
                state["current_agent"] = intent
                return state
        
        state["intent"] = "general"
        state["current_agent"] = "orchestrator"
        return state

class ProfileAgentNode:
    """Resume and profile analysis agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def process(self, state: AgentState) -> AgentState:
        """Process profile-related queries"""
        user_message = state["messages"][-1]["content"]
        
        system_prompt = """You are a Career Profile Analysis Agent. Analyze resumes, 
        identify skill gaps, and provide actionable career advice. Be specific, 
        encouraging, and data-driven."""
        
        if self.llm:
            response = self.llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ])
            state["final_response"] = response.content
        else:
            state["final_response"] = f"""📊 **Profile Analysis**

I've analyzed your career profile. Here are my findings:

**Current Strengths:**
- 3+ years of software development experience
- Strong foundation in Python, JavaScript, React
- Good mix of technical and soft skills

**Growth Opportunities:**
- Cloud certifications (AWS/Azure) - High demand skill
- System design expertise - Critical for senior roles
- Open source contributions - Builds credibility

**Recommended Actions:**
1. Update resume with quantifiable achievements
2. Create portfolio showcasing best projects
3. Practice elevator pitch (2-minute intro)
4. Optimize LinkedIn profile for recruiter visibility

**Market Position:** You're in the 75th percentile for mid-level developers.

Would you like me to help with any specific area?"""
        
        state["metadata"]["agent_used"] = "profile"
        state["metadata"]["confidence"] = 0.92
        return state

class MarketAgentNode:
    """Job market analysis and matching agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def process(self, state: AgentState) -> AgentState:
        """Process job search queries"""
        user_message = state["messages"][-1]["content"]
        
        system_prompt = """You are a Job Market Analysis Agent. Search for jobs, 
        analyze market trends, provide salary insights, and match opportunities 
        to user profiles. Be data-driven and realistic."""
        
        if self.llm:
            response = self.llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ])
            state["final_response"] = response.content
        else:
            state["final_response"] = f"""💼 **Job Market Intelligence**

**Top Matching Opportunities:**

1. **Senior Software Engineer** @ TechCorp
   - 📍 Remote (US) | 💰 $120k-150k
   - Match Score: 94/100
   - Skills: Python, React, AWS, PostgreSQL
   - Posted: 2 days ago | 47 applicants
   
2. **Full Stack Developer** @ InnovateAI
   - 📍 San Francisco, CA (Hybrid) | 💰 $130k-160k
   - Match Score: 89/100
   - Skills: JavaScript, Node.js, React, MongoDB
   - Posted: 1 week ago | 89 applicants

3. **Backend Engineer** @ DataScale
   - 📍 Remote | 💰 $115k-145k
   - Match Score: 87/100
   - Skills: Python, FastAPI, Docker, Kubernetes
   - Posted: 3 days ago | 34 applicants

**Market Insights:**
- 📈 23% increase in remote positions
- 💰 Average salary for your skills: $135k
- 🔥 Highest demand: AI/ML, Cloud, DevOps
- 📊 Your profile ranks in top 15% of candidates

**Next Steps:**
1. Apply to top 3 matches today
2. Tailor resume for each position
3. Set up job alerts for similar roles

Ready to apply? I can help customize your application!"""
        
        state["metadata"]["agent_used"] = "market"
        state["metadata"]["jobs_found"] = 47
        return state

class LearningAgentNode:
    """Learning path and skill development agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def process(self, state: AgentState) -> AgentState:
        """Process learning-related queries"""
        user_message = state["messages"][-1]["content"]
        
        system_prompt = """You are a Career Learning & Development Agent. Create 
        personalized learning paths, recommend courses, and track skill progression. 
        Be structured, motivating, and focused on practical outcomes."""
        
        if self.llm:
            response = self.llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ])
            state["final_response"] = response.content
        else:
            state["final_response"] = f"""📚 **Personalized Learning Roadmap**

**Your 12-Week Career Acceleration Plan**

**Phase 1: Foundation (Weeks 1-4)**
🎯 Goal: Strengthen core technical skills

- **System Design Fundamentals** (10 hrs)
  - Resources: SystemDesignPrimer (GitHub), Grokking System Design
  - Projects: Design URL shortener, Chat system
  
- **Data Structures & Algorithms** (12 hrs)
  - Resources: LeetCode, AlgoExpert
  - Target: 50 problems (Easy → Medium)

**Phase 2: Specialization (Weeks 5-8)**
🎯 Goal: Develop marketable expertise

- **Cloud Architecture (AWS)** (15 hrs)
  - Resources: AWS Skill Builder (Free)
  - Certification: AWS Solutions Architect Associate
  
- **Microservices & APIs** (8 hrs)
  - Build: REST API with FastAPI
  - Deploy: Docker + Kubernetes basics

**Phase 3: Mastery (Weeks 9-12)**
🎯 Goal: Portfolio & market positioning

- **Build 3 Portfolio Projects**
  - Real-time chat app (WebSockets)
  - ML prediction API (FastAPI + ML)
  - Full-stack SaaS dashboard
  
- **Open Source Contribution** (5 hrs)
  - Find: "good first issue" on GitHub
  - Contribute: 3+ PRs to established projects

**Time Commitment:** 10-15 hrs/week
**Total Investment:** $0 (all free resources)
**Expected Outcome:** 25% salary increase potential

Ready to start? I can send you Week 1 materials!"""
        
        state["metadata"]["agent_used"] = "learning"
        state["metadata"]["learning_plan_created"] = True
        return state

class InterviewAgentNode:
    """Interview preparation and practice agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def process(self, state: AgentState) -> AgentState:
        """Process interview preparation queries"""
        user_message = state["messages"][-1]["content"]
        
        system_prompt = """You are an Interview Preparation Agent. Conduct mock 
        interviews, provide feedback, teach interview techniques, and build 
        confidence. Be constructive, encouraging, and thorough."""
        
        if self.llm:
            response = self.llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ])
            state["final_response"] = response.content
        else:
            state["final_response"] = f"""🎯 **Interview Preparation Plan**

**Your 3-Week Interview Bootcamp**

**Week 1: Technical Foundations**
- **Coding Practice** (Daily 1-2 hrs)
  - 5 Easy problems (Arrays, Strings)
  - 3 Medium problems (Trees, Graphs)
  - Focus: Explain your thought process clearly
  
- **System Design Basics**
  - Watch: 5 system design videos
  - Practice: Whiteboard simple systems

**Week 2: Behavioral Excellence**
- **STAR Method Examples** (Prepare 10)
  - Situation: Set context (1 sentence)
  - Task: Describe challenge (1 sentence)
  - Action: Explain your approach (2-3 sentences)
  - Result: Quantify impact (1 sentence with metrics)
  
- **Common Questions:**
  1. "Tell me about yourself" → 2-min pitch
  2. "Biggest weakness?" → Growth mindset + example
  3. "Why this company?" → Research + passion

**Week 3: Mock Interviews**
- **Schedule 3 Mock Interviews:**
  - Technical coding (45 min)
  - System design (60 min)
  - Behavioral (30 min)

**Practice Question (Technical):**
*"Given an array of integers, find two numbers that add up to a target."*

**Practice Question (Behavioral):**
*"Describe a time you disagreed with a team decision. How did you handle it?"*

**Pro Tips:**
- Ask clarifying questions before coding
- Think out loud during technical rounds
- Prepare 3-5 questions for the interviewer
- Follow up within 24 hours

Ready to start? Let's practice a coding problem!"""
        
        state["metadata"]["agent_used"] = "interview"
        state["metadata"]["practice_session"] = True
        return state

class ApplicationAgentNode:
    """Job application assistance agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def process(self, state: AgentState) -> AgentState:
        """Process application-related queries"""
        user_message = state["messages"][-1]["content"]
        
        system_prompt = """You are a Job Application Assistant Agent. Help with 
        resume tailoring, cover letter writing, application tracking, and 
        follow-ups. Be professional, detail-oriented, and strategic."""
        
        if self.llm:
            response = self.llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ])
            state["final_response"] = response.content
        else:
            state["final_response"] = f"""✍️ **Application Strategy & Support**

**Current Application Status:**
- ✅ Google (Software Engineer) - Submitted 2 days ago
- ⏳ Amazon (SDE II) - In Progress (resume ready)
- 📝 Microsoft (Full Stack) - Draft stage

**For Your Next Application:**

**1. Resume Optimization ✓**
- Tailored to job description
- Added quantifiable achievements:
  - "Reduced API response time by 40%"
  - "Led team of 4 engineers"
  - "Improved test coverage from 60% to 95%"
- ATS-optimized keywords included

**2. Cover Letter Template:**
```
Dear Hiring Manager,

I'm excited to apply for the [Position] at [Company]. With [X] years 
of experience in [Key Skills], I've consistently delivered [Type of Results].

Most recently at [Current Company], I [Specific Achievement with Metrics]. 
This experience has prepared me to contribute meaningfully to [Company's 
Specific Project/Goal].

I'm particularly drawn to [Company] because [Genuine Reason Based on Research]. 
I'd welcome the opportunity to discuss how my background in [Skill] aligns 
with your team's objectives.

Thank you for your consideration.

Best regards,
[Your Name]
```

**3. Application Checklist:**
- ✅ Resume updated with relevant keywords
- ✅ Cover letter customized to company
- ✅ LinkedIn profile matches resume
- ✅ Portfolio links tested and working
- ⏳ Reference list prepared
- ⏳ Thank you email template ready

**4. Strategic Timeline:**
- Day 1: Submit application before 10 AM
- Day 3: Connect with hiring manager on LinkedIn
- Week 1: Follow up if no response
- Week 2: Check application status

**Application Score:** 92/100
- Strong technical match
- Good culture fit indicators
- Clear career progression story

Ready to submit? Give me the job posting URL and I'll help optimize!"""
        
        state["metadata"]["agent_used"] = "application"
        state["metadata"]["applications_tracked"] = 8
        return state

# ============================================
# LangGraph Workflow
# ============================================

class CareerAgentOrchestrator:
    """Main orchestrator using LangGraph"""
    
    def __init__(self):
        self.llm = get_llm()
        self.intent_classifier = IntentClassifier(self.llm)
        self.agents = {
            "profile": ProfileAgentNode(self.llm),
            "market": MarketAgentNode(self.llm),
            "learning": LearningAgentNode(self.llm),
            "interview": InterviewAgentNode(self.llm),
            "application": ApplicationAgentNode(self.llm),
        }
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("classify_intent", self._classify_intent_node)
        workflow.add_node("profile_agent", self._profile_agent_node)
        workflow.add_node("market_agent", self._market_agent_node)
        workflow.add_node("learning_agent", self._learning_agent_node)
        workflow.add_node("interview_agent", self._interview_agent_node)
        workflow.add_node("application_agent", self._application_agent_node)
        workflow.add_node("default_response", self._default_response_node)
        
        # Set entry point
        workflow.set_entry_point("classify_intent")
        
        # Add conditional routing
        workflow.add_conditional_edges(
            "classify_intent",
            self._route_to_agent,
            {
                "profile": "profile_agent",
                "market": "market_agent",
                "learning": "learning_agent",
                "interview": "interview_agent",
                "application": "application_agent",
                "general": "default_response"
            }
        )
        
        # All agents end after processing
        for agent in ["profile_agent", "market_agent", "learning_agent", 
                      "interview_agent", "application_agent", "default_response"]:
            workflow.add_edge(agent, END)
        
        return workflow.compile()
    
    def _classify_intent_node(self, state: AgentState) -> AgentState:
        """Classify user intent"""
        return self.intent_classifier.classify(state)
    
    def _route_to_agent(self, state: AgentState) -> str:
        """Route to appropriate agent based on intent"""
        return state.get("intent", "general")
    
    def _profile_agent_node(self, state: AgentState) -> AgentState:
        return self.agents["profile"].process(state)
    
    def _market_agent_node(self, state: AgentState) -> AgentState:
        return self.agents["market"].process(state)
    
    def _learning_agent_node(self, state: AgentState) -> AgentState:
        return self.agents["learning"].process(state)
    
    def _interview_agent_node(self, state: AgentState) -> AgentState:
        return self.agents["interview"].process(state)
    
    def _application_agent_node(self, state: AgentState) -> AgentState:
        return self.agents["application"].process(state)
    
    def _default_response_node(self, state: AgentState) -> AgentState:
        """Default response for general queries"""
        state["final_response"] = """👋 **Welcome to Career AI!**

I'm your AI career companion with specialized agents to help you succeed:

🔹 **Profile Agent** - Resume analysis & skill assessment
🔹 **Market Agent** - Job search & salary insights  
🔹 **Learning Agent** - Personalized learning paths
🔹 **Interview Agent** - Interview prep & practice
🔹 **Application Agent** - Application assistance

**Try asking:**
- "Analyze my resume and suggest improvements"
- "Find software engineer jobs for me"
- "Create a learning roadmap for cloud computing"
- "Help me prepare for technical interviews"
- "Assist with my job application to Google"

What would you like help with today?"""
        state["metadata"]["agent_used"] = "orchestrator"
        return state
    
    async def process_message(self, message: str, user_id: str, 
                             history: List[Dict] = None) -> Dict[str, Any]:
        """Process user message through agent workflow"""
        initial_state = {
            "messages": history or [] + [{"role": "user", "content": message}],
            "user_id": user_id,
            "current_agent": "",
            "intent": "",
            "context": {},
            "final_response": "",
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "agent_used": "",
                "processing_time": "0.8s"
            }
        }
        
        # Run workflow
        result = self.workflow.invoke(initial_state)
        
        return {
            "response": result["final_response"],
            "agent_used": result["metadata"]["agent_used"],
            "metadata": result["metadata"]
        }

# ============================================
# Usage Example
# ============================================

if __name__ == "__main__":
    # Test the orchestrator
    orchestrator = CareerAgentOrchestrator()
    
    test_messages = [
        "Help me improve my resume",
        "Find me software engineer jobs",
        "Create a learning plan for me",
        "Practice interview questions with me"
    ]
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        result = orchestrator.process_message(msg, "test_user")
        print(f"Agent: {result['agent_used']}")
        print(f"Response: {result['response'][:100]}...")