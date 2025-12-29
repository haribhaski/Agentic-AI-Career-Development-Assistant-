from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    groq_api_key: str
    deepseek_api_key: str
    gemini_api_key: str
    
    # Database
    supabase_url: str
    supabase_key: str
    redis_url: str = "redis://localhost:6379"
    
    # Search
    serper_api_key: str
    brave_api_key: str
    
    # Security
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
