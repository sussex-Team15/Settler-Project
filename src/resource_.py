import abc
import os

from enum import Enum
from utils import ASSET_DIR, RESOURCE_CARDS_DIR


class ResourceCard(abc.ABC):
    @abc.abstractmethod
    def name(self):
        pass

    def asset(self):

        found_files = [file for file in os.listdir(RESOURCE_CARDS_DIR) if self.__class__.__name__.lower() in file]
        if found_files:
            for file in found_files:
                extension = f".{file.split('.')[1]}"
                if extension in FILE_EXTENSIONS:
                    return os.path.join(RESOURCE_CARDS_DIR, file)

        raise NotImplementedError(f"no asset files found for "
                                  f"{self.__class__.__name__.lower()}' "
                                  f"{self.__class__.__bases__[0].__name__.lower()}")


class Lumber(ResourceCard):
    def name(self):
        return "Lumber"


class Wool(ResourceCard):
    def name(self):
        return "Wool"


class Grain(ResourceCard):
    def name(self):
        return "Grain"


class Brick(ResourceCard):
    def name(self):
        return "Brick"


class Ore(ResourceCard):
    def name(self):
        return "Ore"


class Null(ResourceCard):
    def name(self):
        return None


class Resource(Enum):
    WOOD = Lumber()
    WOOL = Wool()
    GRAIN = Grain()
    BRICK = Brick()
    ORE = Ore()

    NONE = Null()

    def __init__(self, card):
        self.card = card

    def name(self):
        return self.card.name()

    def asset(self):
        return self.card.asset()
