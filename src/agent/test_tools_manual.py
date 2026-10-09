from agent.tools.calculator import calculator
from agent.tools.weather import get_weather
from agent.tools.notes import add_note, list_notes
print("CALCULATOR")
print(calculator("25 * 4"))
print("\nWEATHER")
print(get_weather(24.8607, 67.0011))
print("\nNOTES")
print(add_note("Learn agent loops"))
print(list_notes())