import abc
import os

from enum import Enum
from utils import ASSET_DIR


class ResourceCard(abc.ABC):
    @abc.abstractmethod
    def name(self):
        pass

    def asset(self):
        return f"{os.path.join(os.path.join(ASSET_DIR, 'resource'),self.__class__.__name__.lower())}.jpg"


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
