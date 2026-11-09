"""A2UI: how the agent describes interfaces for the page.

The agent does not render anything. The page declares its component catalog,
the agent composes an interface with these components and returns it as an A2UI
message (JSON description), sent to the page through AG-UI; the page renders it
with its React components (frontend/src/catalog/).
"""

from typing import Any

from langchain.agents.middleware import ModelRequest, dynamic_prompt
from langchain.tools import ToolRuntime


def page_catalog(state: dict) -> dict | None:
    """Return the A2UI catalog declared by the page, or None if the page sent none.

    The CopilotKit runtime places it in state["ag-ui"]["a2ui_schema"] (JSON string or dict).
    """
    raise NotImplementedError


@dynamic_prompt
def catalog_prompt(request: ModelRequest) -> str:
    """Build the system prompt of each model call: prompt.md + JSON schema of the page components.

    Needed because CopilotKitMiddleware does not copy state["ag-ui"] into the prompt.
    """
    raise NotImplementedError


def show_interface(components: list[dict[str, Any]], runtime: ToolRuntime, data: dict[str, Any] | None = None) -> str:
    """Describe an interface for the page to display, using the page's component catalog.

    Args:
        components: A2UI v0.9 components (flat list, root component with id "root").
        data: optional data model, for values bound with {"path": "/key"}.

    Returns the A2UI operations envelope (create_surface, update_components,
    update_data_model) or, if the components are invalid, the validation errors
    so that the model can fix them and call the tool again.
    """
    raise NotImplementedError
