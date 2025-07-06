from typing import List
from autogen_ext.models.openai import OpenAIChatCompletionClient

class ModelClientFactory:
    """
    Factory class for creating model clients.
    """
    models = ["gpt-4o","gpt-4o-mini","gpt-3.5-turbo"]
    strategies = {
        "creative": {
            "model": "gpt-4o",
            "temperature": 0.8
        },
        "technical": {
            "model": "gpt-4o",
            "temperature": 0.1
        },
        "efficient": {
            "model": "gpt-4o-mini",
            "temperature": 0.3
        }
    }
    
    def create_client(self, strategy: str) -> OpenAIChatCompletionClient:
        """
        Create a model client based on the strategy.
        """
        if strategy not in self.strategies:
            raise ValueError(f"Invalid strategy: {strategy}")
        return OpenAIChatCompletionClient(
            model=self.strategies[strategy]["model"], 
            temperature=self.strategies[strategy]["temperature"]
        )
        
    def create_custom_client(self, model: str, temperature: float) -> OpenAIChatCompletionClient:
        """
        Create a custom model client.
        """
        if model not in self.models:
            raise ValueError(f"Invalid model: {model}")
        
        if temperature < 0 or temperature > 2:
            raise ValueError(f"Invalid temperature: {temperature}")
        
        return OpenAIChatCompletionClient(model=model, temperature=temperature)
    
    def get_available_strategies(self) -> List[str]:
        """
        Get the available strategies.
        """
        return list(self.strategies.keys())
    
    def add_strategy(self, strategy: str, model: str, temperature: float) -> None:
        """
        Add a new strategy.
        """
        if strategy in self.strategies:
            raise ValueError(f"Strategy already exists: {strategy}")
        
        if model not in self.models:
            raise ValueError(f"Invalid model: {model}")
        
        if temperature < 0 or temperature > 2:
            raise ValueError(f"Invalid temperature: {temperature}")
        
        self.strategies[strategy] = {
            "model": model,
            "temperature": temperature
        }
    
    def remove_strategy(self, strategy: str) -> None:
        """
        Remove a strategy.
        """
        if strategy not in self.strategies:
            raise ValueError(f"Strategy does not exist: {strategy}")
        del self.strategies[strategy]
    
    def get_strategy(self, strategy: str) -> dict:
        """
        Get a strategy.
        """
        if strategy not in self.strategies:
            raise ValueError(f"Strategy does not exist: {strategy}")
        return self.strategies[strategy]
    
    def get_all_strategies(self) -> dict:
        """
        Get all strategies.
        """
        return self.strategies
    