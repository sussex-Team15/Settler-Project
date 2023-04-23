import abc
from enum import Enum
import hexgrid

from src.resource_ import Resource
from src.utils import TILE_CARDS_DIR, Abstract


class Tile(Abstract):
    """Abstract class template for Tiles and controls behaviour for all tile card types, also inherits behaviour from abstract class so that the correct image files are retrieved for each tile

    :param Abstract: abstract base class in utils.py
    :type Abstract: type
    """
    @abc.abstractmethod
    def name(self):
        """
        Abstract method representing description of a game tile
        
        Should be implemented by derived classes to return tile's description

        :return: A String representing the description of a tile
        """
        pass

    @abc.abstractmethod
    def generate_resource(self):
        """
        Abstract method representing description of a game tile
        
        Should be implemented by derived classes to return tile's description

        :return: 1 new resource based on which tile is in use
        """
        pass

    @abc.abstractmethod
    def short_name(self):
        """
        Abstract method representing short name description of a game tile
        
        Should be implemented by derived classes to return short tile's description

        :return: A String representing the short name description of a tile
        """
        pass

    def asset(self):
        """Returns Tile asset

        :return: Tile asset file
        :rtype: str
        """
        return self.get_asset(TILE_CARDS_DIR)


class Forest(Tile):
    """Derived Class from Tile abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the Tile - Forest

        :return: A string displaying the tile name
        :rtype: str
        """
        return "Forest"

    def generate_resource(self):
        """Displays which new resource has now been generated

        :return: 1 new resource based on which tile is in use
        :rtype: Resource
        """
        return Resource.WOOD

    def short_name(self):
        """Displays a string indicating the short Name of the tile - Fo

        :return: A string displaying the short tile name
        :rtype: str
        """
        return "fo"


class Pasture(Tile):
    """Derived Class from Tile abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the Tile - Pasture

        :return: A string displaying the tile name
        :rtype: str
        """
        return "Pasture"

    def generate_resource(self):
        """Displays which new resource has now been generated

        :return: 1 new resource based on which tile is in use
        :rtype: Resource
        """
        return Resource.WOOL

    def short_name(self):
        """Displays a string indicating the short Name of the tile - Pa

        :return: A string displaying the short tile name
        :rtype: str
        """
        return "pa"


class Fields(Tile):
    """Derived Class from Tile abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the Tile - Fields

        :return: A string displaying the tile name
        :rtype: str
        """
        return "Fields"

    def generate_resource(self):
        """Displays which new resource has now been generated

        :return: 1 new resource based on which tile is in use
        :rtype: Resource
        """
        return Resource.GRAIN

    def short_name(self):
        """Displays a string indicating the short Name of the tile - fi

        :return: A string displaying the short tile name
        :rtype: str
        """
        return "fi"


class Hills(Tile):
    """Derived Class from Tile abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the Tile - Hills

        :return: A string displaying the tile name
        :rtype: str
        """
        return "Hills"

    def generate_resource(self):
        """Displays which new resource has now been generated

        :return: 1 new resource based on which tile is in use
        :rtype: Resource
        """
        return Resource.BRICK

    def short_name(self):
        """Displays a string indicating the short Name of the tile - hi

        :return: A string displaying the short tile name
        :rtype: str
        """
        return "hi"


class Mountain(Tile):
    """Derived Class from Tile abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the Tile - Mountain

        :return: A string displaying the tile name
        :rtype: str
        """
        return "Mountain"

    def generate_resource(self):
        """Displays which new resource has now been generated

        :return: 1 new resource based on which tile is in use
        :rtype: Resource
        """
        return Resource.ORE

    def short_name(self):
        """Displays a string indicating the short Name of the tile - mo

        :return: A string displaying the short tile name
        :rtype: str
        """
        return "mo"


class Desert(Tile):
    """Derived Class from Tile abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the Tile - Desert

        :return: A string displaying the tile name
        :rtype: str
        """
        return "Desert"

    def generate_resource(self):
        """Displays which new resource has now been generated

        :return: 1 new resource based on which tile is in use
        :rtype: Resource
        """
        return Resource.NONE

    def short_name(self):
        """Displays a string indicating the short Name of the tile - de

        :return: A string displaying the short tile name
        :rtype: str
        """
        return "de"


class ResourceTile(Enum):
    """
    Represents a resource tile in the game, with associated properties and methods.

    This class is an enumeration of the different types of resource tiles in the game, including Forest, Pasture, Fields, Hills, Mountain, and Desert. Each type of tile has a corresponding `Tile` object, which is used to generate resources and provide other information.
    """
    FOREST = Forest()
    PASTURE = Pasture()
    FIELDS = Fields()
    HILLS = Hills()
    MOUNTAIN = Mountain()
    DESERT = Desert()

    def __init__(self, tile):
        """
        Initializes a new resource tile object with the given `Tile` object.

        :param tile: The `Tile` object associated with the resource tile.
        :type tile: Tile
        """
        self.tile = tile

    def name(self):  # pylint: disable=function-redefined
        """
        Returns the name of the resource tile.

        :return: The name of the resource tile.
        :rtype: str
        """
        return self.tile.name()

    def generate_resource(self):
        """
        Generates a resource for the resource tile.

        :return: The generated resource.
        :rtype: Resource
        """
        return self.tile.generate_resource().value

    def short_name(self):
        """
        Returns the short name of the resource tile.

        :return: The short name of the resource tile.
        :rtype: str
        """
        return self.tile.short_name()

    def asset(self):
        """
        Returns the asset file associated with the resource tile.

        :return: The asset file associated with the resource tile.
        :rtype: str
        """
        return self.tile.asset()


class GameTile:  # pylint: disable=too-many-instance-attributes
    """
    Represents a game tile in a hexagonal grid, with associated coordinates and edges.

    :param real_number: The number that will show on the GUI.
    :type real_number: int
    :param tile: The tile object.
    :type tile: object
    :param points: The points of the tile.
    :type points: int
    :param tile_id: The unique ID of the tile.
    :type tile_id: int

    This class represents a game tile in a hexagonal grid. It contains attributes that represent
    the tile's real number, the tile object, its points, and its unique ID. It also has properties
    that represent its coordinates and edges, which are calculated using the Hexgrid module.
    """
    def __init__(self, real_number, tile, points, tile_id):
        """Constructor Class
        """
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
        """
        Returns a string representation of the game tile.

        :return: A string representation of the game tile.
        :rtype: str
        """
        return f"GameTile({self.tile.name()}, {self.tile_id})"

    def get_tile_info(self):
        """
        Returns a dictionary of the tile's ID, coordinates, and edges.

        :return: A dictionary of the tile's ID, coordinates, and edges.
        :rtype: dict
        """
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
