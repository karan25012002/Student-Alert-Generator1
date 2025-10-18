from pydantic_settings import BaseSettings
from typing import List
import os

# Production frontend URL for CORS configuration
PRODUCTION_FRONTEND_URL = "https://student-alert-generator1-7.onrender.com"

class Settings(BaseSettings):
    # Database
    MONGODB_URL: str = os.getenv("MONGODB_ATLAS_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "student_tracker")
    
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google Gemini API
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # CORS
    _default_origins = "http://localhost:3000,http://127.0.0.1:3000"
    _env_origins = os.getenv("ALLOWED_ORIGINS", "")
    if _env_origins:
        ALLOWED_ORIGINS: List[str] = _env_origins.split(",")
    else:
        ALLOWED_ORIGINS: List[str] = _default_origins.split(",")
    
    # Always include production frontend URL for Render deployment
    if PRODUCTION_FRONTEND_URL not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(PRODUCTION_FRONTEND_URL)
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
