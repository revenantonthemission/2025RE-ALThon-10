import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Course Simulator"
    PROJECT_VERSION: str = "1.0.0"
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/course_db")

settings = Settings()
