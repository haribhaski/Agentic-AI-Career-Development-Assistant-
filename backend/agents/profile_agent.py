from typing import Dict, List, Any
from langchain_core.messages import HumanMessage
import json

class ProfileAgent:
    """Analyzes resumes, extracts skills, identifies gaps"""
    
    def __init__(self, llm):
        self.llm = llm
        # Removed unnecessary SentenceTransformer - LLM handles everything
    
    async def process(self, state: Dict) -> Dict:
        """Process profile-related requests"""
        
        if not self.llm:
            state["final_response"] = "Profile agent requires LLM configuration"
            state["next_agent"] = "end"
            return state
        
        user_profile = state.get("user_profile", {})
        messages = state.get("messages", [])
        
        # Extract skills from profile
        skills = await self._extract_skills(user_profile)
        state["current_skills"] = skills
        
        # Analyze career trajectory
        career_analysis = await self._analyze_career_path(user_profile, skills)
        
        # Identify skill gaps for target roles
        skill_gaps = await self._identify_skill_gaps(
            skills,
            state.get("target_roles", [])
        )
        state["skill_gaps"] = skill_gaps
        
        # Generate response
        response = await self._generate_response(
            career_analysis,
            skills,
            skill_gaps
        )
        
        state["final_response"] = response
        state["next_agent"] = "end"
        
        return state
    
    async def _extract_skills(self, profile: Dict) -> List[str]:
        """Extract skills using LLM"""
        
        prompt = f"""Analyze this profile and extract ALL technical and soft skills.
        
        Profile: {json.dumps(profile)}
        
        Return a JSON array of skills. Example: ["Python", "React", "Team Leadership"]
        Return ONLY the JSON array, no other text."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        
        try:
            # Clean response - remove markdown code blocks if present
            content = response.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            skills = json.loads(content)
            return skills if isinstance(skills, list) else []
        except Exception as e:
            # Fallback: extract from profile
            return profile.get("skills", [])
    
    async def _analyze_career_path(self, profile: Dict, skills: List[str]) -> str:
        """Analyze career trajectory and provide insights"""
        
        prompt = f"""Analyze this career profile and provide insights:
        
        Profile: {json.dumps(profile)}
        Skills: {skills}
        
        Provide:
        1. Current career stage assessment
        2. Strengths
        3. Areas for development
        4. Recommended next steps
        
        Be encouraging and specific."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
    
    async def _identify_skill_gaps(
        self,
        current_skills: List[str],
        target_roles: List[str]
    ) -> List[Dict]:
        """Identify skills needed for target roles"""
        
        if not target_roles:
            return []
        
        prompt = f"""Given these current skills: {current_skills}
        
        And these target roles: {target_roles}
        
        Identify the TOP 5 skill gaps that need to be filled.
        
        Return as JSON array with format:
        [{{"skill": "AWS", "importance": "high", "time_to_learn": "2-3 months"}}]
        
        Return ONLY the JSON array."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        
        try:
            content = response.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            gaps = json.loads(content)
            return gaps if isinstance(gaps, list) else []
        except Exception as e:
            return []
    
    async def _generate_response(
        self,
        analysis: str,
        skills: List[str],
        gaps: List[Dict]
    ) -> str:
        """Generate final user-friendly response"""
        
        response = f"""## Your Profile Analysis

{analysis}

### Your Skills ({len(skills)})
{', '.join(skills[:10])}{"..." if len(skills) > 10 else ""}

"""
        if gaps:
            response += f"""### Skills to Develop
"""
            for gap in gaps[:5]:
                response += f"- **{gap.get('skill', 'Unknown')}** ({gap.get('importance', 'medium')} priority) - {gap.get('time_to_learn', 'varies')}\n"
        
        return response
