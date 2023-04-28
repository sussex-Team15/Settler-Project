# pylint: disable=missing-module-docstring
# pylint: disable=unnecessary-pass
import abc
from enum import Enum

from src.utils import RESOURCE_CARDS_DIR, Abstract


class ResourceCard(Abstract):
    """Abstract class template for Resource cards and
    controls behaviour for all resource card types,
    also inherits behaviour from abstract class so
    that the correct image files are retrieved for
    each resource card

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
    """Derived Class from ResourceCard abstract class"""

    def name(self):
        """Displays a string indicating the Name of the resource card - Lumber

        :return: A string displaying the resource card name
        :rtype: str
        """
        return "Lumber"


class Wool(ResourceCard):
    """Derived Class from ResourceCard abstract class"""

    def name(self):
        """Displays a string indicating the Name of the resource card - Wool

        :return: A string displaying the resource card name
        :rtype: str
        """
        return "Wool"


class Grain(ResourceCard):
    """Derived Class from ResourceCard abstract class"""

    def name(self):
        """Displays a string indicating the Name of the resource card - Grain

        :return: A string displaying the resource card name
        :rtype: str
        """
        return "Grain"


class Brick(ResourceCard):
    """Derived Class from ResourceCard abstract class"""

    def name(self):
        """Displays a string indicating the Name of the resource card - Brick

        :return: A string displaying the resource card name
        :rtype: str
        """
        return "Brick"


class Ore(ResourceCard):
    """Derived Class from ResourceCard abstract class"""

    def name(self):
        """Displays a string indicating the Name of the resource card - Brick

        :return: A string displaying the resource card name
        :rtype: Ore
        """
        return "Ore"


class Null(ResourceCard):
    """
    A class representing a null resource card.
    """

    def name(self):
        """
        Returns None, since a null resource card has no name.

        :return: None
        """
        return None


# pylint: disable=function-redefined


class Resource(Enum):
    """Class representing a Settlers of Catan resource.

    :param card: The corresponding ResourceCard object for this resource.
    :type card: ResourceCard
    """

    WOOD = Lumber()
    WOOL = Wool()
    GRAIN = Grain()
    BRICK = Brick()
    ORE = Ore()

    NONE = Null()

    def __init__(self, card):
        """Constructor class"""
        self.card = card

    def name(self):
        """Get the name of the resource.

        :return: The name of the resource.
        :rtype: str
        """
        return self.card.name()

    def asset(self):
        """Get the asset representing the resource.

        :return: The asset representing the resource.
        :rtype: str
        """
        return self.card.asset()
