# 🚀 Agentic AI Career Assistant

100% Free, State-of-the-art career development system using latest 2025 AI technology.

## Tech Stack

### Frontend
- Next.js 15 + React 19
- TypeScript
- Tailwind CSS v4
- shadcn/ui v2
- Framer Motion
- Supabase Auth

### Backend
- Python 3.11+
- FastAPI
- LangGraph (Multi-agent orchestration)
- DeepSeek R1 / Groq Llama 3.3
- Supabase (PostgreSQL + pgvector)
- Redis (Caching)

### AI & Agents
- DeepSeek R1 (Latest reasoning model)
- Groq (700+ tokens/sec)
- Gemini 2.0 Flash (Multimodal)
- LangGraph (Agent framework)
- Swarm (Multi-agent)

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- Redis (or use Docker)

### Installation

1. Clone and setup:
```bash
git clone <your-repo>
cd career-ai-agent
```

2. Setup frontend:
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Add your Supabase keys
npm run dev
```

3. Setup backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys
uvicorn main:app --reload
```

### Using Docker (Recommended)

```bash
docker-compose up
```

## Free API Keys Setup

1. **Groq** (Free): https://console.groq.com
2. **DeepSeek** (Free): https://platform.deepseek.com
3. **Supabase** (Free): https://supabase.com
4. **Serper** (2.5k free): https://serper.dev
5. **Firecrawl** (Free tier): https://firecrawl.dev
6. **Nomic** (Free): https://atlas.nomic.ai

## Features

- 🤖 Multi-agent AI system
- 👤 Intelligent profile analysis
- 📊 Real-time job matching
- 🎯 Personalized learning paths
- 📝 Auto-resume tailoring
- 🎤 Voice interview practice
- 📈 Progress tracking
- 🔄 Continuous learning from feedback

## License

MIT
