"""Agent configuration, read once from the .env file (see .env.example)."""

import os

from dotenv import load_dotenv

load_dotenv()

# Model, reached through the IMT gateway (OpenAI-compatible)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_BASE_URL = os.environ["OPENAI_BASE_URL"]
OPENAI_MODEL = os.environ["OPENAI_MODEL"]

# Backend MCP server exposing the banking tools
BACKEND_MCP_URL = os.getenv("BACKEND_MCP_URL", "http://127.0.0.1:8000/mcp")

# AG-UI server, called by the CopilotKit runtime
AGENT_PORT = int(os.getenv("AGENT_PORT", "8001"))
