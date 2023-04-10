from pprint import pprint
import abc
import os
import hexgrid

from enum import Enum
from resource_ import Resource
from utils import FILE_EXTENSIONS, TILE_CARDS_DIR


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

        found_files = [file for file in os.listdir(
            TILE_CARDS_DIR) if self.__class__.__name__.lower() in file]
        if found_files:
            for file in found_files:
                extension = f".{file.split('.')[1]}"
                if extension in FILE_EXTENSIONS:
                    return os.path.join(TILE_CARDS_DIR, file)

        act_class = self.__class__.__name__.lower()
        base_class = self.__class__.__bases__[0].__name__.lower()
        raise NotImplementedError(f"no asset files found for "
                                  f"{act_class}' "
                                  f"{base_class}")


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
    def __init__(self, number_label, real_number, tile, points, tile_id):
        self.number_label = number_label
        self.real_number = real_number  # number that will show on GUI
        self.tile = tile
        self.points = points
        self.tile_id = tile_id

        def convert_to_number(coord):
            return int(f"{hexgrid.hex_digit(coord,digit=1)}"
                       f"{hexgrid.hex_digit(coord,digit=2)}")

        self.tile_coord = convert_to_number(
            hexgrid.tile_id_to_coord(self.tile_id))

        self.node_coord_N = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'N'))
        self.node_coord_NE = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'NE'))
        self.node_coord_NW = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'NW'))
        self.node_coord_S = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'S'))
        self.node_coord_SE = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'SE'))
        self.node_coord_SW = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'SW'))

        self.edge_NE = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'NE'))
        self.edge_NW = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'NW'))
        self.edge_SE = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'SE'))
        self.edge_SW = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'SW'))
        self.edge_E = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'E'))
        self.edge_W = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'W'))

    def __repr__(self):
        return f"GameTile({self.tile.name()}, {self.tile_id})"

    def get_tile_info(self):

        def convert_to_number(coord):
            return int(f"{hexgrid.hex_digit(coord,digit=1)}"
                       f"{hexgrid.hex_digit(coord,digit=2)}")

        return {
            'Tile id': self.tile_id,
            'Coord': self.tile_coord,
            'Node': {'Node <N>': self.node_coord_N,
                     'Node <NE>': self.node_coord_NE,
                     'Node <NW>': self.node_coord_NW,
                     'Node <S>': self.node_coord_S,
                     'Node <SE>': self.node_coord_SE,
                     'Node <SW>': self.node_coord_SW},

            'Edge': {'Edge <E>': self.edge_E,
                     'Edge <NE>': self.edge_NE,
                     'Edge <NW>': self.edge_NW,
                     'Edge <SE>': self.edge_SE,
                     'Edge <SW>': self.edge_SW,
                     'Edge <W>': self.edge_W}
        }
