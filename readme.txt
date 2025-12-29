# 🚀 Agentic AI Career Development Assistant

**A cutting-edge, 100% free AI career companion using the latest 2025 technology stack**

![Status](https://img.shields.io/badge/status-production--ready-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![AI](https://img.shields.io/badge/AI-DeepSeek%20R1%20%7C%20Groq-purple)

---

## 🏆 **Built to Win - Key Features**

### **40% Architecture & Autonomy**
- ✅ **LangGraph Multi-Agent System** - True agentic behavior with state machines
- ✅ **6 Specialized Agents** - Profile, Market, Learning, Application, Interview, Feedback
- ✅ **Persistent Memory** - Long-term user context with Supabase + pgvector
- ✅ **Model Context Protocol (MCP)** - Latest Anthropic standard (Dec 2024)
- ✅ **Swarm Framework** - OpenAI's lightweight multi-agent orchestration

### **20% User Experience**
- ✅ **Humanistic Design** - Warm, encouraging, non-AI-like interface
- ✅ **Real-time Streaming** - Instant AI responses
- ✅ **Beautiful Auth** - Step-by-step onboarding with career goals
- ✅ **Mobile Responsive** - Works perfectly on all devices

### **20% Innovation & Adaptability**
- ✅ **Auto-Apply Agent** - Autonomous job applications with approval
- ✅ **Voice Interview Practice** - Real-time feedback on answers
- ✅ **Rejection Learning Loop** - Learns from failures to improve strategy
- ✅ **Career Simulation** - "What-if" scenario planning

### **20% Impact & Alignment**
- ✅ **Complete Career Journey** - From resume to job offer
- ✅ **Proven Architecture** - Based on successful industry patterns
- ✅ **Real Job Data** - Live scraping from multiple sources
- ✅ **Measurable Outcomes** - Track progress with metrics

---

## 🛠️ **Technology Stack (100% Free)**

### **Frontend**
- **Next.js 15** + React 19 - Latest framework
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Modern styling
- **shadcn/ui v2** - Beautiful components
- **Framer Motion** - Smooth animations
- **Supabase Auth** - Authentication

### **Backend**
- **Python 3.11+** - Modern Python
- **FastAPI** - High-performance API
- **LangGraph 0.2** - Agent orchestration
- **LangChain 0.3** - AI framework

### **AI Models (All Free)**
- **DeepSeek R1** - Latest reasoning model (Jan 2025) 🆕
- **Groq Llama 3.3 70B** - Ultra-fast inference (700+ tokens/sec)
- **Gemini 2.0 Flash** - Multimodal capabilities
- **Nomic Embed v1.5** - Free embeddings

### **Database & Storage**
- **Supabase** - PostgreSQL + pgvector (Free tier)
- **Redis** - Session caching
- **Chroma** - Local vector storage

### **Intelligence Gathering**
- **Serper API** - Google Search (Free 2.5k/month)
- **Firecrawl** - Web scraping (Free tier)
- **Brave Search** - Alternative search (Free tier)

---

## 📋 **Prerequisites**

- Node.js 20+
- Python 3.11+
- Git
- A text editor (VS Code recommended)

---

## 🚀 **Quick Start (5 Minutes)**

### **Step 1: Clone & Setup**

```bash
# Run the setup script from the first artifact
bash setup.sh

# OR manually:
mkdir career-ai-agent && cd career-ai-agent
# Copy folder structure from setup script
```

### **Step 2: Get Free API Keys** (5 minutes total)

#### Required APIs (All Free):

1. **Groq** (1 min) - https://console.groq.com
   - Sign up with Google
   - Copy API key
   - Free: 30 requests/min

2. **DeepSeek** (1 min) - https://platform.deepseek.com
   - Create account
   - Get API key
   - Free: Unlimited (currently)

3. **Supabase** (2 min) - https://supabase.com
   - Create new project
   - Copy URL and anon key
   - Run SQL schema from `database_schema.sql`
   - Free: 500MB database, 2GB bandwidth

4. **Serper** (1 min) - https://serper.dev
   - Sign up
   - Get API key
   - Free: 2,500 searches/month

#### Optional (but recommended):

5. **Gemini** - https://makersuite.google.com
6. **Firecrawl** - https://firecrawl.dev
7. **Nomic** - https://atlas.nomic.ai

### **Step 3: Configure Environment**

```bash
# Frontend (.env.local)
cd frontend
cp .env.example .env.local

# Edit with your values:
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend (.env)
cd ../backend
cp .env.example .env

# Edit with your API keys:
GROQ_API_KEY=your_groq_key
DEEPSEEK_API_KEY=your_deepseek_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_service_role_key
SERPER_API_KEY=your_serper_key
JWT_SECRET_KEY=your_random_secret_key
```

### **Step 4: Install Dependencies**

```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **Step 5: Setup Database**

```bash
# In Supabase dashboard:
# 1. Go to SQL Editor
# 2. Copy/paste the entire database_schema.sql
# 3. Run query
# 4. Verify tables created
```

### **Step 6: Run the Application**

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev

# Open browser: http://localhost:3000
```

---

## 🐳 **Docker Setup (Recommended)**

```bash
# Start everything with one command
docker-compose up

# Includes:
# - Frontend (port 3000)
# - Backend (port 8000)
# - Redis (port 6379)
```

---

## 📁 **Project Structure**

```
career-ai-agent/
├── frontend/                    # Next.js application
│   ├── app/
│   │   ├── auth/               # Login, signup pages
│   │   ├── dashboard/          # Main dashboard
│   │   ├── profile/            # User profile
│   │   ├── jobs/               # Job listings
│   │   ├── learning/           # Learning paths
│   │   └── interview/          # Interview practice
│   ├── components/
│   │   ├── ui/                 # shadcn components
│   │   ├── layout/             # Layout components
│   │   └── career/             # Career-specific components
│   └── lib/                    # Utilities
│
├── backend/                     # FastAPI application
│   ├── agents/                 # Specialized agents
│   │   ├── orchestrator.py     # Main coordinator
│   │   ├── profile_agent.py
│   │   ├── market_agent.py
│   │   ├── learning_agent.py
│   │   ├── application_agent.py
│   │   ├── interview_agent.py
│   │   └── feedback_agent.py
│   ├── services/               # Business logic
│   │   ├── auth.py
│   │   ├── memory.py
│   │   ├── supabase_client.py
│   │   └── scraper.py
│   ├── models/                 # Data models
│   ├── utils/                  # Utilities
│   ├── main.py                 # FastAPI app
│   └── config.py               # Configuration
│
├── shared/                      # Shared types
├── docs/                        # Documentation
├── docker-compose.yml
└── README.md
```

---

## 🎯 **Usage Examples**

### **1. Profile Analysis**
```
User: "Analyze my resume"
AI: *Extracts skills, identifies gaps, suggests improvements*
```

### **2. Job Matching**
```
User: "Find me software engineer jobs"
AI: *Searches, scores, ranks jobs by fit*
```

### **3. Learning Roadmap**
```
User: "I want to learn React"
AI: *Generates 12-week plan with resources*
```

### **4. Interview Practice**
```
User: "Practice technical interview"
AI: *Asks questions, evaluates answers, gives feedback*
```

### **5. Application Assistance**
```
User: "Help me apply to Google"
AI: *Tailors resume, writes cover letter, tracks application*
```

---

## 🧪 **Testing the Agent System**

### **Test Profile Agent:**
```bash
curl -X POST http://localhost:8000/api/profile/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "React"],
    "experience_level": "entry",
    "career_goal": "Software Engineer"
  }'
```

### **Test Job Matching:**
```bash
curl -X GET http://localhost:8000/api/jobs/match \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🎨 **Customization**

### **Change AI Model:**
```python
# backend/agents/orchestrator.py
# Replace Groq with DeepSeek R1
from openai import OpenAI

llm = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url="https://api.deepseek.com"
)
```

### **Add New Agent:**
```python
# 1. Create new agent file
# backend/agents/networking_agent.py

class NetworkingAgent:
    async def process(self, state):
        # Your logic here
        pass

# 2. Register in orchestrator
self.networking_agent = NetworkingAgent(self.llm)
workflow.add_node("networking", self.networking_agent.process)
```

---

## 📊 **Monitoring & Analytics**

### **View User Stats:**
```sql
SELECT * FROM user_career_dashboard WHERE user_id = 'your_user_id';
```

### **Track Agent Performance:**
```sql
SELECT agent_used, COUNT(*) 
FROM conversations 
GROUP BY agent_used;
```

---

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **"Module not found" errors**
   ```bash
   # Reinstall dependencies
   cd frontend && npm install
   cd backend && pip install -r requirements.txt
   ```

2. **Database connection errors**
   - Check Supabase URL and keys in .env
   - Verify RLS policies are set correctly

3. **API rate limits**
   - Groq: 30 req/min (free tier)
   - Switch to DeepSeek for unlimited

4. **CORS errors**
   - Check CORS settings in `main.py`
   - Verify frontend URL in allowed origins

---

## 🚀 **Deployment**

### **Frontend (Vercel - Free)**
```bash
cd frontend
vercel
```

### **Backend (Railway - Free)**
```bash
cd backend
# Connect to Railway
# Deploy automatically
```

### **Database**
- Supabase handles hosting (included in free tier)

---

## 📈 **Performance Optimization**

- **Redis caching** for frequent queries
- **Connection pooling** for database
- **Lazy loading** for embeddings
- **Rate limiting** on API endpoints
- **Response streaming** for better UX

---

## 🔒 **Security**

- ✅ Row Level Security (RLS) on all tables
- ✅ JWT authentication
- ✅ API key encryption
- ✅ CORS protection
- ✅ Input validation
- ✅ SQL injection prevention

---

## 🤝 **Contributing**

This is a competition project, but after the hackathon:
1. Fork the repository
2. Create feature branch
3. Submit pull request

---

## 📄 **License**

MIT License - free to use and modify

---

## 🎯 **Competition Strategy**

### **Demo Flow (10 minutes):**

**Minutes 0-2: Problem Statement**
- Show confusing career landscape
- Explain need for AI guidance

**Minutes 2-4: Architecture Deep-Dive**
- Show LangGraph diagram
- Explain multi-agent system
- Demonstrate MCP integration

**Minutes 4-7: Live Demo**
- User uploads resume
- AI analyzes and finds jobs
- Auto-tailors application
- Shows learning roadmap

**Minutes 7-9: Innovation Showcase**
- Voice interview practice
- Rejection learning loop
- Career simulation

**Minutes 9-10: Impact & Metrics**
- Show user analytics
- Present success stories
- Future roadmap

### **Judging Criteria Optimization:**

**Architecture (40%)**
- ✅ 6 specialized agents
- ✅ LangGraph state machines
- ✅ Persistent memory
- ✅ Latest protocols (MCP)

**UX (20%)**
- ✅ Beautiful, humanistic design
- ✅ Real-time streaming
- ✅ Mobile-responsive

**Innovation (20%)**
- ✅ Auto-apply feature
- ✅ Voice practice
- ✅ Learning loop
- ✅ Simulation mode

**Impact (20%)**
- ✅ Solves real problem
- ✅ Complete solution
- ✅ Measurable results

---

## 📞 **Support**

For issues or questions:
- Check `docs/` folder
- Review error logs
- Test with sample data

---

## 🎉 **Acknowledgments**

Built with:
- DeepSeek AI
- Anthropic (MCP)
- OpenAI (Swarm)
- Groq
- Supabase
- Vercel
- The open-source community

---

**Ready to win? Let's build the future of career development! 🚀**