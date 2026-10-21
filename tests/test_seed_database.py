"""Tests unitaires des fonctions utilitaires de backend/seed_database.py."""

import re
from unittest.mock import MagicMock

import pytest

from backend.models import Account
from backend.seed_database import (
    BATCH_SIZE,
    batches,
    count_rows,
    insert_in_batches,
    make_iban,
    make_pin_hash,
)


# ---------------- make_iban ----------------

def is_valid_iban(iban):
    """Validation ISO 13616 : 4 premiers caractères à la fin,
    lettres remplacées par des nombres (A=10 ... Z=35), reste modulo 97 égal à 1."""
    rearranged = iban[4:] + iban[:4]
    numeric = "".join(str(int(char, 36)) for char in rearranged)
    return int(numeric) % 97 == 1


def test_make_iban_is_valid():
    iban = make_iban(42)

    # Format français : 27 caractères, commence par "FR"
    assert len(iban) == 27
    assert iban.startswith("FR")
    assert iban[2:].isdigit()
    assert is_valid_iban(iban)


@pytest.mark.parametrize("number", [0, 1, 96, 97, 12_345, 99_999, 10**10])
def test_make_iban_is_valid_for_many_numbers(number):
    iban = make_iban(number)

    assert re.fullmatch(r"FR\d{25}", iban)
    assert is_valid_iban(iban)


def test_make_iban_is_deterministic():
    assert make_iban(123) == make_iban(123)


def test_make_iban_gives_different_ibans_for_different_numbers():
    ibans = {make_iban(n) for n in range(1_000)}

    assert len(ibans) == 1_000


def test_is_valid_iban_detects_a_typo():
    # Vérifie que notre outil de validation n'accepte pas n'importe quoi :
    # changer un seul chiffre doit rendre l'IBAN invalide.
    iban = make_iban(42)
    last_digit = int(iban[-1])
    wrong_iban = iban[:-1] + str((last_digit + 1) % 10)

    assert not is_valid_iban(wrong_iban)


# ---------------- make_pin_hash ----------------

def test_make_pin_hash_format():
    parts = make_pin_hash("alice").split("$")

    assert len(parts) == 4
    algorithm, iterations, salt, digest = parts
    assert algorithm == "pbkdf2_sha256"
    assert iterations == "100000"
    assert re.fullmatch(r"[0-9a-f]{32}", salt)
    assert re.fullmatch(r"[0-9a-f]{64}", digest)  # SHA-256 = 32 octets = 64 caractères hexa


def test_make_pin_hash_is_deterministic():
    assert make_pin_hash("alice") == make_pin_hash("alice")


def test_make_pin_hash_differs_between_users():
    # Le sel dépend du nom d'utilisateur : deux utilisateurs avec le même PIN
    # ne doivent pas avoir le même hash.
    assert make_pin_hash("alice") != make_pin_hash("bob")


def test_make_pin_hash_does_not_contain_the_username():
    assert "alice" not in make_pin_hash("alice")


# ---------------- batches ----------------

def test_batches_with_no_rows():
    assert list(batches([], size=3)) == []


def test_batches_with_exactly_one_batch():
    assert list(batches([1, 2, 3], size=3)) == [[1, 2, 3]]


def test_batches_with_a_smaller_last_batch():
    assert list(batches([1, 2, 3, 4], size=3)) == [[1, 2, 3], [4]]


def test_batches_keeps_every_row_in_order():
    rows = list(range(10))

    flattened = [row for batch in batches(rows, size=4) for row in batch]

    assert flattened == rows


def test_batches_uses_batch_size_by_default():
    rows = list(range(BATCH_SIZE + 1))

    sizes = [len(batch) for batch in batches(rows)]

    assert sizes == [BATCH_SIZE, 1]


# ---------------- count_rows ----------------
# On remplace la session SQLAlchemy par un MagicMock : pas besoin de PostgreSQL.

def test_count_rows_returns_the_count():
    session = MagicMock()
    session.scalar.return_value = 7

    assert count_rows(session, Account) == 7
    session.scalar.assert_called_once()


def test_count_rows_returns_zero_when_result_is_none():
    session = MagicMock()
    session.scalar.return_value = None

    assert count_rows(session, Account) == 0


# ---------------- insert_in_batches ----------------

def test_insert_in_batches_inserts_and_flushes_each_batch():
    session = MagicMock()
    rows = [{"id": i} for i in range(BATCH_SIZE * 2 + 1)]

    insert_in_batches(session, Account, rows)

    assert session.execute.call_count == 3
    assert session.flush.call_count == 3
    sent_batches = [call.args[1] for call in session.execute.call_args_list]
    assert [len(batch) for batch in sent_batches] == [BATCH_SIZE, BATCH_SIZE, 1]


def test_insert_in_batches_does_nothing_without_rows():
    session = MagicMock()

    insert_in_batches(session, Account, [])

    session.execute.assert_not_called()
    session.flush.assert_not_called()
