import abc

from enum import Enum
from src.utils import DEVELOPMENT_CARDS_DIR, Abstract


class DevelopmentCard(Abstract):
    """_summary_

    :param Abstract: _description_
    :type Abstract: _type_
    """
    def name(self):
        return self.__class__.__name__.title().replace('_', ' ')

    @abc.abstractmethod
    def description(self):
        pass

    @abc.abstractmethod
    def vp_awarded(self):
        return 0  # 0 for false and anyother num for the amount of VP awarded

    def asset(self):
        return self.get_asset(DEVELOPMENT_CARDS_DIR)


class Chapel(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class Knight(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return ("Move the Robber. Steal 1 resource card "
                "from the owner of an adjacent settlement")

    def vp_awarded(self):
        return 0


class LargestArmy(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return ("The first player to play 3 Knight cards "
                "gets this card. Another player who plays more "
                "Knight cards will take this card")

    def vp_awarded(self):
        return 2


class Library(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class LongestRoad(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return ("This Card Goes to the player with the longes unbroken"
                " road of at least 5 segments. Another player who builds"
                " a longer Road will take this card")

    def vp_awarded(self):
        return 2


class Market(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return "+1 Victor Point"

    def vp_awarded(self):
        return 1


class Monopoly(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return ("When you play this card, announce 1 type of resource."
                " All other players must give you all their resource cards "
                "of that type")

    def vp_awarded(self):
        return 0


class Palace(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class RoadBuilding(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return "Place 2 new roads as if you had just built them"

    def vp_awarded(self):
        return 0


class University(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class YearofPlenty(DevelopmentCard):
    """_summary_

    :param DevelopmentCard: _description_
    :type DevelopmentCard: _type_
    """
    def description(self):
        return ("take any 2 resources from the bank add them to your hand."
                " They can be 2 of the same resource or 2 different resources")

    def vp_awarded(self):
        return 0


class DevelopmentCards(Enum):
    """_summary_

    :param Enum: _description_
    :type Enum: _type_
    :return: _description_
    :rtype: _type_
    """
    CHAPEL = Chapel()
    KNIGHT = Knight()
    LARGEST_ARMY = LargestArmy()
    LIBRARY = Library()
    LONGEST_ROAD = LongestRoad()
    MARKET = Market()
    MONOPLY = Monopoly()
    PALACE = Palace()
    ROAD_BUILDING = RoadBuilding()
    UNIVERSITY = University()
    YEAR_OF_PLENTY = YearofPlenty()

    def __init__(self, card):
        self.card = card

    def name(self):  # pylint: disable=function-redefined
        return self.card.name()

    def description(self):
        return self.card.description()

    def vp_awarded(self):
        return self.card.vp_awarded()

    def asset(self):
        return self.card.asset()


print(DevelopmentCards.CHAPEL.name())
