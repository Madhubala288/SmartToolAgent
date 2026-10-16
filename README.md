# SmartToolAgent — Custom ReAct AI Agent Framework

SmartToolAgent is a terminal-based AI agent built with Python. It follows a custom **Reason–Act–Observe (ReAct)** loop, selects tools using LLM tool calling, executes Python functions, observes tool results, and returns structured responses validated with Pydantic.

## Features

- **Custom agent loop:** Runs a tool-calling cycle with a configurable maximum step limit.
- **Calculator:** Evaluates mathematical expressions with operation and result-size limits.
- **Weather:** Retrieves weather information using the configured weather tool.
- **SQLite notes:** Saves and retrieves notes.
- **Dynamic tool schemas:** Generates function schemas from Python function signatures.
- **Structured output:** Validates final responses using Pydantic's `AnswerSummary` model and retries once if JSON validation fails.
- **Error handling:** Handles tool failures and LLM request errors without unnecessarily crashing the agent.
- **Configurable LLM provider:** Supports Gemini and Ollama through environment variables.

## Architecture

```mermaid
flowchart TD
    A[User Question] --> B[Agent Loop]
    B --> C[LLM and Tool Selection]
    C --> D{Tool Requested?}
    D -- Yes --> E[Validate Arguments and Execute Tool]
    E --> F[Tool Result or Error]
    F --> G[Add Result to Conversation]
    G --> B
    D -- No --> H[Validate Final JSON with Pydantic]
    H --> I{Valid JSON?}
    I -- No --> J[Retry Formatting Once]
    J --> H
    I -- Yes --> K[Return AnswerSummary]
```

## Technology Stack

- Python 3.13+
- `uv` for dependency and environment management
- OpenAI-compatible Python client
- Gemini API or Ollama
- Pydantic for data validation
- SQLite for persistent notes
- Open-Meteo weather service (if enabled by the weather tool)

## Prerequisites

- Python 3.13 or a compatible version allowed by `pyproject.toml`
- `uv`
- A Gemini API key, or a locally running Ollama server and a compatible model
- Internet access for hosted LLM and weather requests

Install `uv` using its official installation instructions: https://docs.astral.sh/uv/getting-started/installation/

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Madhubala288/SmartToolAgent
cd SmartToolAgent
```

Replace `YOUR_REPOSITORY_URL` with the actual Git repository URL.

### 2. Install dependencies

```bash
uv sync --locked
```

This uses `pyproject.toml` and `uv.lock` to install the project dependencies. If the lock file needs to be regenerated after changing dependencies, run `uv lock` and commit the updated `uv.lock`.

### 3. Configure environment variables

Create a local environment file from the example.

**Windows Command Prompt:**

```cmd
copy .env.example .env
```

**macOS/Linux:**

```bash
cp .env.example .env
```

Open `.env` and configure the provider and model you want to use.

### Gemini configuration

```dotenv
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.5-flash-lite
LLM_API_KEY=your_gemini_api_key
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

Use a valid model available to your API account. Model availability and quota can change.

### Ollama configuration

First install Ollama and pull a model that supports the required tool-calling features. Start the Ollama server before running the agent.

```dotenv
LLM_PROVIDER=ollama
LLM_MODEL=your_installed_ollama_model
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
```

Replace `your_installed_ollama_model` with the exact model name available in your Ollama installation. Compatibility depends on the model and Ollama version.

## Running the Agent

From the project root, run:

```bash
uv run python main.py
```

Enter a question at the prompt. Type `exit` to quit.

Example questions:

```text
What is 25 times 5?
Calculate 10 modulo 3.
Save a note saying review the agent loop.
List my saved notes.
```

The available weather questions depend on the weather tool's supported arguments.

## Example Output

The following illustrates the response structure; the exact wording may vary.

```json
{
  "answer": "25 times 5 is 125.",
  "tools_used": ["calculator"],
  "confidence": 1.0
}
```

- `answer`: The agent's response.
- `tools_used`: The names of tools invoked, including tools whose execution failed.
- `confidence`: A score between `0.0` and `1.0`.

## Testing

Run the automated tests with:

```bash
uv run pytest
```

If a test makes external API calls, ensure the required service and configuration are available. Prefer mocking external calls in automated tests so the test suite can run without paid API usage or network dependencies.

For manual calculator checks:

```bash
uv run python -c "from agent.tools.calculator import calculator; print(calculator('25*5'))"
uv run python -c "from agent.tools.calculator import calculator; print(calculator('10%3'))"
```

Expected outputs:

```text
125
1
```

To check that large exponentiation is rejected:

```bash
uv run python -c "from agent.tools.calculator import calculator; print(calculator('2**1000000000'))"
```

The command is expected to raise a validation error because the exponent exceeds the configured limit.

## Project Structure

```text
SmartToolAgent/
├── data/
├── src/
│   ├── agent/
│   │   ├── config.py
│   │   ├── agent_loop.py
│   │   ├── models.py
│   │   ├── prompts.py
│   │   └── tools/
│   └── schemas/
├── tests/
├── .env.example
├── .gitignore
├── LEARNING_NOTES.md
├── main.py
├── pyproject.toml
└── uv.lock
```

The structure above summarizes the main components; individual files may vary as development continues.

## Security

- Never commit `.env` or share your API key.
- Keep `.env.example` limited to placeholder values.
- Do not put secrets in source code, logs, screenshots, or public documentation.
- Review tool inputs and errors before adding new tools.

## Limitations

- Hosted model availability, rate limits, and response quality depend on the configured provider.
- Ollama models may differ in tool-calling and JSON-mode support.
- Weather requests require network access.
- The agent has a maximum number of steps to limit repeated tool calls.

## Development Notes

See `LEARNING_NOTES.md` for project learning notes and prompt experiments. See `tests/` for the project's test cases and evaluation questions.

## Execution Evidence

The following scenarios should be run and their actual terminal output recorded before submission.

### Run 1 — Calculator Tool

**Input**
```text
What is 25 times 5?
```

**Expected verification:** The calculator tool is called, the answer is `125`, and the final response contains the required fields.

**Actual output:** 
You: what is 25*5?
2026-10-16 11:19:31,852 | INFO | Agent step 1
2026-10-16 11:19:40,596 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:19:40,647 | INFO | Executing tool=calculator arguments={'expression': '25*5'}
2026-10-16 11:19:40,648 | INFO | Tool calculator executed successfully.
2026-10-16 11:19:40,648 | INFO | Agent step 2
2026-10-16 11:19:42,002 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 503 Service Unavailable"
2026-10-16 11:19:42,004 | INFO | Retrying request in 0.463469 seconds (retry 1 of 2)
2026-10-16 11:19:52,110 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:19:52,121 | WARNING | Final response was not valid AnswerSummary JSON: 1 validation error for AnswerSummary
  Invalid JSON: trailing characters at line 1 column 4 [type=json_invalid, input_value='25 * 5 = 125', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid
2026-10-16 11:19:59,029 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:19:59,061 | INFO | Final JSON validated successfully after retry.

Agent:
{
  "answer": "25 * 5 = 125",
  "tools_used": [
    "calculator"
  ],
  "confidence": 1.0
}

### Run 2 — Multi-Tool Execution

**Input**
```text
Save a note saying test the agent loop, then show my notes.
```

**Expected verification:** The agent calls `add_note` and `list_notes`, and the saved note appears in the result.

**Actual output:** 
You: Save a note saying test the agent loop, then show my notes.
2026-10-16 11:28:44,783 | INFO | Agent step 1
2026-10-16 11:28:49,609 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:28:49,641 | INFO | Executing tool=add_note arguments={'content': 'test the agent loop'}
2026-10-16 11:28:49,695 | INFO | Tool add_note executed successfully.
2026-10-16 11:28:49,697 | INFO | Agent step 2
2026-10-16 11:28:54,019 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:28:54,048 | INFO | Executing tool=list_notes arguments={}
2026-10-16 11:28:54,053 | INFO | Tool list_notes executed successfully.
2026-10-16 11:28:54,053 | INFO | Agent step 3
2026-10-16 11:28:56,189 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 503 Service Unavailable"
2026-10-16 11:28:56,191 | INFO | Retrying request in 0.378892 seconds (retry 1 of 2)
2026-10-16 11:28:57,554 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 503 Service Unavailable"
2026-10-16 11:28:57,557 | INFO | Retrying request in 0.957737 seconds (retry 2 of 2)
2026-10-16 11:29:02,797 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:29:02,801 | WARNING | Final response was not valid AnswerSummary JSON: 1 validation error for AnswerSummary
  Invalid JSON: expected ident at line 1 column 2 [type=json_invalid, input_value='I have successfully save...10. test the agent loop', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid
2026-10-16 11:29:06,716 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:29:06,724 | INFO | Final JSON validated successfully after retry.

Agent:
{
  "answer": "I have successfully saved the note \"test the agent loop\". Here are all your current notes:\n\n1. Learn agent loops\n2. complete smart tool agent setup\n3. complete smart tool agent setup\n4. Complete my Agentic AI assignment\n5. Learn agent loops\n6. Learn agent loops\n7. My project is SmartToolAgent\n8. Learn agent loops\n9. Learn agent loops\n10. test the agent loop",
  "tools_used": [
    "add_note",
    "list_notes"
  ],
  "confidence": 1.0
}


### Run 3 — Error Handling

**Input**
```text
Calculate 2 raised to the power of 1000000000.
```

**Expected verification:** The calculator rejects the excessive exponent, the tool error is handled, and the agent attempts to return a valid final response.

**Actual output:** 
You: Calculate 2 raised to the power of 1000000000.
2026-10-16 11:30:15,261 | INFO | Agent step 1
2026-10-16 11:30:20,326 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:30:20,333 | INFO | Executing tool=calculator arguments={'expression': '2 ** 1000000000'}
2026-10-16 11:30:20,348 | ERROR | Tool execution failed: calculator
Traceback (most recent call last):
  File "D:\laptop data\Agentic AI internship at Dawoodtech NextGen\SmartToolAgent\src\agent\agent_loop.py", line 180, in run_agent
    result = execute_tool(tool_name, arguments)
  File "D:\laptop data\Agentic AI internship at Dawoodtech NextGen\SmartToolAgent\src\agent\agent_loop.py", line 42, in execute_tool
    return tool_function(**arguments)
  File "D:\laptop data\Agentic AI internship at Dawoodtech NextGen\SmartToolAgent\src\agent\tools\calculator.py", line 100, in calculator
    return evaluate(tree)
  File "D:\laptop data\Agentic AI internship at Dawoodtech NextGen\SmartToolAgent\src\agent\tools\calculator.py", line 56, in evaluate
    return evaluate(node.body)
  File "D:\laptop data\Agentic AI internship at Dawoodtech NextGen\SmartToolAgent\src\agent\tools\calculator.py", line 78, in evaluate
    raise ValueError(
        f"Exponent magnitude cannot exceed {MAX_EXPONENT}."
    )
ValueError: Exponent magnitude cannot exceed 1000.
2026-10-16 11:30:20,427 | INFO | Agent step 2
2026-10-16 11:30:25,263 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:30:25,274 | WARNING | Final response was not valid AnswerSummary JSON: 1 validation error for AnswerSummary
  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='The calculator tool retu...f the resulting number.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid
2026-10-16 11:30:29,181 | INFO | HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions "HTTP/1.1 200 OK"
2026-10-16 11:30:29,202 | INFO | Final JSON validated successfully after retry.

Agent:
{
  "answer": "The calculator tool returned an error because the exponent magnitude cannot exceed 1000. Therefore, calculating $2^{1,000,000,000}$ directly is not supported due to the extreme size of the resulting number.",
  "tools_used": [
    "calculator"
  ],
  "confidence": 1.0
}

