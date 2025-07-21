# app/config.py
from pydantic_settings import BaseSettings
from pydantic import Field


from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB connection string
    MONGO_URI: str = Field(default="mongodb://localhost:27017")

    # Database name (default fallback)
    MONGO_DB_NAME: str = Field(default="ingredient_ai")

    # OpenAI or other LLM API key (optional use)
    OPENAI_API_KEY: str | None = Field(default=None, alias="OPENAI_API_KEY")

    # Any additional config
    DEBUG: bool = Field(default=True)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Use caching to prevent reloading on every import
@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Singleton-style access
settings = get_settings()
