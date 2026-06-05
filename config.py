import os
import sys

# Load environment variables from .env file (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, skip

# Get configuration values from environment or Streamlit secrets
def _get_config_value(key, default=''):
    """Get config value from multiple sources with fallbacks"""
    # Try Streamlit secrets first (for Streamlit Cloud)
    try:
        import streamlit as st
        value = st.secrets.get(key)
        if value:
            return value
    except (ImportError, AttributeError, Exception):
        pass
    
    # Fall back to environment variables
    return os.getenv(key, default)


# Load configuration values
GROQ_API_KEY = _get_config_value('GROQ_API_KEY', '')
LLM_PROVIDER = _get_config_value('LLM_PROVIDER', 'groq')
CHROMA_DB_PATH = _get_config_value('CHROMA_DB_PATH', './chroma_db')


class Config:
    """Configuration class for RAG Engine"""
    
    # LLM Configuration
    GROQ_API_KEY = GROQ_API_KEY
    GROQ_MODEL_NAME = 'llama-3.3-70b-versatile'  # Updated from deprecated models
    LLM_PROVIDER = LLM_PROVIDER
    
    # Embedding Configuration
    EMBEDDING_MODEL_NAME = 'BAAI/bge-large-en-v1.5'
    
    # Vector Database Configuration
    CHROMA_DB_PATH = CHROMA_DB_PATH
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        if not cls.GROQ_API_KEY or cls.GROQ_API_KEY == '':
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Please set it in .env (local) or Streamlit Secrets (cloud)"
            )
        if not cls.GROQ_MODEL_NAME:
            raise ValueError("GROQ_MODEL_NAME is not set in config")
        print(f"✓ Config validated - Using model: {cls.GROQ_MODEL_NAME}")
        print(f"✓ Provider: {cls.LLM_PROVIDER}")
