"""A2UI: how the agent describes interfaces for the page.

The agent does not render anything. The page declares its component catalog,
the agent composes an interface with these components and returns it as an A2UI
message (JSON description), sent to the page through AG-UI; the page renders it
with its React components (frontend/src/catalog/).
"""

import json
from typing import Any
from uuid import uuid4

from ag_ui_a2ui_toolkit import (
    BASIC_CATALOG_ID,
    create_surface,
    format_validation_errors,
    update_components,
    update_data_model,
    validate_a2ui_components,
    wrap_as_operations_envelope,
)
from langchain.agents.middleware import ModelRequest, dynamic_prompt
from langchain.tools import ToolRuntime


def page_catalog(state: dict) -> dict | None:
    """Return the A2UI catalog declared by the page, or None if the page sent none.

    The CopilotKit runtime places it in state["ag-ui"]["a2ui_schema"] (JSON string or dict).
    """
    schema = (state.get("ag-ui") or {}).get("a2ui_schema")
    return json.loads(schema) if isinstance(schema, str) else schema


@dynamic_prompt
def catalog_prompt(request: ModelRequest) -> str:
    """Build the system prompt of each model call: prompt.md + JSON schema of the page components.

    Needed because CopilotKitMiddleware does not copy state["ag-ui"] into the prompt.
    """
    catalog = page_catalog(request.state)
    if not catalog:
        return request.system_prompt
    return f"{request.system_prompt}\n\n## Available components (JSON schema)\n{json.dumps(catalog['components'])}"


def show_interface(components: list[dict[str, Any]], runtime: ToolRuntime, data: dict[str, Any] | None = None) -> str:
    """Display an interface to the customer, composed with the available components.

    Args:
        components: A2UI v0.9 components (flat list, root component with id "root").
        data: optional data model, for values bound with {"path": "/key"}.
    """
    catalog = page_catalog(runtime.state)
    check = validate_a2ui_components(components=components, data=data, catalog=catalog)
    if not check["valid"]:
        # Sent back to the model, which fixes the components and calls the tool again
        return "Invalid interface, fix it and try again:\n" + format_validation_errors(check["errors"])

    surface = f"surface-{uuid4().hex[:8]}"
    operations = [
        create_surface(surface, (catalog or {}).get("catalogId", BASIC_CATALOG_ID)),
        update_components(surface, components),
    ]
    if data:
        operations.append(update_data_model(surface, data))
    return wrap_as_operations_envelope(operations)
