"""
Utility functions for Jupyter notebooks.
Provides common setup and helper functions for learning exercises.
"""
import sys
import os
from pathlib import Path
from typing import Optional

# Add src to path for imports
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


def setup_notebook_environment() -> None:
    """
    Set up the notebook environment with proper imports and configuration.
    Call this at the beginning of each notebook.
    """
    # Ensure src is in path
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    # Check if configuration is available
    try:
        from config.settings import is_configured
        if not is_configured():
            print("⚠️  Configuration not found. Please:")
            print("   1. Copy .env.example to .env")
            print("   2. Add your OpenAI API key")
            print("   3. Restart the notebook kernel")
    except ImportError:
        print("⚠️  Configuration module not available")


def print_lesson_header(lesson_name: str, description: str) -> None:
    """Print a formatted lesson header."""
    print("=" * 60)
    print(f"📚 {lesson_name}")
    print("-" * 60)
    print(f"📝 {description}")
    print("=" * 60)
    print()


def print_section_header(section_name: str) -> None:
    """Print a formatted section header."""
    print(f"\n🔧 {section_name}")
    print("-" * 40)


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✅ {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ️  {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"⚠️  {message}")


def check_requirements() -> bool:
    """Check if required packages are installed."""
    try:
        import autogen_agentchat
        import autogen_ext
        import openai
        print_success("All required packages are installed!")
        return True
    except ImportError as e:
        print_warning(f"Missing required package: {e}")
        print_info("Run: uv add autogen-agentchat autogen-ext[openai]")
        return False


def create_test_model_client():
    """Create a test model client for notebook examples."""
    try:
        from config.settings import get_settings
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        
        settings = get_settings()
        if not settings.validate():
            print_warning("OpenAI API key not configured")
            return None
        
        client = OpenAIChatCompletionClient(
            model=settings.openai_model,
            api_key=settings.openai_api_key
        )
        print_success(f"Created model client: {settings.openai_model}")
        return client
    except Exception as e:
        print_warning(f"Could not create model client: {e}")
        return None


def display_agent_info(agent) -> None:
    """Display information about an agent."""
    print(f"Agent Name: {agent.name}")
    print(f"Agent Type: {type(agent).__name__}")
    if hasattr(agent, 'system_message'):
        print(f"System Message: {agent.system_message[:100]}...")
    print()


# Convenience imports for notebooks
def notebook_imports():
    """Import commonly used modules for notebooks."""
    import asyncio
    import json
    from typing import Dict, List, Optional, Any
    
    # Make available in notebook namespace
    globals().update({
        'asyncio': asyncio,
        'json': json,
        'Dict': Dict,
        'List': List,
        'Optional': Optional,
        'Any': Any
    })