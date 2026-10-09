import inspect
from typing import Any, Callable, Dict, List
from agent.tools import calculator, get_weather, add_note, list_notes


def function_to_schema(func: Callable) -> Dict[str, Any]:
    """
    Generates an OpenAI/Gemini compatible JSON schema automatically
    from a Python function's signature and docstring.
    """
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or ""

    properties = {}
    required = []

    for name, param in sig.parameters.items():
        # Determine param type from type hints
        param_type = "string"
        if param.annotation in (int, float):
            param_type = "number"
        elif param.annotation == bool:
            param_type = "boolean"

        properties[name] = {
            "type": param_type,
            "description": f"Parameter {name}"
        }

        # If parameter has no default value, mark it as required
        if param.default == inspect.Parameter.empty:
            required.append(name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": doc.split("\n")[0] if doc else "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }


# Automatically generate tool schemas from function docstrings & signatures
TOOLS_SCHEMA: List[Dict[str, Any]] = [
    function_to_schema(calculator),
    function_to_schema(get_weather),
    function_to_schema(add_note),
    function_to_schema(list_notes),
]