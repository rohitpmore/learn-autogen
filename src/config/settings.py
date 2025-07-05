"""
Configuration management for AutoGen learning project.
Handles environment variables and application settings.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # OpenAI Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        
        # Application Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        
        # Agent Configuration
        self.default_agent_timeout = int(os.getenv("DEFAULT_AGENT_TIMEOUT", "30"))
        self.max_turns = int(os.getenv("MAX_TURNS", "10"))
        
        # Testing Configuration
        self.test_timeout = int(os.getenv("TEST_TIMEOUT", "5"))
        self.mock_responses = os.getenv("MOCK_RESPONSES", "True").lower() == "true"
    
    def validate(self) -> bool:
        """Validate required configuration."""
        if not self.openai_api_key:
            return False
        return True


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def is_configured() -> bool:
    """Check if the application is properly configured."""
    return get_settings().validate()