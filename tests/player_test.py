# pylint: disable=redefined-outer-name
# pylint: disable=wrong-import-position
# pylint: disable=missing-module-docstring
# pylint: disable=fixme
import pytest

from src.player import Player
from src.resource_ import Resource


@pytest.fixture
def player():
    """
    Fixture that returns a Player object for testing.

    :return: A Player object representing a player in the game.
    :rtype: Player
    """
    return Player("John", (255, 0, 0))


def test_roll_dice(player):
    """
    Test the roll_dice method of the Player class.

    This test checks that the roll_dice method returns two integers between 1 and 6.

    :param player: A Player object representing a player in the game.
    :type player: Player
    """
    dice_1, dice_2 = player.roll_dice()
    assert 1 <= dice_1 <= 6
    assert 1 <= dice_2 <= 6


def test_build_settlement(player):
    # TODO: DocString
    player.resources = {Resource.BRICK: 2,
                        Resource.WOOD: 2,
                        Resource.WOOL: 2,
                        Resource.GRAIN: 2}

    pdb.set_trace()
    player.build_settlement(1110, False)

    assert {Resource.BRICK: 2,
            Resource.WOOD: 2,
            Resource.WOOL: 2,
            Resource.GRAIN: 2} != player.resources


# TODO: test building a city


def test_build_road(player):
    """
    Test the build_road method of the Player class.

    This test checks that the build_road method increases the number of roads of the player by one,
    and that the new road starts at the correct node.

    :param player: A Player object representing a player in the game.
    :type player: Player
    """
    road_count = len(player.roads)
    player.resources = {Resource.WOOD:1, Resource.BRICK:1}
    player.build_road(1, 2)
    assert len(player.roads) == road_count + 1
    assert player.roads[-1] == (1, 2)


def test_get_resources(player):
    """
    Test the add_resources method of the Player class.

    This test checks that the add_resources method adds 
    the specified resource to the player's resources.

    :param player: A Player object representing a player in the game.
    :type player: Player
    """
    player.resources = {Resource.WOOD:1,
                        Resource.BRICK:1, Resource.GRAIN:1, Resource.WOOL:1}
    assert player.get_resources() == {
        Resource.WOOD:1, Resource.BRICK:1, Resource.GRAIN:1, Resource.WOOL:1}


def test_add_resources(player):
    player.add_resource(Resource.WOOD)
    player.add_resource(Resource.BRICK)
    assert player.resources == {Resource.WOOD:1, Resource.BRICK:1, 
                                Resource.GRAIN:0, Resource.NONE:0,
                                Resource.ORE:0, Resource.WOOL:0}


def test_get_victory_points(player):
    """
    Test the get_victory_points method of the Player class.

    This test checks that the get_victory_points method 
    returns the correct number of victory points of the player.

    :param player: A Player object representing a player in 
    the game.
    :type player: Player
    """
    player.victory_points = 5
    assert player.get_victory_points() == 5
