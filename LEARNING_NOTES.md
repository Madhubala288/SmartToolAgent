1. Workflow vs Agent
Workflow: A hardcoded sequence of deterministic steps where execution follows a strict predefined path. Decision-making is explicit and coded via conditional statements.

Agent: An autonomous LLM-driven entity that dynamically decides which actions/tools to call based on the user request, context, and environment responses.

2. Gemini OpenAI Compatibility
Supported Parameters: messages, tools, tool_choice, temperature, max_tokens, response_format.

Limitations: Slight differences in tool call format handling, token counting variations, and strict adherence to specific Pydantic JSON schemas compared to native OpenAI models.

3. ReAct (Reason, Act, Observe) Cycle
Reason: The model analyzes user intent and decides what tool or information is required.

Act: The model outputs a tool call request with precise parameters.

Observe: The agent executes the requested tool (e.g., SQLite lookup, API fetch) and feeds the output back into the conversation context.

Repeat / Answer: The cycle continues until the model has sufficient information to return the final answer.

4. System Prompts Comparison
Prompt A (Minimal): Fast response, but lacks structured formatting or proper confidence scoring.

Prompt B (Strict Tool Execution): Accurately invokes tools when needed, returns rigid structured JSON output validated via Pydantic.

Prompt C (Verbose Reasoning): High transparency in step-by-step reasoning, slightly slower performance due to longer output tokens.