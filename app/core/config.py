#app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document RAG System"
    SECRET_KEY: str = "#&236#HBGTS"  
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/assignment"

    class Config:
        env_file = ".env"

settings = Settings()