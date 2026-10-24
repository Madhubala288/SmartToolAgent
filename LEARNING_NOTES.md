# SmartToolAgent — Learning Notes

## 1. Workflow vs Agent

**Workflow:** A predefined sequence of steps controlled by program logic.

**Agent:** An LLM-driven system that chooses tools dynamically based on the user's request and the results returned by those tools.

## 2. Gemini OpenAI-Compatible API

The project uses an OpenAI-compatible client to communicate with the configured LLM provider. Supported functionality depends on the provider and model. Tool calling and structured JSON output should be tested with the selected model.

## 3. ReAct Agent Loop

- **Reason:** Interpret the user's request and decide which action is needed.
- **Act:** Request a tool call from the model.
- **Observe:** Execute the tool and return its result to the model.
- **Repeat:** Continue until a final answer is generated or the step limit is reached.
- **Validate:** Parse the final JSON response with Pydantic and retry once if validation fails.

## 4. System Prompt Comparison

Three system prompts should be tested using the same request and model. Record actual outputs instead of assuming which prompt performs best.

| Prompt | Purpose | Actual Output | Correct Tool Selection? | Valid JSON? | Response Time |
|---|---|---|---|---|---|
| Minimal | Short, general instructions | Answer 400; JSON wrapped in Markdown fences; tool name reported as default_api:calculator | Yes | No | 6.82 seconds |
| Strict Tool Execution | Emphasizes tool use and structured responses | Answer 400; JSON wrapped in Markdown fences; tool name reported as default_api:calculator | Yes | No | 12.62 seconds |
| Verbose Instructions | Provides detailed instructions | Answer 400; valid AnswerSummary JSON; calculator listed correctly | Yes | Yes | 9.08 seconds |

## 5. Experiment Procedure

1. Select one request that requires a tool, such as `What is 25 multiplied by 16?`
2. Run the same request with each of the three prompts.
3. Keep the model and other settings the same.
4. Record the complete final output, tools called, JSON validity, and elapsed time.
5. Compare correctness, tool selection, response structure, and latency.

## 6. Key Learning

System prompts influence how an LLM interprets instructions and selects tools. However, prompt quality should be evaluated through repeatable experiments rather than assumptions. Tool execution, error handling, and Pydantic validation help make an agent more reliable.

## 7. Limitations

- Weather tools depend on external service availability and network access.
- LLM responses may vary between runs.
- Response time and token usage depend on the selected provider and model.

---

## Task 3: Gemini Compatibility

**Important finding:** API compatibility does not guarantee that every parameter behaves identically[cite: 10].

| Parameter | What to document |
|---|---|
| `messages` | Chat conversation input[cite: 11] |
| `tools` | Tool/function definitions[cite: 11] |
| `tool_choice` | Whether and how tools are selected[cite: 11] |
| `temperature` | Controls sampling randomness; support may vary[cite: 11] |
| `max_tokens` | Output-length limit; provider-specific behavior may differ[cite: 11] |
| `response_format` | Requests structured output or JSON where supported[cite: 11] |

Gemini's OpenAI-compatible endpoint and Ollama's OpenAI-compatible endpoint can differ in supported options and behavior. Record what you actually tested rather than claiming every parameter works identically[cite: 11].

---

## Building Effective Agents

An effective AI agent is more than an LLM that generates a response. It combines a language model with instructions, tools, a control loop, and mechanisms for handling errors[cite: 12]. The system prompt defines the agent's role, rules, tool-use behavior, and required output format[cite: 12]. Clear instructions and short examples help the model produce more consistent results[cite: 12].

The agent loop enables the model to decide whether it needs a tool, generate the required arguments, execute the tool, and inspect its result[cite: 12]. The result is then returned to the model so it can continue working or provide a final answer[cite: 12]. A step limit prevents endless loops, while argument validation and exception handling help the system recover from invalid requests and tool failures[cite: 12].

Structured output is another important part of reliable agent design[cite: 12]. In SmartToolAgent, Pydantic validation checks that the final response contains the expected answer, tools_used, and confidence fields[cite: 12]. A retry can help recover from invalid output, but a well-designed system prompt should reduce unnecessary retries[cite: 12].

Agents should also be evaluated through realistic test cases, including successful tool calls, multiple-tool tasks, malformed inputs, and failures[cite: 12]. Logging actual results, tool usage, response validity, and execution time makes it easier to compare prompt designs and identify weaknesses[cite: 12].

Overall, effective agents require a balance of clear instructions, reliable tools, controlled execution, validation, error recovery, and systematic evaluation[cite: 13]. A successful agent should not only produce a useful answer but also behave predictably when a tool or model fails[cite: 13].