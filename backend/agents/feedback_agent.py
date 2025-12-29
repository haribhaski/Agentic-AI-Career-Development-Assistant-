from typing import Dict, List
from langchain_core.messages import HumanMessage

class FeedbackAgent:
    """Learns from outcomes, adapts strategy"""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def process(self, state: Dict) -> Dict:
        """Analyze feedback and adapt strategy"""
        
        messages = state.get("messages", [])
        last_message = messages[-1].content if messages else ""
        
        # Analyze rejection patterns
        analysis = await self._analyze_rejection(last_message, state)
        
        # Suggest improvements
        suggestions = await self._generate_improvements(analysis)
        
        response = f"""## Feedback Analysis

{analysis}

### Recommendations
{suggestions}

Remember: Every rejection is a learning opportunity! 💪"""
        
        state["final_response"] = response
        state["next_agent"] = "end"
        
        return state
    
    async def _analyze_rejection(self, feedback: str, state: Dict) -> str:
        """Analyze rejection feedback"""
        
        prompt = f"""Analyze this application feedback:
        
        {feedback}
        
        Identify:
        1. Specific reasons for rejection
        2. Skills that were missing
        3. Areas to improve
        
        Be constructive and specific."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content
    
    async def _generate_improvements(self, analysis: str) -> str:
        """Generate actionable improvements"""
        
        prompt = f"""Based on this analysis: {analysis}
        
        Provide 3 specific, actionable steps to improve.
        
        Make them concrete and achievable."""
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return response.content