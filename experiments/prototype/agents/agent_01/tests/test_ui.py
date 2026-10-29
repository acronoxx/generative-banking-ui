"""Tests of ui.show_interface: no model or backend needed."""

import json
from types import SimpleNamespace

import ui

# Minimal page catalog: the basic Column and Text components plus one banking component
CATALOG = {
    "catalogId": "test://catalog",
    "components": {
        "Column": {"type": "object", "properties": {"children": {"type": "array"}}},
        "Text": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]},
        "AccountCard": {
            "type": "object",
            "properties": {"accountType": {"type": "string"}, "balance": {"type": "string"}},
            "required": ["accountType", "balance"],
        },
    },
}
RUNTIME = SimpleNamespace(state={"ag-ui": {"a2ui_schema": json.dumps(CATALOG)}})


def test_valid_interface_returns_envelope():
    """Valid components: the tool returns an A2UI envelope."""
    components = [
        {"id": "root", "component": "Column", "children": ["a1"]},
        {"id": "a1", "component": "AccountCard", "accountType": "checking", "balance": "10 €"},
    ]
    result = ui.show_interface(components, RUNTIME)
    assert "Invalid" not in result
    assert "test://catalog" in result


def test_unknown_component_returns_errors():
    """Component missing from the page catalog: the tool returns errors for the model."""
    result = ui.show_interface([{"id": "root", "component": "Chart"}], RUNTIME)
    assert result.startswith("Invalid interface")


def test_missing_root_returns_errors():
    """No component with id "root": the tool returns errors for the model."""
    result = ui.show_interface([{"id": "x", "component": "Text", "text": "hi"}], RUNTIME)
    assert result.startswith("Invalid interface")
