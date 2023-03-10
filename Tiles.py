from pprint import pprint
import abc
import os
import hexgrid

from enum import Enum
from resource_cards import Resource
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

        found_files = [file for file in os.listdir(TILE_CARDS_DIR) if self.__class__.__name__.lower() in file]
        if found_files:
            for file in found_files:
                extension = f".{file.split('.')[1]}"
                if extension in FILE_EXTENSIONS:
                    return os.path.join(TILE_CARDS_DIR, file)

        raise NotImplementedError(f"no asset files found for "
                                  f"{self.__class__.__name__.lower()}' "
                                  f"{self.__class__.__bases__[0].__name__.lower()}")


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
    def __init__(self, number_label, tile, points, tile_id):
        self.number_label = number_label
        self.tile = tile
        self.points = points
        self.tile_id = tile_id

    def __repr__(self):
        return f"GameTile({self.tile.name()}, {self.tile_id})"

    def get_tile_info(self):

        def convert_to_number(coord):
            return int(f"{hexgrid.hex_digit(coord,digit=1)}{hexgrid.hex_digit(coord,digit=2)}")
        tile_coord = hexgrid.tile_id_to_coord(self.tile_id)

        node_coord_N = hexgrid.from_location(hexgrid.NODE, self.tile_id, 'N')
        node_coord_NE = hexgrid.from_location(hexgrid.NODE, self.tile_id, 'NE')
        node_coord_NW = hexgrid.from_location(hexgrid.NODE, self.tile_id, 'NW')
        node_coord_S = hexgrid.from_location(hexgrid.NODE, self.tile_id, 'S')
        node_coord_SE = hexgrid.from_location(hexgrid.NODE, self.tile_id, 'SE')
        node_coord_SW = hexgrid.from_location(hexgrid.NODE, self.tile_id, 'SW')

        edge_NE = hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'NE')
        edge_NW = hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'NW')
        edge_SE = hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'SE')
        edge_SW = hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'SW')
        edge_E = hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'E')
        edge_W = hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'W')

        return {
            'Tile id': self.tile_id,
            'Coord': convert_to_number(tile_coord),
            'Node <N>': convert_to_number(node_coord_N),
            'Node <NE>': convert_to_number(node_coord_NE),
            'Node <NW>': convert_to_number(node_coord_NW),
            'Node <S>': convert_to_number(node_coord_S),
            'Node <SE>': convert_to_number(node_coord_SE),
            'Node <SW>': convert_to_number(node_coord_SW),

            'Edge <E>': convert_to_number(edge_E),
            'Edge <NE>': convert_to_number(edge_NE),
            'Edge <NW>': convert_to_number(edge_NW),
            'Edge <SE>': convert_to_number(edge_SE),
            'Edge <SW>': convert_to_number(edge_SW),
            'Edge <W>': convert_to_number(edge_W),
        }
