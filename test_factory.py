from src.agents.factory import ModelClientFactory

factory = ModelClientFactory()

print("Available strategies:", factory.get_available_strategies())

creative_client = factory.create_client("creative")
technical_client = factory.create_client("technical")
efficient_client = factory.create_client("efficient")

print("Creative client:", type(creative_client))
print("Technical client:", type(technical_client))
print("Efficient client:", type(efficient_client))

try:
    bad_client = factory.create_client("nonexistent")
except ValueError as e:
    print("Error handled correctly:", e)

factory.add_strategy("experimental", "gpt-4o", 1.5)
experimental_client = factory.create_client("experimental")
print("Experimental client:", type(experimental_client))

custom_client = factory.create_custom_client("gpt-4o-mini", 0.5)
print("Custom client:", type(custom_client))
