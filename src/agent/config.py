
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

LLM_MODEL = (
    os.getenv("LLM_MODEL")
    or os.getenv("GEMINI_MODEL")
    or "gemini-3.5-flash-lite"
)

if LLM_PROVIDER == "gemini":
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    base_url = os.getenv(
        "LLM_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    if not api_key:
        raise ValueError("Set LLM_API_KEY or GEMINI_API_KEY in .env")

elif LLM_PROVIDER == "ollama":
    api_key = os.getenv("LLM_API_KEY", "ollama")
    base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")

else:
    raise ValueError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}. "
        "Choose 'gemini' or 'ollama'."
    )

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    timeout=120.0,
max_retries=2,
)

# Backward compatibility with the existing agent_loop.py
GEMINI_MODEL = LLM_MODEL
