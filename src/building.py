import abc
import os
from src.utils import BUILDINGS_DIR, FILE_EXTENSIONS
from src.resource_ import Resource


class Building(abc.ABC):
    """Abstract class template for building types controls behaviour or
    settlements and builidngs
   
    :param owner: player that owns current building
    :type owner: str
    :param node: which node the building has been constructed on
    :type node: int
    :param cost: cost of resources required to construct the building
    :type cost: list
    """
    def __init__(self, owner, node):
        """Constructor Method
        """
        self.owner = owner
        self.node = node
        self.cost = []

    def build(self, resources):
        """Builds a specific type of building, either city or settlement

        :param resources: Player's current resource inventory to construct a building
        :type resources: list
        """
        enough_resource = all(resource in resources for resource in self.cost)
        if enough_resource:
            # TODO node needs to be object instance of a Node class
            self.node.has_settlement = True

    def asset(self):
        """Retrieves corresponding image files for either a city or settlement

        :raises NotImplementedError: If a type of building besides a city or settlement is attempted to be built
        """
        found_files = [file for file in os.listdir(
            BUILDINGS_DIR) if self.__class__.__name__.lower() in file]
        if found_files:
            for file in found_files:
                extension = f".{file.split('.')[1]}"
                if extension in FILE_EXTENSIONS:
                    return os.path.join(BUILDINGS_DIR, file)

        act_class = self.__class__.__name__.lower()
        base_class = self.__class__.__bases__[0].__name__.lower()
        raise NotImplementedError(f"no asset files found for "
                                  f"'{act_class}' "
                                  f"{base_class}")


class Settlement(Building):
    """Inherits behaviour from abstract base class building

    :param owner: player that owns current building
    :type owner: str
    :param node: which node the building has been constructed on
    :type node: int
    :param cost: cost of resources required to construct the building
    :type cost: list
    """

    def __init__(self, owner, node):
        """Constructor Method
        """
        super().__init__(owner, node)
        self.cost = [Resource.BRICK, Resource.WOOL,
                     Resource.GRAIN, Resource.WOOD]


class City(Building):
    """Inherits behaviour from abstract base class building

    :param owner: player that owns current building
    :type owner: str
    :param node: which node the building has been constructed on
    :type node: int
    :param cost: cost of resources required to construct the building
    :type cost: list
    """
    def __init__(self, owner, node):
        """Constructor Method
        """
        super().__init__(owner, node)
        self.valid_node = False
        if self.node.has_settlement:
            self.valid_node = True
        self.cost = [Resource.GRAIN, Resource.GRAIN,
                     Resource.ORE, Resource.ORE, Resource.ORE]
