"""Tests of the ownership checks of app/services/: a customer only reaches their own data."""


def test_list_accounts_returns_only_own_accounts():
    """list_accounts returns the accounts of the connected customer and no other."""
    raise NotImplementedError


def test_transactions_of_other_customer_account_are_refused():
    """get_recent_transactions on another customer's account returns an error."""
    raise NotImplementedError


def test_prepare_transfer_from_other_customer_account_is_refused():
    """prepare_transfer with a source account or a beneficiary of another customer returns an error."""
    raise NotImplementedError
