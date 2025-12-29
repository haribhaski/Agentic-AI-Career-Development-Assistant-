from typing import Dict, List
from langchain_core.messages import HumanMessage

class ApplicationAgent:
    """Handles resume tailoring, cover letters, applications"""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def process(self, state: Dict) -> Dict:
        """Handle application-related requests"""
        
        messages = state.get("messages", [])
        last_message = messages[-1].content if messages else ""
        
        # Determine action
        if "resume" in last_message.lower():
            response = await self._tailor_resume(state)
        elif "cover letter" in last_message.lower():
            response = await self._generate_cover_letter(state)
        else:
            response = await self._general_application_advice(state)
        
        state["final_response"] = response
        state["next_agent"] = "end"
        
        return state
    
    async def _tailor_resume(self, state: Dict) -> str:
        """Tailor resume for specific job"""
        
        profile = state.get("user_profile", {})
        
        prompt = f"""Create ATS-optimized resume sections based on this profile:
        
        {json.dumps(profile)}
        
        Focus on:
        1. Strong action verbs
        2. Quantified achievements
        3. Relevant keywords
        
        Provide bullet points for experience section."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return f"## Optimized Resume Content\n\n{response.content}"
    
    async def _generate_cover_letter(self, state: Dict) -> str:
        """Generate personalized cover letter"""
        
        profile = state.get("user_profile", {})
        
        prompt = f"""Write a compelling cover letter for:
        
        Candidate: {json.dumps(profile)}
        
        Make it:
        - Specific and personal
        - Achievement-focused
        - Under 400 words
        
        Return the cover letter text."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return f"## Your Cover Letter\n\n{response.content}"
    
    async def _general_application_advice(self, state: Dict) -> str:
        return "I can help you with resume tailoring and cover letter writing. What would you like to work on?"

