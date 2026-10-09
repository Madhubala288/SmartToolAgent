from agent.config import client, GEMINI_MODEL
def main():
    response = client.chat.completions.create(
        model=GEMINI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant.",
            },
            {
                "role": "user",
                "content": "Explain what an AI agent is in two sentences.",
            },
        ],
    )
    print(response.choices[0].message.content)
if __name__ == "__main__":
    main()