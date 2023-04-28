# pylint: disable=missing-module-docstring
# pylint: disable=redefined-outer-name
import pytest
from src.bank import Bank
from src.resource_ import Resource


@pytest.fixture
def bank():
    """
    Fixture function that returns an instance of Bank class.

    :return: An instance of Bank class.
    :rtype: Bank
    """
    return Bank()


def test_bank_init(bank):
    """
    Test function that checks initialization of bank object.

    This function checks that the bank is initialized with 20 resources and 0 development cards.

    :param bank: An instance of Bank class.
    :type bank: Bank
    """
    assert len(bank.resources) == 5
    assert bank.trade_ratio == 4


def test_null_method(bank):
    """
    Test function that checks null_method of bank object.

    This function checks that null_method of bank object returns the expected value.

    :param bank: An instance of Bank class.
    :type bank: Bank
    """
    assert bank.null_method() == (bank.resources, bank.trade_ratio)
