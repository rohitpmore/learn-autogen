import asyncio
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up environment (assuming .env is in project root)
if 'OPENAI_API_KEY' not in os.environ:
    print("Warning: OPENAI_API_KEY not found in environment variables")

from src.agents.factory import ModelClientFactory
from src.agents.builder import AgentBuilder
from src.tools.calculator import calculate

async def main():
    factory = ModelClientFactory()
    builder = AgentBuilder(factory)
    
    math_agent = builder.create_agent(
        name="math_agent",
        strategy="technical",
        system_message="You are a math agent. Use the calculator tool for precise calculations.",
        tools=[calculate]
    )
    
    result = await math_agent.run(task="Calculate 25*4 + 10")
    
    print("Full conversation:")
    for msg in result.messages:
        print(f"{msg.source}: {msg.content}")
        print("-" * 50)
    
if __name__ == "__main__":
    asyncio.run(main())