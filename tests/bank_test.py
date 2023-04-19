# pylint: disable=missing-module-docstring,missing-function-docstring
# pylint: disable=redefined-outer-name
import pytest
from src.bank import Bank
from src.resource_ import Resource


@pytest.fixture
def bank():
    return Bank([Resource.BRICK] * 4 + [Resource.WOOD] * 4 + [Resource.WOOL]
                * 4 + [Resource.GRAIN] * 4 + [Resource.ORE] * 4, [])


def test_bank_init(bank):
    assert len(bank.resources) == 20
    assert len(bank.dev_cards) == 0
    assert bank.trade_ratios == 4


def test_get_trade_ratio(bank):
    assert bank.get_trade_ratio(0) == 4
    assert bank.get_trade_ratio(1) == 3


def test_null_method(bank):
    assert bank.null_method() == (bank.resources, bank.trade_ratios,
                                  bank.dev_cards)
