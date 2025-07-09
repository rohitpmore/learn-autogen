from enum import Enum


operation_enum = Enum("Operation", ["add", "subtract", "multiply", "divide"])

async def calculate(operation: str, a: float, b: float) -> float:
    """
    Calculate the result of a mathematical operation.

    Args:
        operation: The operation to perform. (add, subtract, multiply, divide)
            add: Add two numbers.
            subtract: Subtract the second number from the first.
            multiply: Multiply two numbers.
            divide: Divide the first number by the second.
            If the second number is 0, raise a ValueError.
        a: The first operand.
        b: The second operand.

    Returns:
        The result of the operation.
    """
    if operation.lower() == operation_enum.add.name:
        return a + b
    elif operation.lower() == operation_enum.subtract.name:
        return a - b
    elif operation.lower() == operation_enum.multiply.name:
        return a * b
    elif operation.lower() == operation_enum.divide.name:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError(f"Invalid operation: {operation}")
