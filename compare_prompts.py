
import json
import time

from pydantic import ValidationError
from agent.config import client, GEMINI_MODEL
from agent.models import AnswerSummary
from schemas.tools import TOOL_SCHEMAS
from agent.tools.registry import TOOL_REGISTRY

QUESTION = "What is 25 multiplied by 16?"

PROMPTS = {
    "Minimal": (
        "You are a helpful assistant. Use tools when needed. "
        "Return JSON with answer, tools_used, and confidence."
    ),
    "Strict Tool Execution": """
You are a tool-using assistant.
For mathematical calculations, you MUST use the calculator tool.
Do not calculate mentally. Use the actual tool result.
Return only JSON with answer (string), tools_used (array of strings),
and confidence (number between 0 and 1).
""",
    "Verbose Instructions": """
You are SmartToolAgent, an accurate tool-using assistant.
Read the request carefully. For mathematical questions, select the
calculator tool and pass the correct expression.
Execute the tool, use its actual result, and never invent results.
Return only valid JSON with answer (string), tools_used (array of strings),
and confidence (number between 0 and 1). No Markdown fences.
"""
}

for name, prompt in PROMPTS.items():
    print("\n" + "=" * 60)
    print("PROMPT:", name)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": QUESTION},
    ]
    tools_used = []
    start = time.perf_counter()

    try:
        final_text = ""

        for step in range(5):
            response = client.chat.completions.create(
                model=GEMINI_MODEL,
                messages=messages,
                tools=TOOL_SCHEMAS,
            )

            message = response.choices[0].message

            if not message.tool_calls:
                final_text = message.content or ""
                break

            messages.append(message)

            for call in message.tool_calls:
                tool_name = call.function.name
                tools_used.append(tool_name)

                arguments = json.loads(call.function.arguments or "{}")

                if tool_name not in TOOL_REGISTRY:
                    result = {"error": f"Unknown tool: {tool_name}"}
                else:
                    try:
                        result = TOOL_REGISTRY[tool_name](**arguments)
                    except Exception as error:
                        result = {"error": str(error)}

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, default=str),
                })

        elapsed = time.perf_counter() - start
        print("Executed tools:", tools_used)
        print("Total response time:", round(elapsed, 2), "seconds")

        try:
            parsed = AnswerSummary.model_validate_json(final_text)
            print("Valid AnswerSummary JSON: Yes")
            print(parsed.model_dump_json(indent=2))
        except (ValidationError, ValueError, TypeError):
            print("Valid AnswerSummary JSON: No")
            print("Raw final output:", final_text or "(empty)")
    except Exception as error:
        print("ERROR:", str(error))

