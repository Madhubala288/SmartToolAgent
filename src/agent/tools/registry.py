from agent.tools.calculator import calculator
from agent.tools.weather import get_weather
from agent.tools.notes import add_note, list_notes


TOOL_REGISTRY = {
    "calculator": calculator,
    "get_weather": get_weather,
    "add_note": add_note,
    "list_notes": list_notes,
}