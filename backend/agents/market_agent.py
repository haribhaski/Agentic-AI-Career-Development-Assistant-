
from typing import Dict, List, Any
from langchain_core.messages import HumanMessage
from firecrawl import FirecrawlApp
import httpx
import json
from config import get_settings

settings = get_settings()

class MarketIntelligenceAgent:
    """Searches jobs, analyzes market trends using Serper & Firecrawl"""
    
    def __init__(self, llm):
        self.llm = llm
        self.firecrawl = FirecrawlApp(api_key=settings.firecrawl_api_key) if settings.firecrawl_api_key else None
    
    async def process(self, state: Dict) -> Dict:
        """Find and analyze job opportunities using 2025 intelligence tools"""
        
        skills = state.get("current_skills", [])
        target_roles = state.get("target_roles", [])
        
        # Search for jobs using Serper
        jobs = await self._search_jobs_serper(skills, target_roles)
        state["job_matches"] = jobs
        
        # Analyze market trends
        trends = await self._analyze_market_trends(skills)
        
        # Calculate fit scores using reasoning
        scored_jobs = await self._score_job_matches(jobs, skills)
        
        # Generate response
        response = await self._generate_response(scored_jobs, trends)
        
        state["final_response"] = response
        state["next_agent"] = "end"
        
        return state
    
    async def _search_jobs_serper(
        self,
        skills: List[str],
        roles: List[str]
    ) -> List[Dict]:
        """Search for jobs using Serper.dev API"""
        
        if not settings.serper_api_key:
            return self._fallback_jobs()
            
        query = f"{' '.join(roles[:2])} {' '.join(skills[:2])} jobs"
        url = "https://google.serper.dev/search"
        
        payload = json.dumps({
            "q": query,
            "gl": "us",
            "hl": "en",
            "autocorrect": True
        })
        headers = {
            'X-API-KEY': settings.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                results = response.json()
                # Parse search results into job objects
                jobs = []
                for result in results.get("organic", [])[:10]:
                    jobs.append({
                        "title": result.get("title", "Unknown Role"),
                        "company": result.get("snippet", "").split("-")[0].strip(),
                        "location": "See link",
                        "description": result.get("snippet", ""),
                        "posted": "Recent",
                        "url": result.get("link", "")
                    })
                return jobs
        
        return self._fallback_jobs()

    def _fallback_jobs(self) -> List[Dict]:
        return [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "location": "Remote",
                "description": "Looking for talented engineers...",
                "posted": "2 days ago",
                "url": "https://linkedin.com/jobs"
            }
        ]
    
    async def _score_job_matches(
        self,
        jobs: List[Dict],
        skills: List[str]
    ) -> List[Dict]:
        """Score each job based on skill match using LLM"""
        
        if not jobs:
            return []
            
        # Score top 5 jobs to save tokens/time
        top_jobs = jobs[:5]
        
        for job in top_jobs:
            prompt = f"""Rate how well this candidate matches this job (0-100):
            
            Candidate skills: {skills}
            Job: {job['title']} - {job['description']}
            
            Return ONLY a number 0-100."""
            
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            
            try:
                score_text = response.content.strip()
                # Extract number from response
                score = int(''.join(filter(str.isdigit, score_text)))
                job["fit_score"] = score
            except:
                job["fit_score"] = 50
        
        return sorted(top_jobs, key=lambda x: x.get("fit_score", 0), reverse=True)
    
    async def _analyze_market_trends(self, skills: List[str]) -> str:
        """Analyze current market demand"""
        
        prompt = f"""Analyze the 2025 job market trends for someone with these skills: {skills}
        
        Include:
        1. Current demand & salary expectations
        2. Impact of AI in this field
        3. Emerging skills to watch
        
        Be concise and insightful."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
    
    async def _generate_response(self, jobs: List[Dict], trends: str) -> str:
        """Generate user-friendly response with 2025 insights"""
        
        response = f"""## 📊 Market Intelligence Insights
        
{trends}

### 🎯 Strategic Job Matches

"""
        for i, job in enumerate(jobs, 1):
            response += f"""{i}. **{job['title']}** | {job['company']}
   - **Fit Score:** {job.get('fit_score', 'N/A')}%
   - **Insight:** {job['description'][:150]}...
   - [Apply Now]({job['url']})

"""
        
        return response
