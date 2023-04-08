import pytest
import sys
sys.path.insert(1, 'src')

from player import *
from trade import *




def test_trade_init():
    player1 = Player("Noah")
    player2 = Player("John")
    resources = ["Wool","Grain","Brick","Wood","Ore"]

    trade = Trade(player1, resources, player2)

    assert trade.offering_player == player1
    assert trade.offered_resources == resources
    assert trade.recieving_player == player2
    assert trade.is_accepted == False


def test_accept_trade():
    player1 = Player("Noah")
    player2 = Player("John")
    resources = ["Wool","Grain","Brick","Wood","Ore"]

    trade = Trade(player1, resources, player2)
    trade.accept_trade()

    assert trade.is_accepted == True


def test_cancel_trade():
    player1 = Player("Noah")
    player2 = Player("John")
    resources = ["Wool","Grain","Brick","Wood","Ore"]

    trade = Trade(player1, resources, player2)
    trade.accept_trade()
    trade.cancel_trade()

    assert trade.is_accepted == False


def test_get_offering_player():
    player1 = Player("Noah")
    player2 = Player("John")
    resources = ["Wool","Grain","Brick","Wood","Ore"]

    trade = Trade(player1, resources, player2)
    
    assert trade.get_offering_player() == player1


def test_get_offered_resource():
    player1 = Player("Noah")
    player2 = Player("John")
    resources = ["Wool","Grain","Brick","Wood","Ore"]

    trade = Trade(player1, resources, player2)

    assert trade.get_offered_resource() == resources


def test_execute_trade():
    player1 = Player("Noah")
    player1.resources = ["Wood", "Brick"]
    player2 = Player("John")
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