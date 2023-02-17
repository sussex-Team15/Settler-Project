import abc
import os

from enum import Enum
from resource_cards import Resource
from utils import ASSET_DIR


class Tile(abc.ABC):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def generate_resource(self):
        pass

    @abc.abstractmethod
    def short_name(self):
        pass

    def asset(self):
        return f"{os.path.join(os.path.join(ASSET_DIR, 'tiles'),self.__class__.__name__.lower())}.jpg"


class Forest(Tile):
    def name(self):
        return "Forest"

    def generate_resource(self):
        return Resource.WOOD

    def short_name(self):
        return "fo"


class Pasture(Tile):
    def name(self):
        return "Pasture"

    def generate_resource(self):
        return Resource.WOOL

    def short_name(self):
        return "pa"


class Fields(Tile):
    def name(self):
        return "Fields"

    def generate_resource(self):
        return Resource.GRAIN

    def short_name(self):
        return "fi"


class Hills(Tile):
    def name(self):
        return "Hills"

    def generate_resource(self):
        return Resource.BRICK

    def short_name(self):
        return "hi"


class Mountain(Tile):
    def name(self):
        return "Mountain"

    def generate_resource(self):
        return Resource.ORE

    def short_name(self):
        return "mo"


class Desert(Tile):
    def name(self):
        return "Desert"

    def generate_resource(self):
        return Resource.NONE

    def short_name(self):
        return "de"


class ResourceTile(Enum):
    FOREST = Forest()
    PASTURE = Pasture()
    FIELDS = Fields()
    HILLS = Hills()
    MOUNTAIN = Mountain()
    DESERT = Desert()

    def __init__(self, tile):
        self.tile = tile

    def name(self):
        return self.tile.name()

    def generate_resource(self):
        return self.tile.generate_resource().value

    def short_name(self):
        return self.tile.short_name()

    def asset(self):
        return self.tile.asset()


class GameTile:
    def __init__(self, number_label, tile, points, position):
        self.number_label = number_label
        self.tile = tile
        self.points = points
        self.position = position
