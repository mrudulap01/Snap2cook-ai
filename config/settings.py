import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    @property
    def OPENROUTER_API_KEY(self) -> str:
        # Check Streamlit Secrets first (for Cloud Deployment)
        try:
            import streamlit as st
            if "OPENROUTER_API_KEY" in st.secrets:
                return st.secrets["OPENROUTER_API_KEY"]
        except Exception:
            pass
            
        # Fallback to local .env
        return os.getenv("OPENROUTER_API_KEY") or os.getenv("GEMINI_API_KEY", "")

    @property
    def LOG_LEVEL(self) -> str:
        return os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
