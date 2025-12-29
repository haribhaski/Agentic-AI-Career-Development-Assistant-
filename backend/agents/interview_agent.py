from typing import Dict, List
from langchain_core.messages import HumanMessage
import json
class InterviewAgent:
    """Conducts mock interviews, provides feedback"""
    
    def __init__(self, llm):
        self.llm = llm
        self.interview_questions = {}
    
    async def process(self, state: Dict) -> Dict:
        """Conduct interview practice"""
        
        target_role = state.get("target_roles", ["Software Engineer"])[0]
        skills = state.get("current_skills", [])
        
        # Generate interview questions
        questions = await self._generate_questions(target_role, skills)
        
        response = f"""## Mock Interview: {target_role}

I'll ask you {len(questions)} questions. Take your time with each answer.

**Question 1:** {questions[0]['question']}

Type your answer when ready!"""
        
        state["final_response"] = response
        state["next_agent"] = "end"
        
        return state
    
    async def _generate_questions(self, role: str, skills: List[str]) -> List[Dict]:
        """Generate role-specific interview questions"""
        
        prompt = f"""Generate 5 interview questions for a {role} position.
        
        Candidate skills: {skills}
        
        Include:
        - 2 technical questions
        - 2 behavioral questions
        - 1 problem-solving question
        
        Return as JSON array with format:
        [{{"question": "...", "type": "technical", "difficulty": "medium"}}]
        
        Return ONLY valid JSON."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        
        try:
            questions = json.loads(response.content)
            return questions
        except:
            return [{"question": "Tell me about yourself", "type": "behavioral"}]
