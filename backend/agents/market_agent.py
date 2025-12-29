
from typing import Dict, List
import aiohttp
from bs4 import BeautifulSoup
import json

class MarketIntelligenceAgent:
    """Searches jobs, analyzes market trends, finds opportunities"""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def process(self, state: Dict) -> Dict:
        """Find and analyze job opportunities"""
        
        skills = state.get("current_skills", [])
        target_roles = state.get("target_roles", [])
        
        # Search for jobs
        jobs = await self._search_jobs(skills, target_roles)
        state["job_matches"] = jobs
        
        # Analyze market trends
        trends = await self._analyze_market_trends(skills)
        
        # Calculate fit scores
        scored_jobs = await self._score_job_matches(jobs, skills)
        
        # Generate response
        response = await self._generate_response(scored_jobs, trends)
        
        state["final_response"] = response
        state["next_agent"] = "end"
        
        return state
    
    async def _search_jobs(
        self,
        skills: List[str],
        roles: List[str]
    ) -> List[Dict]:
        """Search for jobs using free APIs"""
        
        # Use Serper API (free tier)
        query = f"{' '.join(roles[:2])} {' '.join(skills[:3])} jobs"
        
        # Simulate job search (replace with actual API call)
        jobs = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "location": "Remote",
                "description": "Looking for Python and React developer...",
                "posted": "2 days ago",
                "url": "https://example.com/job1"
            },
            # Add more jobs from actual search
        ]
        
        return jobs
    
    async def _score_job_matches(
        self,
        jobs: List[Dict],
        skills: List[str]
    ) -> List[Dict]:
        """Score each job based on skill match"""
        
        for job in jobs:
            prompt = f"""Rate how well this candidate matches this job (0-100):
            
            Candidate skills: {skills}
            Job: {job['title']} - {job['description']}
            
            Return ONLY a number 0-100."""
            
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            
            try:
                score = int(response.content.strip())
                job["fit_score"] = score
            except:
                job["fit_score"] = 50
        
        # Sort by fit score
        return sorted(jobs, key=lambda x: x.get("fit_score", 0), reverse=True)
    
    async def _analyze_market_trends(self, skills: List[str]) -> str:
        """Analyze current market demand"""
        
        prompt = f"""Analyze the current job market for someone with these skills: {skills}
        
        Provide:
        1. Market demand (hot/moderate/slow)
        2. Average salary range
        3. Trending skills in this space
        4. Geographic hotspots
        
        Be data-driven and realistic."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
    
    async def _generate_response(self, jobs: List[Dict], trends: str) -> str:
        """Generate user-friendly response"""
        
        response = f"""## Job Market Analysis

{trends}

### Top Matches for You

"""
        for i, job in enumerate(jobs[:5], 1):
            response += f"""
{i}. **{job['title']}** at {job['company']}
   - Location: {job['location']}
   - Fit Score: {job.get('fit_score', 'N/A')}%
   - Posted: {job['posted']}
   - [View Job]({job['url']})
   
"""
        
        return response