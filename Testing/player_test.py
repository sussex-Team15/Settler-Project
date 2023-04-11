import pytest
import sys
sys.path.insert(1, 'src')

from player import Player


@pytest.fixture
def player():
    return Player("John", (255, 0, 0))


def test_roll_dice(player):
    d1, d2 = player.roll_dice()
    assert 1 <= d1 <= 6
    assert 1 <= d2 <= 6


def test_build_settlement(player):
    pass


def test_build_city(player):
    pass


def test_build_road(player):
    road_count = len(player.roads)
    player.resources = [Resource.WOOD, Resource.BRICK]
    player.build_road(1, 2)
    assert len(player.roads) == road_count + 1
    assert player.roads[-1] == (1, 2)


def test_get_resources(player):
    player.resources = [Resource.WOOD, Resource.BRICK, Resource.GRAIN, Resource.WOOL]
    assert player.get_resources() == [Resource.WOOD, Resource.BRICK, Resource.GRAIN, Resource.WOOL]


def test_add_resources(player):
    player.add_resources(Resource.WOOD)
    player.add_resources(Resource.BRICK)
    assert player.resources == [Resource.WOOD, Resource.BRICK]


def test_get_victory_points(player):
    player.victory_points = 5
    assert player.get_victory_points() == 5