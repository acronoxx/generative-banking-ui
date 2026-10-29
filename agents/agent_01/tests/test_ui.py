"""Tests of ui.show_interface: no model or backend needed."""


def test_valid_interface_returns_envelope():
    """Valid components: the tool returns an A2UI envelope."""
    raise NotImplementedError


def test_unknown_component_returns_errors():
    """Component missing from the page catalog: the tool returns errors for the model."""
    raise NotImplementedError


def test_missing_root_returns_errors():
    """No component with id "root": the tool returns errors for the model."""
    raise NotImplementedError
