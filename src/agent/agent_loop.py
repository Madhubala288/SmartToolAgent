import json
import logging

from agent.config import client, GEMINI_MODEL
from agent.models import AnswerSummary
from agent.prompts import SYSTEM_PROMPT
from schemas.tools import TOOL_SCHEMAS
from agent.tools.registry import TOOL_REGISTRY


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


MAX_STEPS = 5


def execute_tool(tool_name: str, arguments: dict):
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool_function = TOOL_REGISTRY[tool_name]

    logger.info(
        "Executing tool=%s arguments=%s",
        tool_name,
        arguments,
    )

    return tool_function(**arguments)


def run_agent(user_question: str) -> AnswerSummary:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_question,
        },
    ]

    tools_used = []

    for step in range(1, MAX_STEPS + 1):

        logger.info("Agent step %d", step)

        try:
            response = client.chat.completions.create(
                model=GEMINI_MODEL,
                messages=messages,
                tools=TOOL_SCHEMAS,
            )

        except Exception as error:
            logger.error("LLM request failed: %s", error)

            if "429" in str(error):
                return AnswerSummary(
                    answer=(
                        "Gemini API quota has been exceeded. "
                        "Please wait for the quota to reset "
                        "or use another available API model."
                    ),
                    tools_used=tools_used,
                    confidence=0.0,
                )

            raise

        message = response.choices[0].message

        # -------------------------------------------------
        # TOOL CALL
        # -------------------------------------------------
        if message.tool_calls:

            messages.append(message)

            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name

                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    result = execute_tool(
                        tool_name,
                        arguments,
                    )

                    tools_used.append(tool_name)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(
                                result,
                                default=str,
                            ),
                        }
                    )

                except Exception as error:

                    logger.exception(
                        "Tool execution failed."
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(
                                {
                                    "error": str(error)
                                }
                            ),
                        }
                    )

            continue

        # -------------------------------------------------
        # FINAL ANSWER
        # -------------------------------------------------
        final_text = message.content or ""

        return AnswerSummary(
            answer=final_text,
            tools_used=tools_used,
            confidence=1.0 if tools_used else 0.8,
        )

    raise RuntimeError(
        f"Agent exceeded maximum step limit ({MAX_STEPS})."
    )