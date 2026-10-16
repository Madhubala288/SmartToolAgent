
import json
import logging

from pydantic import ValidationError

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


def unique_tools(tools_used: list[str]) -> list[str]:
    """Return tool names without duplicates, preserving order."""
    return list(dict.fromkeys(tools_used))


def execute_tool(tool_name: str, arguments: dict):
    """Execute a registered tool using the supplied arguments."""
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool_function = TOOL_REGISTRY[tool_name]

    logger.info(
        "Executing tool=%s arguments=%s",
        tool_name,
        arguments,
    )

    return tool_function(**arguments)


def parse_final_answer(
    final_text: str,
    tools_used: list[str],
) -> AnswerSummary:
    """Validate final JSON and retry once if validation fails."""
    recorded_tools = unique_tools(tools_used)

    try:
        result = AnswerSummary.model_validate_json(final_text)

        return result.model_copy(
            update={"tools_used": recorded_tools}
        )

    except (ValidationError, ValueError, TypeError) as error:
        logger.warning(
            "Final response was not valid AnswerSummary JSON: %s",
            error,
        )

    retry_messages = [
        {
            "role": "system",
            "content": (
                "You are a JSON response formatter. Return ONLY one valid "
                "JSON object with these fields: "
                '"answer" (string), "tools_used" (array of strings), '
                '"confidence" (number between 0 and 1). '
                "Do not include Markdown fences or additional text."
            ),
        },
        {
            "role": "user",
            "content": (
                "Convert the response below into the required JSON format. "
                "Preserve its meaning. Use the actual tool names provided "
                "below for tools_used. If the original response is empty, "
                "explain that no valid answer was produced.\n\n"
                f"Actual tools used: {json.dumps(recorded_tools)}\n"
                f"Original response:\n{final_text or '[empty response]'}"
            ),
        },
    ]

    try:
        retry = client.chat.completions.create(
            model=GEMINI_MODEL,
            messages=retry_messages,
            response_format={"type": "json_object"},
            max_tokens=500,
        )

        retry_text = retry.choices[0].message.content or ""
        result = AnswerSummary.model_validate_json(retry_text)

        logger.info("Final JSON validated successfully after retry.")

        return result.model_copy(
            update={"tools_used": recorded_tools}
        )

    except Exception:
        logger.exception("Final JSON validation failed after retry.")

        return AnswerSummary(
            answer=(
                "I couldn't generate a valid structured answer this time. "
                "Please try your question again."
            ),
            tools_used=recorded_tools,
            confidence=0.0,
        )


def run_agent(user_question: str) -> AnswerSummary:
    """Run the tool-calling agent and return a validated answer."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]

    tools_used: list[str] = []

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
                answer = (
                    "The language model API quota or rate limit was reached. "
                    "Please wait and try again."
                )
            else:
                answer = (
                    "The language model request failed. "
                    "Please check your configuration or try again later."
                )

            return AnswerSummary(
                answer=answer,
                tools_used=unique_tools(tools_used),
                confidence=0.0,
            )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name

                # Record the tool before execution so failed calls are tracked.
                if tool_name not in tools_used:
                    tools_used.append(tool_name)

                try:
                    arguments = json.loads(
                        tool_call.function.arguments or "{}"
                    )

                    if not isinstance(arguments, dict):
                        raise ValueError(
                            "Tool arguments must be a JSON object."
                        )

                    result = execute_tool(tool_name, arguments)
                    tool_content = json.dumps(result, default=str)

                    logger.info(
                        "Tool %s executed successfully.",
                        tool_name,
                    )

                except Exception as error:
                    logger.exception(
                        "Tool execution failed: %s",
                        tool_name,
                    )

                    tool_content = json.dumps(
                        {
                            "error": str(error),
                            "tool": tool_name,
                        }
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_content,
                    }
                )

            continue

        final_text = message.content or ""
        return parse_final_answer(final_text, tools_used)

    logger.warning("Agent reached maximum step limit.")

    return AnswerSummary(
        answer=(
            f"The agent reached its maximum of {MAX_STEPS} steps "
            "before completing the request."
        ),
        tools_used=unique_tools(tools_used),
        confidence=0.0,
    )
