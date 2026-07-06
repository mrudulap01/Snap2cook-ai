import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    # Use GEMINI_API_KEY as a fallback if OPENROUTER_API_KEY is not set, 
    # since the user previously set GEMINI_API_KEY in their .env
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY") or os.getenv("GEMINI_API_KEY", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
