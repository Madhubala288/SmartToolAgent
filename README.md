# SmartToolAgent - Custom ReAct AI Agent Framework

A terminal-based AI assistant built with Python and Gemini. It uses a custom ReAct (Reason-Act-Observe) agent loop to select and execute tools, observe their results, and return structured JSON validated with Pydantic.

## Architecture & Workflow Diagram


┌─────────────────────────────────────────┐
│              User Request               │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│         ReAct Agent Loop (LLM)          │
│          (Reason - Act - Observe)       │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│        Tool Selection & Schema          │
│          (Pydantic Validation)          │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│            Tools Execution              │
│  ├─ Calculator                          │
│  ├─ Weather API (Open-Meteo)            │
│  └─ SQLite Notes DB                     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│          Observation Channel            │
│       (Feed context back to LLM)        │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│          Pydantic JSON Output           │
└─────────────────────────────────────────┘

## Features

* Calculator: Safe evaluation of mathematical expressions.
* Current Weather: Fetches real-time weather using Open-Meteo API.
* SQLite Notes: Persistent storage and retrieval of user notes.
* Custom Agent Loop: Native LLM tool-calling loop.
* Pydantic Validation: Ensures structured final responses.
* Dynamic Schemas (Bonus): Automatic JSON schema generation using Python inspect.

## Prerequisites

* Python 3.10+
* uv (or pip)
* Gemini API key
* Internet connection for Gemini and weather requests

## Setup

1. Download or clone this repository.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate
4. Install project dependencies:
pip install -r requirements.txt
5. Copy .env.example to .env.
6. Add your own Gemini API key to .env.

## Run

python main.py

Type a question at the prompt. Type exit to quit.

## Example JSON Output

{
"answer": "25 multiplied by 5 is 125.",
"tools_used": ["calculator"],
"confidence": 1.0
}

## Security

Never share your Gemini API key or commit your .env file to GitHub.