import sys

from src.player import Player
from src.trade import Trade


def test_trade_init():
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)

    assert trade.offering_player == player1
    assert trade.offered_resources == resources
    assert trade.recieving_player == player2
    assert trade.is_accepted is False


def test_accept_trade():
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)
    trade.accept_trade()

    assert trade.is_accepted is True


def test_cancel_trade():
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)
    trade.accept_trade()
    trade.cancel_trade()

    assert trade.is_accepted is False


def test_get_offering_player():
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)

    assert trade.get_offering_player() == player1


def test_get_offered_resource():
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)

    assert trade.get_offered_resource() == resources


def test_execute_trade():
    player1 = Player("Noah", (255, 0, 0))
    player1.resources = ["Wood", "Brick"]
    player2 = Player("John", (0, 255, 0))
    player2.resources = ["Sheep", "Ore"]
    resources = ["Brick"]

    trade = Trade(player1, resources, player2)
    trade.accept_trade()
    trade.execute_trade()

    assert "Wood" in player1.resources
    assert "Brick" not in player1.resources
    assert "Wood" not in player2.resources
    assert "Brick" in player2.resources
    assert "Sheep" in player2.resources
    assert "Ore" in player2.resources
