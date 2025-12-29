from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from backend.config import get_settings

settings = get_settings()

def get_reasoning_llm():
    """Get DeepSeek R1 for complex reasoning"""
    if settings.deepseek_api_key:
        return ChatOpenAI(
            model_name="deepseek-reasoner",
            openai_api_key=settings.deepseek_api_key,
            openai_api_base="https://api.deepseek.com",
            temperature=0
        )
    # Fallback to Groq if DeepSeek not available
    return get_fast_llm()

def get_fast_llm():
    """Get Groq Llama 3.3 for fast inference"""
    if settings.groq_api_key:
        return ChatGroq(
            model_name="llama-3.3-70b-versatile",
            groq_api_key=settings.groq_api_key,
            temperature=0.1
        )
    # Final fallback to standard ChatOpenAI if configured
    return ChatOpenAI(temperature=0)
