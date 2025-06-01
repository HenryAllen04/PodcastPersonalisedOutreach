# Purpose: Configuration management for PODVOX - handles environment variables and app settings

from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Configuration
    app_name: str = "PODVOX"
    app_version: str = "0.1.0"
    debug: bool = True
    port: int = 8000
    
    # API Keys
    openai_api_key: str
    sieve_api_key: str
    elevenlabs_api_key: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    
    # Sieve Configuration
    sieve_backend: str = "sieve-fast"  # or "sieve-contextual"
    min_clip_length: float = 10.0
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings() 