import abc
from enum import Enum

from src.utils import RESOURCE_CARDS_DIR, Abstract


class ResourceCard(Abstract):
    """Abstract class template for Resource cards and controls behaviour for all resource card types, also inherits behaviour from abstract class so that the correct image files are retrieved for each resource card

    :param Abstract: abstract base class in utils.py
    :type Abstract: type
    """
    @abc.abstractmethod
    def name(self):
        """
        Abstract method representing description of a resource card and the outcome
        
        Should be implemented by derived classes to return card's description

        :return: A String representing the description of a resource card
        """
        pass

    def asset(self):
        """Returns resource card asset

        :return: Resource Card asset
        :rtype: str
        """
        return self.get_asset(RESOURCE_CARDS_DIR)


class Lumber(ResourceCard):
    """Derived Class from ResourceCard abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the resource card - Lumber

        :return: A string displaying the resource card name
        :rtype: str
        """
        return "Lumber"


class Wool(ResourceCard):
    """Derived Class from ResourceCard abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the resource card - Wool

        :return: A string displaying the resource card name
        :rtype: str
        """
        return "Wool"


class Grain(ResourceCard):
    """Derived Class from ResourceCard abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the resource card - Grain

        :return: A string displaying the resource card name
        :rtype: str
        """
        return "Grain"


class Brick(ResourceCard):
    """Derived Class from ResourceCard abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the resource card - Brick

        :return: A string displaying the resource card name
        :rtype: str
        """
        return "Brick"


class Ore(ResourceCard):
    """Derived Class from ResourceCard abstract class
    """
    def name(self):
        """Displays a string indicating the Name of the resource card - Brick

        :return: A string displaying the resource card name
        :rtype: Ore
        """
        return "Ore"


class Null(ResourceCard):
    def name(self):
        return None

# pylint: disable=function-redefined


class Resource(Enum):
    """Enum base class

    :param Enum: _description_
    :type Enum: _type_
    :return: _description_
    :rtype: _type_
    """
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
