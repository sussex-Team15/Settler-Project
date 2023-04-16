import abc
import hexgrid
from enum import Enum

from src.resource_ import Resource
from src.utils import TILE_CARDS_DIR, Abstract


class Tile(Abstract):
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
        return self.get_asset(TILE_CARDS_DIR)


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

    def name(self):  # pylint: disable=function-redefined
        return self.tile.name()

    def generate_resource(self):
        return self.tile.generate_resource().value

    def short_name(self):
        return self.tile.short_name()

    def asset(self):
        return self.tile.asset()


class GameTile:  # pylint: disable=too-many-instance-attributes
    def __init__(self, real_number, tile, points, tile_id):
        self.real_number = real_number  # number that will show on GUI
        self.tile = tile
        self.points = points
        self.tile_id = tile_id

        def convert_to_number(coord):
            return int(f"{hexgrid.hex_digit(coord,digit=1)}"
                       f"{hexgrid.hex_digit(coord,digit=2)}")

        self.tile_coord = convert_to_number(
            hexgrid.tile_id_to_coord(self.tile_id))

        self.node_coord_n = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'N'))
        self.node_coord_ne = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'NE'))
        self.node_coord_nw = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'NW'))
        self.node_coord_s = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'S'))
        self.node_coord_se = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'SE'))
        self.node_coord_sw = convert_to_number(
            hexgrid.from_location(hexgrid.NODE, self.tile_id, 'SW'))

        self.edge_ne = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'NE'))
        self.edge_nw = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'NW'))
        self.edge_se = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'SE'))
        self.edge_sw = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'SW'))
        self.edge_s = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'E'))
        self.edge_w = convert_to_number(
            hexgrid.from_location(hexgrid.EDGE, self.tile_id, 'W'))

    def __repr__(self):
        return f"GameTile({self.tile.name()}, {self.tile_id})"

    def get_tile_info(self):

        return {
            'Tile id': self.tile_id,
            'Coord': self.tile_coord,
            'Node': {'Node <N>': self.node_coord_n,
                     'Node <NE>': self.node_coord_ne,
                     'Node <NW>': self.node_coord_nw,
                     'Node <S>': self.node_coord_s,
                     'Node <SE>': self.node_coord_se,
                     'Node <SW>': self.node_coord_sw},

            'Edge': {'Edge <E>': self.edge_s,
                     'Edge <NE>': self.edge_ne,
                     'Edge <NW>': self.edge_nw,
                     'Edge <SE>': self.edge_se,
                     'Edge <SW>': self.edge_sw,
                     'Edge <W>': self.edge_w}
        }
