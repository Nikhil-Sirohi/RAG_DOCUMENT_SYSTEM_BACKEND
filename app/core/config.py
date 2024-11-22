#app/core/config.py



from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document RAG System"
    SECRET_KEY: str = "#&236#HBGTS"
    ALGORITHM: str = "HS256"
    OPENAI_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 50
    DATABASE_URL: str = "postgresql://nikhilsirohi:newpassword@localhost:5432/rag"

    class Config:
        env_file = ".env"

settings = Settings()

