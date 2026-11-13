import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ReportSaathi Core Engine"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./reportsaathi_system.db")
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
