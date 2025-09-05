from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Gemini API Configuration
    gemini_api_key: str = "demo_key_for_testing"
    
    # Appwrite Configuration
    appwrite_project_id: str = "demo_project"
    appwrite_api_key: str = "demo_api_key"
    appwrite_endpoint: str = "https://cloud.appwrite.io/v1"
    appwrite_database_id: str = "main"
    appwrite_conversations_collection_id: str = "conversations"
    appwrite_messages_collection_id: str = "messages"
    
    # Application Configuration
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()