from enum import Enum
import abc


class ResourceCard(abc.ABC):
    @abc.abstractmethod
    def name(self):
        pass

    def char(self):
        return f"{self.name()[0]}{self.name()[-1]}"

    def asset(self):
        return f"PATH\\ResourceCard_{self.__class__.__name__}.png"


class Wood(ResourceCard):
    def name(self):
        return "Wood"


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


class Resource(Enum):
    WOOD = Wood()
    WOOL = Wool()
    GRAIN = Grain()
    BRICK = Brick()
    ORE = Ore()

    NONE = None

    def __init__(self, card):
        self.card = card

    def name(self):
        return self.card.name()

    def char(self):
        return self.card.char()

    def asset(self):
        return self.card.asset()
