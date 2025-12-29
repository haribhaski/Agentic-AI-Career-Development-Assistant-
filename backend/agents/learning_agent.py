from typing import Dict, List
from langchain_core.messages import HumanMessage
import json
class LearningPathAgent:
    """Creates personalized learning roadmaps"""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def process(self, state: Dict) -> Dict:
        """Generate personalized learning plan"""
        
        skills = state.get("current_skills", [])
        gaps = state.get("skill_gaps", [])
        target_roles = state.get("target_roles", [])
        
        # Generate learning roadmap
        roadmap = await self._create_roadmap(skills, gaps, target_roles)
        state["learning_plan"] = roadmap
        
        # Find resources
        resources = await self._find_learning_resources(gaps)
        roadmap["resources"] = resources
        
        # Generate response
        response = await self._generate_response(roadmap)
        
        state["final_response"] = response
        state["next_agent"] = "end"
        
        return state
    
    async def _create_roadmap(
        self,
        skills: List[str],
        gaps: List[Dict],
        roles: List[str]
    ) -> Dict:
        """Create structured learning roadmap"""
        
        prompt = f"""Create a 12-week learning roadmap for:
        
        Current skills: {skills}
        Skill gaps: {gaps}
        Target roles: {roles}
        
        Return as JSON with this structure:
        {{
          "weeks": [
            {{
              "week": 1,
              "focus": "Python Basics",
              "goals": ["Learn syntax", "Build calculator"],
              "hours_per_week": 10
            }}
          ],
          "milestones": [
            {{"week": 4, "milestone": "Complete first project"}}
          ]
        }}
        
        Return ONLY valid JSON."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        
        try:
            roadmap = json.loads(response.content)
            return roadmap
        except:
            return {"weeks": [], "milestones": []}
    
    async def _find_learning_resources(self, gaps: List[Dict]) -> List[Dict]:
        """Find free learning resources"""
        
        resources = []
        
        for gap in gaps[:5]:
            skill = gap.get("skill", "")
            
            prompt = f"""Find the top 3 FREE learning resources for: {skill}
            
            Return as JSON array:
            [{{
              "title": "Python Crash Course",
              "platform": "YouTube",
              "url": "https://...",
              "type": "video",
              "duration": "4 hours"
            }}]
            
            Return ONLY valid JSON array."""
            
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            
            try:
                skill_resources = json.loads(response.content)
                resources.extend(skill_resources)
            except:
                pass
        
        return resources
    
    async def _generate_response(self, roadmap: Dict) -> str:
        """Generate user-friendly roadmap"""
        
        response = """## Your Personalized Learning Roadmap

"""
        
        weeks = roadmap.get("weeks", [])
        for week_data in weeks[:4]:  # Show first 4 weeks
            response += f"""
### Week {week_data['week']}: {week_data['focus']}
- Goals: {', '.join(week_data['goals'])}
- Time: {week_data['hours_per_week']} hours/week

"""
        
        response += "\n### Learning Resources\n\n"
        for resource in roadmap.get("resources", [])[:5]:
            response += f"- [{resource['title']}]({resource['url']}) ({resource['platform']})\n"
        
        return response

