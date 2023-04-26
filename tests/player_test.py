# pylint: disable=redefined-outer-name
# pylint: disable=wrong-import-position
# pylint: disable=missing-module-docstring,missing-function-docstring
# pylint: disable=fixme



import pytest

from src.player import Player
from src.resource_ import Resource


@pytest.fixture
def player():

    return Player("John", (255, 0, 0))


def test_roll_dice(player):
    dice_1, dice_2 = player.roll_dice()
    assert 1 <= dice_1 <= 6
    assert 1 <= dice_2 <= 6


def test_build_settlement(player):
    player.resources = {Resource.BRICK: 1,
                        Resource.WOOD: 1,
                        Resource.WOOL: 1,
                        Resource.GRAIN: 1}
    player.build_settlement(1110, False)
    assert {Resource.BRICK: 1,
            Resource.WOOD: 1,
            Resource.WOOL: 1,
            Resource.GRAIN: 1} != player.resources


def test_build_city(player):
    player.resources = {Resource.ORE: 3,
                        Resource.GRAIN: 2}
    player.build_city(1110)
    assert {Resource.ORE: 3,
            Resource.GRAIN: 2} != player.resources


def test_build_road(player):
    road_count = len(player.roads)
    player.resources = {Resource.WOOD:1, Resource.BRICK:1}
    player.build_road(1, 2)
    assert len(player.roads) == road_count + 1
    assert player.roads[-1] == (1, 2)


def test_get_resources(player):
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
    player.victory_points = 5
    assert player.get_victory_points() == 5
