import abc
from enum import Enum

from src.utils import RESOURCE_CARDS_DIR, Abstract


class ResourceCard(Abstract):
    @abc.abstractmethod
    def name(self):
        pass

    def asset(self):
        return self.get_asset(RESOURCE_CARDS_DIR)


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
