from src.agents.factory import ModelClientFactory
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

class AgentBuilder:
    """
    Builder class for creating agents.
    """
    model_factory: ModelClientFactory
    
    def __init__(self, model_factory: ModelClientFactory):
        self.model_factory = model_factory

    def create_agent(self, name: str, strategy: str, system_message: str, tools: list = None) -> AssistantAgent:
        """
        Create an agent with a given strategy.
        """
        if strategy not in self.model_factory.get_available_strategies():
            raise ValueError(f"Invalid strategy: {strategy}")
        
        if name is None:
            raise ValueError("Name is required")
        
        model_client = self.model_factory.create_client(strategy)
        
        if system_message is None:
            system_message =  f"You are a helpful assistant. You are able to answer questions and help with tasks with strategy: {strategy}"
        
        return AssistantAgent(name=name, model_client=model_client, system_message=system_message, tools=tools)
    
    def create_custom_agent(self, name: str, model_client: OpenAIChatCompletionClient, system_message: str, tools: list = None) -> AssistantAgent:
        """
        Create a custom agent with a given model client.
        """
        if name is None:
            raise ValueError("Name is required")
        
        if model_client is None:
            raise ValueError("Model client is required")
        
        if system_message is None:
            system_message = "You are a helpful assistant. You are able to answer questions and help with tasks."
        
        return AssistantAgent(name=name, model_client=model_client, system_message=system_message, tools=tools)
    
