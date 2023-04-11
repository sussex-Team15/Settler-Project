import abc
import os
from utils import BUILDINGS_DIR, FILE_EXTENSIONS
from resource_ import Resource


class Building(abc.ABC):
    def __init__(self, owner, node):
        self.owner = owner
        self.node = node
        self.cost = []

    def build(self, resources):
        enough_resource = all(resource in resources for resource in self.cost)
        if enough_resource:
            # TODO node needs to be object instance of a Node class
            self.node.has_settlement = True

    def asset(self):

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

    def __init__(self, owner, node):
        super().__init__(owner, node)
        self.cost = [Resource.BRICK, Resource.WOOL,
                     Resource.GRAIN, Resource.WOOD]


class City(Building):

    def __init__(self, owner, node):
        super().__init__(owner, node)
        self.valid_node = False
        if self.node.has_settlement:
            self.valid_node = True
        self.cost = [Resource.GRAIN, Resource.GRAIN,
                     Resource.ORE, Resource.ORE, Resource.ORE]
