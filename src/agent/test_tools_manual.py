
from agent.tools.calculator import calculator
from agent.tools.weather import get_weather
from agent.tools.notes import add_note, list_notes


def main():
    print("CALCULATOR")
    print(calculator("25 * 4"))

    print("\nWEATHER")
    try:
        print(get_weather(24.8607, 67.0011))
    except Exception as exc:
        print(f"Weather test failed: {exc}")

    print("\nNOTES")
    print(add_note("Learn agent loops"))
    print(list_notes())


if __name__ == "__main__":
    main()
