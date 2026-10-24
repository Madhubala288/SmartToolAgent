# SmartToolAgent — Learning Notes

## 1. Workflow vs Agent

**Workflow:** A predefined sequence of steps controlled by program logic. The program determines the order of operations in advance.

**Agent:** An LLM-driven system that can select tools dynamically based on the user's request, the available tools, and the results returned by previous actions.

The main difference is that a workflow follows a predefined path, whereas an agent can choose its next action based on the current situation.

## 2. Gemini OpenAI-Compatible API

SmartToolAgent uses an OpenAI-compatible client to communicate with the configured LLM provider. This allows the application to use a common client interface, but it does not guarantee identical behavior across providers.

Tool calling, JSON output, supported parameters, and error handling may vary by provider and model. These features should be verified through actual experiments with the selected model.

The project supports provider configuration through environment variables, allowing Gemini or Ollama to be selected without changing the agent's core implementation.

## 3. ReAct Agent Loop

The ReAct-style agent loop combines reasoning, actions, and observations to complete tasks.

- **Reason:** Interpret the user's request and determine the next action.
- **Act:** Request a tool call from the LLM when a tool is needed.
- **Observe:** Execute the selected tool and return its result to the LLM.
- **Repeat:** Continue the loop until the model generates a final answer or the step limit is reached.
- **Validate:** Validate the final response using Pydantic and retry once if validation fails.

The step limit helps prevent endless loops. Tool argument checks and error handling help the agent respond safely when an operation fails.

## 4. System Prompt Comparison

Three system prompts were compared using the same request and model. The experiment recorded tool selection, output structure, JSON validity, and response time.

| Prompt | Purpose | Observed Output | Correct Tool Selection? | Valid JSON? | Response Time |
|---|---|---|---|---|---:|
| Minimal | Short, general instructions | Answer 400; JSON wrapped in Markdown fences; tool reported as `default_api:calculator` | Yes | No | 6.82 seconds |
| Strict Tool Execution | Emphasizes tool use and structured responses | Answer 400; JSON wrapped in Markdown fences; tool reported as `default_api:calculator` | Yes | No | 12.62 seconds |
| Verbose Instructions | Provides detailed instructions | Answer 400; valid `AnswerSummary` JSON; calculator listed correctly | Yes | Yes | 9.08 seconds |

### Experiment Findings

In these recorded runs, the Minimal and Strict Tool Execution prompts produced JSON wrapped in Markdown fences and did not satisfy the expected output format. The Verbose Instructions prompt produced valid `AnswerSummary` JSON.

The Verbose Instructions prompt was the strongest performer in this particular experiment because its final response matched the required structure. However, one experiment is not enough to prove that it will always perform best.

## 5. Experiment Procedure

1. Select a request that requires a tool, such as `What is 25 multiplied by 16?`.
2. Run the same request with each of the three prompts.
3. Keep the model and other settings consistent.
4. Record the final output, tools called, JSON validity, and elapsed time.
5. Compare correctness, tool selection, response structure, and latency.
6. Repeat the experiments when possible to determine whether the results are consistent.

## 6. Key Learning

System prompts influence how an LLM interprets instructions, selects tools, and formats its final response. Clear rules and examples can improve consistency, but prompt quality should be evaluated through repeatable experiments rather than assumptions.

Reliable agent design also requires more than a good prompt. Tool execution, argument validation, error handling, step limits, and structured output validation help make the application more predictable.

## 7. Limitations

- Weather tools depend on external service availability and network access.
- LLM responses may vary between runs.
- Response time and token usage depend on the selected provider, model, and request.
- OpenAI-compatible endpoints may differ in supported parameters and tool-calling behavior.
- Pydantic validation checks the response structure, but valid JSON does not necessarily mean that the answer is factually correct.

---

## 8. Task 3: Gemini Compatibility

**Important finding:** API compatibility does not guarantee that every parameter behaves identically across providers, models, or endpoints.

| Parameter | Purpose | Compatibility Considerations |
|---|---|---|
| `messages` | Supplies conversation messages to the model | Message formats and supported roles may vary by endpoint. |
| `tools` | Defines available tools or functions | Tool schemas and supported calling behavior may differ. |
| `tool_choice` | Controls whether or how tools are selected | Supported values and model behavior may vary. |
| `temperature` | Controls sampling randomness | Accepted ranges and model-specific behavior may differ. |
| `max_tokens` | Limits generated output length | Limits and parameter support depend on the provider and model. |
| `response_format` | Requests a structured response, such as JSON | JSON mode or structured-output support may vary by endpoint and model. |

### Compatibility Testing

SmartToolAgent uses an OpenAI-compatible client interface to communicate with its configured provider. This reduces the need to change the core client code when switching providers, but it does not establish that every parameter is supported identically.

For a reliable compatibility evaluation:

1. Confirm that the parameter is accepted by the selected endpoint.
2. Run a minimal request using the parameter.
3. Record whether the request succeeds and whether the output matches expectations.
4. Document any unsupported options, errors, or differences in behavior.

The parameter descriptions above explain their intended purposes and possible compatibility considerations. They should not be interpreted as proof that every parameter was individually tested against both Gemini and Ollama.

---

## 9. Building Effective Agents

An effective AI agent is more than a language model that generates text. It combines an LLM with clear instructions, tools, a control loop, and mechanisms for handling errors. The system prompt establishes the agent's role, behavior, tool-use rules, and expected output format. Clear instructions and short examples help guide the model toward consistent responses.

The agent loop allows the model to determine whether a tool is required, generate the appropriate arguments, execute the tool, and examine the returned result. That observation is passed back to the model so it can decide whether another action is needed or whether it can provide a final answer. A step limit prevents unbounded execution, while argument validation and exception handling help manage invalid requests and tool failures.

Structured output is another important part of reliable agent design. In SmartToolAgent, Pydantic validation checks whether the final response follows the expected `AnswerSummary` structure, including `answer`, `tools_used`, and `confidence`. If validation fails, a retry can help recover from malformed output. However, retries should act as a fallback rather than compensate for unclear prompt instructions.

Agent evaluation should include realistic cases such as successful single-tool calls, multiple-tool tasks, invalid inputs, oversized calculations, and external service failures. Recording actual tool usage, output validity, correctness, and response time makes it possible to compare prompt designs and identify weaknesses. Tests should also distinguish application failures from network or provider failures.

Overall, effective agents require a balance of clear instructions, appropriate tool selection, reliable execution, controlled loops, validation, error recovery, and systematic evaluation. A successful agent should not only generate a useful answer but also handle unexpected situations predictably. SmartToolAgent applies these principles through its configurable LLM provider, tool registry, agent loop, calculator safeguards, and Pydantic-based final response validation.