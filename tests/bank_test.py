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
    return Bank([Resource.BRICK] * 4 + [Resource.WOOD] * 4 + [Resource.WOOL]
                * 4 + [Resource.GRAIN] * 4 + [Resource.ORE] * 4, [])


def test_bank_init(bank):
    """
    Test function that checks initialization of bank object.

    This function checks that the bank is initialized with 20 resources and 0 development cards.

    :param bank: An instance of Bank class.
    :type bank: Bank
    """
    assert len(bank.resources) == 20
    assert len(bank.dev_cards) == 0
    assert bank.trade_ratios == 4


def test_get_trade_ratio(bank):
    """
    Test function that checks get_trade_ratio method of bank object.

    This function checks that get_trade_ratio method of bank object returns the expected value.

    :param bank: An instance of Bank class.
    :type bank: Bank
    """
    assert bank.get_trade_ratio(0) == 4
    assert bank.get_trade_ratio(1) == 3


def test_null_method(bank):
    """
    Test function that checks null_method of bank object.

    This function checks that null_method of bank object returns the expected value.

    :param bank: An instance of Bank class.
    :type bank: Bank
    """
    assert bank.null_method() == (bank.resources, bank.trade_ratios,
                                  bank.dev_cards)
