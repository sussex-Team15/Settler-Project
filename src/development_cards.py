# pylint: disable=missing-module-docstring
# pylint: disable=unnecessary-pass
import abc

from enum import Enum
from src.utils import DEVELOPMENT_CARDS_DIR, Abstract
from src.resource_ import Resource

class DevelopmentCard(Abstract):
    """Abstract class template for development cards 
    and controls behaviour for all development card 
    types, also inherits behaviour from abstract class
    so that the correct image files are retrieved for 
    each development card.

    :param Abstract: abstract base class in utils.py
    :type Abstract: type
    """
    def name(self):
        """Returns name of development card

        :return: Development Card name
        :rtype: Development Card class
        """
        return self.__class__.__name__.title().replace('_', ' ')

    @abc.abstractmethod
    def description(self):
        """
        Abstract method representing description of a development card and the outcome
        
        Should be implemented by derived classes to return card's description

        :return: A String representing the description
        """
        pass

    @abc.abstractmethod
    def vp_awarded(self):
        """
        Abstract method representing how many victory points should be awarded
        
        Should be implemented by derived classes to return number of victory points

        :return: An integer representing victory points
        """
        return 0  # 0 for false and anyother num for the amount of VP awarded

    def asset(self):
        """Returns development card asset

        :return: Development Card asset
        :rtype: str
        """
        return self.get_asset(DEVELOPMENT_CARDS_DIR)
    
    def cost(self):
        """
        Returns cost of development card

        :return: An interger representing the cost of the card
        :rtype: int
        """
        return 0


class VictoryPointCard(DevelopmentCard):
    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class Chapel(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating the amount of victory points gained from building a Chapel

        :return: A string displaying the amount of victory points gained from building a Chapel
        :rtype: str
        """
        return "+1 Victory Point"

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 1


class Knight(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating how the player is now allowed to move the robber

        :return: A string displaying player's new priviledges
        :rtype: str
        """
        return ("Move the Robber. Steal 1 resource card "
                "from the owner of an adjacent settlement")

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 0
    
    def cost(self):
        return {Resource.WOOL: 1, Resource.GRAIN: 1, Resource.ORE: 1}


class LargestArmy(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating the requirements met to obtain this card

        :return: A string displaying the rules around this card
        :rtype: str
        """
        return ("The first player to play 3 Knight cards "
                "gets this card. Another player who plays more "
                "Knight cards will take this card")

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 2


class Library(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating that the player has gained a victory point

        :return: A string displaying a new victory point
        :rtype: str
        """
        return "+1 Victory Point"

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 1


class LongestRoad(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating the requirements the player has met to gain this card

        :return: A string displaying the rules associated with this card
        :rtype: str
        """
        return ("This Card Goes to the player with the longes unbroken"
                " road of at least 5 segments. Another player who builds"
                " a longer Road will take this card")

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 2


class Market(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating that the player has gained a victory point

        :return: A string displaying a new victory point
        :rtype: str
        """
        return "+1 Victory Point"

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 1


class Monopoly(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating that the player's new priviledges

        :return: A string outlining what resources the player is now entitled to
        :rtype: str
        """
        return ("When you play this card, announce 1 type of resource."
                " All other players must give you all their resource cards "
                "of that type")

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 0


class Palace(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating that the player has gained a victory point

        :return: A string displaying a new victory point
        :rtype: str
        """
        return "+1 Victory Point"

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 1


class RoadBuilding(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating that the player can place 2 new roads

        :return: A string displaying the players road building priviledges
        :rtype: str
        """
        return "Place 2 new roads as if you had just built them"

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 0


class University(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating that the player has gained a victory point

        :return: A string displaying a new victory point
        :rtype: str
        """
        return "+1 Victory Point"

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 1


class YearofPlenty(DevelopmentCard):
    """Derived Class from DevelopmentCard abstract class
    """
    def description(self):
        """Displays a string indicating that the player can pick 2 resources from the bank

        :return: A string displaying the player's new resource priviledges
        :rtype: str
        """
        return ("take any 2 resources from the bank add them to your hand."
                " They can be 2 of the same resource or 2 different resources")

    def vp_awarded(self):
        """Amount of victory points awarded

        :return: Displays an integer value of the number of victory points to be awarded
        :rtype: int
        """
        return 0


class DevelopmentCards(Enum):
    """
    Enumerations of development cards available in the game.

    :param Enum: Enum base class.
    :type Enum: Enum
    :return: The DevelopmentCards object with corresponding card object.
    :rtype: DevelopmentCards
    """
    
    CHAPEL = Chapel()
    KNIGHT = Knight()
    LARGEST_ARMY = LargestArmy()
    LIBRARY = Library()
    LONGEST_ROAD = LongestRoad()
    VP = VictoryPointCard()
    MARKET = Market()
    MONOPLY = Monopoly()
    PALACE = Palace()
    ROAD_BUILDING = RoadBuilding()
    UNIVERSITY = University()
    YEAR_OF_PLENTY = YearofPlenty()

    def __init__(self, card):
        """Constructor class
        :param card: The corresponding DevelopmentCard object for this resource.
        :type card: DevelopmentCard
        """
        self.card = card

    def name(self):  # pylint: disable=function-redefined
        """
        Get the name of the development card.

        :return: The name of the development card.
        :rtype: str
        """
        return self.card.name()

    def description(self):
        """
        Get the description of the development card.

        :return: The description of the development card.
        :rtype: str
        """
        return self.card.description()

    def vp_awarded(self):
        """
        Get the victory point awarded by the development card.

        :return: The victory point awarded by the development card.
        :rtype: int
        """
        return self.card.vp_awarded()

    def asset(self):
        """
        Get the asset (i.e. image) of the development card.

        :return: The asset of the development card.
        :rtype: str
        """
        return self.card.asset()
    def cost(self):
        return self.card.cost()

