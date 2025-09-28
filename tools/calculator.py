def calculator(expression: str):
    """
    Evaluate a mathematical expression safely.

    Args:
        expression (str): The mathematical expression to evaluate.
                          Example: "2 + 3 * 4"

    Returns:
        float | None: The result of the evaluated expression, or None if invalid.
    """
    try:
        # Use restricted eval environment
        result = eval(expression, {"__builtins__": {}})
        return float(result)
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None
