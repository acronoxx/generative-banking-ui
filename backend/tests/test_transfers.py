"""Tests of the two-step transfer: prepared by the agent, confirmed by the customer on the page."""


def test_prepare_transfer_moves_no_money():
    """prepare_transfer creates a pending simulation and leaves the balances unchanged."""
    raise NotImplementedError


def test_confirm_with_wrong_password_is_refused():
    """POST /api/transfers/{id}/confirm with a wrong password does not confirm the simulation.

    To be decided: only relevant if the login uses a password.
    """
    raise NotImplementedError


def test_confirm_twice_is_refused():
    """A simulation that is no longer pending (confirmed or cancelled) cannot be confirmed."""
    raise NotImplementedError


def test_cancelled_simulation_cannot_be_confirmed():
    """After POST /api/transfers/{id}/cancel, the confirmation returns an error."""
    raise NotImplementedError
