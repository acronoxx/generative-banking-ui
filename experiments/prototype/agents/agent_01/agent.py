"""Banking assistant: model, system prompt, middlewares and agent loop.

The loop itself (model -> tools -> model) is provided by LangChain's create_agent:
this module only configures it.
"""

from datetime import date
from pathlib import Path

from copilotkit import CopilotKitMiddleware
from langchain.agents import create_agent
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph

import config
import ui

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
    """Read the system prompt from prompt.md (the page catalog is added at each request by ui)."""
    return PROMPT_FILE.read_text(encoding="utf-8").replace("{today}", date.today().isoformat())


def build_agent(tools: list[BaseTool]) -> CompiledStateGraph:
    """Assemble the agent: backend tools + show_interface, CopilotKit and catalog middlewares,
    and a checkpointer keeping the history of each conversation (lost when the agent restarts).
    """
    return create_agent(
        model=build_model(),
        system_prompt=load_prompt(),
        tools=[*tools, ui.show_interface],
        middleware=[CopilotKitMiddleware(), ui.catalog_prompt],
        checkpointer=InMemorySaver(),
    )
