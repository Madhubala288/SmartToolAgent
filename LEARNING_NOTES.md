\# SmartToolAgent — Learning Notes



\## 1. Workflow vs Agent



\*\*Workflow:\*\* A predefined sequence of steps controlled by program logic.



\*\*Agent:\*\* An LLM-driven system that chooses tools dynamically based on the user's request and the results returned by those tools.



\## 2. Gemini OpenAI-Compatible API



The project uses an OpenAI-compatible client to communicate with the configured LLM provider. Supported functionality depends on the provider and model. Tool calling and structured JSON output should be tested with the selected model.



\## 3. ReAct Agent Loop



\- \*\*Reason:\*\* Interpret the user's request and decide which action is needed.

\- \*\*Act:\*\* Request a tool call from the model.

\- \*\*Observe:\*\* Execute the tool and return its result to the model.

\- \*\*Repeat:\*\* Continue until a final answer is generated or the step limit is reached.

\- \*\*Validate:\*\* Parse the final JSON response with Pydantic and retry once if validation fails.



\## 4. System Prompt Comparison



Three system prompts should be tested using the same request and model. Record actual outputs instead of assuming which prompt performs best.




| Prompt | Purpose | Actual Output | Correct Tool Selection? | Valid JSON? | Response Time |
|---|---|---|---|---|---|
| Minimal | Short, general instructions | Answer 400; JSON wrapped in Markdown fences; tool name reported as default_api:calculator | Yes | No | 6.82 seconds |
| Strict Tool Execution | Emphasizes tool use and structured responses | Answer 400; JSON wrapped in Markdown fences; tool name reported as default_api:calculator | Yes | No | 12.62 seconds |
| Verbose Instructions | Provides detailed instructions | Answer 400; valid AnswerSummary JSON; calculator listed correctly | Yes | Yes | 9.08 seconds |
\## 5. Experiment Procedure



1\. Select one request that requires a tool, such as `What is 25 multiplied by 16?`

2\. Run the same request with each of the three prompts.

3\. Keep the model and other settings the same.

4\. Record the complete final output, tools called, JSON validity, and elapsed time.

5\. Compare correctness, tool selection, response structure, and latency.



\## 6. Key Learning



System prompts influence how an LLM interprets instructions and selects tools. However, prompt quality should be evaluated through repeatable experiments rather than assumptions. Tool execution, error handling, and Pydantic validation help make an agent more reliable.



\## 7. Limitations



\- Weather tools depend on external service availability and network access.

\- LLM responses may vary between runs.

\- Response time and token usage depend on the selected provider and model.

\- The prompt comparison remains incomplete until the experiments and measurements are recorded.



