import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    @property
    def AI_API_KEY(self) -> str:
        key = None
        
        # 1. Try Streamlit Secrets
        try:
            import streamlit as st
            key = (st.secrets.get("OPENROUTER_API_KEY") or 
                   st.secrets.get("AI_API_KEY") or 
                   st.secrets.get("GEMINI_API_KEY") or
                   st.secrets.get("OPENAI_API_KEY"))
        except Exception:
            pass
            
        # 2. Try os.environ
        if not key:
            key = (os.getenv("OPENROUTER_API_KEY") or 
                   os.getenv("AI_API_KEY") or 
                   os.getenv("GEMINI_API_KEY") or
                   os.getenv("OPENAI_API_KEY"))
            
        # 3. Strip quotes if any
        if key:
            key = key.strip().strip('\"').strip('\'')
            
        if not key:
            raise ValueError("AI API Key is completely missing. Please set OPENROUTER_API_KEY or AI_API_KEY in your .env or Streamlit Secrets.")
            
        return key

    @property
    def AI_BASE_URL(self) -> str:
        return os.getenv("OPENROUTER_BASE_URL", os.getenv("AI_BASE_URL", "https://openrouter.ai/api/v1"))

    @property
    def VISION_MODEL(self) -> str:
        return os.getenv("VISION_MODEL", "google/gemini-2.5-flash")

    @property
    def TEXT_MODEL(self) -> str:
        return os.getenv("TEXT_MODEL", "google/gemini-2.5-flash")
        
    @property
    def FALLBACK_VISION_MODEL(self) -> str:
        return os.getenv("FALLBACK_VISION_MODEL", "qwen/qwen-2-vl-72b-instruct")
        
    @property
    def FALLBACK_TEXT_MODEL(self) -> str:
        return os.getenv("FALLBACK_TEXT_MODEL", "meta-llama/llama-3.1-70b-instruct")

    @property
    def TEMPERATURE(self) -> float:
        return float(os.getenv("TEMPERATURE", "0.7"))
        
    @property
    def MAX_TOKENS(self) -> int:
        return int(os.getenv("MAX_TOKENS", "8000"))
        
    @property
    def TOP_P(self) -> float:
        return float(os.getenv("TOP_P", "1.0"))

    @property
    def LOG_LEVEL(self) -> str:
        return os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
