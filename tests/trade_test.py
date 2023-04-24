# pylint: disable=missing-module-docstring
from src.player import Player
from src.trade import Trade


def test_trade_init():
    """
    Test the Trade object is initialized with the expected values.

    :return: Nothing.
    """
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)

    assert trade.offering_player == player1
    assert trade.offered_resources == resources
    assert trade.recieving_player == player2
    assert trade.is_accepted is False


def test_accept_trade():
    """
    Test that the Trade object is marked as accepted after calling accept_trade.

    :return: Nothing.
    """
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)
    trade.accept_trade()

    assert trade.is_accepted is True


def test_cancel_trade():
    """
    Test that the Trade object is marked as not accepted after calling cancel_trade.

    :return: Nothing.
    """
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)
    trade.accept_trade()
    trade.cancel_trade()

    assert trade.is_accepted is False


def test_get_offering_player():
    """
    Test that get_offering_player() returns the correct offering player.

    :return: Nothing.
    """
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)

    assert trade.get_offering_player() == player1


def test_get_offered_resource():
    """
    Test that get_offered_resource() returns the correct offered resources.

    :return: Nothing.
    """
    player1 = Player("Noah", (255, 0, 0))
    player2 = Player("John", (0, 255, 0))
    resources = ["Wool", "Grain", "Brick", "Wood", "Ore"]

    trade = Trade(player1, resources, player2)

    assert trade.get_offered_resource() == resources


def test_execute_trade():
    """
    Test that execute_trade() properly transfers resources between players.

    :return: Nothing.
    """
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
