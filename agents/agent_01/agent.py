"""Banking assistant: model, system prompt, middlewares and agent loop.

The loop itself (model -> tools -> model) is provided by LangChain's create_agent:
this module only configures it.
"""

from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph

import config

PROMPT_FILE = Path(__file__).with_name("prompt.md")


def build_model() -> ChatOpenAI:
    """Create the chat model, reached through the IMT gateway (OpenAI-compatible).

    The gateway expects the key both as API key and as "subscription-key" query parameter.
    """
    return ChatOpenAI(
        model=config.OPENAI_MODEL,
        base_url=config.OPENAI_BASE_URL,
        api_key=config.OPENAI_API_KEY,
        default_query={"subscription-key": config.OPENAI_API_KEY},
    )


def load_prompt() -> str:
    """Read the system prompt from prompt.md.

    The page component catalog is added at each request by ui.catalog_prompt.
    """
    raise NotImplementedError


def build_agent(tools: list[BaseTool]) -> CompiledStateGraph:
    """Assemble the agent and return it, ready to be exposed by main.py.

    Args:
        tools: banking tools discovered on the backend MCP server (tools.load_backend_tools).

    The agent receives these tools plus ui.show_interface, the middlewares
    CopilotKitMiddleware then ui.catalog_prompt, and a checkpointer that keeps
    the history of each conversation (InMemorySaver: lost when the agent restarts).
    """
    raise NotImplementedError
