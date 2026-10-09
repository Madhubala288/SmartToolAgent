from agent.agent_loop import run_agent


def main():
    print("=" * 60)
    print("SmartToolAgent")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            result = run_agent(question)

            print("\nAgent:")
            print(result.model_dump_json(indent=2))

        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()