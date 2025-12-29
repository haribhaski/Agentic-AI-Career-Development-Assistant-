from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    groq_api_key: str = ""
    deepseek_api_key: str = ""
    gemini_api_key: str = ""
    serper_api_key: str = ""
    firecrawl_api_key: str = ""
    nomic_api_key: str = ""
    
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    
    # JWT
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Missing fields from .env
    brave_api_key: str = ""
    llama_cloud_api_key: str = ""
    access_token_expire_minutes: int = 30
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
