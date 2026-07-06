import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    @property
    def OPENROUTER_API_KEY(self) -> str:
        key = None
        
        # 1. Try Streamlit Secrets
        try:
            import streamlit as st
            key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass
            
        # 2. Try os.environ
        if not key:
            key = os.getenv("OPENROUTER_API_KEY") or os.getenv("GEMINI_API_KEY")
            
        # 3. Strip quotes if any (common copy-paste error)
        if key:
            key = key.strip().strip('\"').strip('\'')
            
        if not key:
            raise ValueError("API Key is completely missing from both st.secrets and os.environ. Please check Streamlit Secrets configuration.")
            
        return key

    @property
    def LOG_LEVEL(self) -> str:
        return os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
