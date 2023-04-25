import abc

from enum import Enum
from src.utils import DEVELOPMENT_CARDS_DIR, Abstract
from src.resource_ import Resource

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
    
    def cost(self):
        return 0



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
    
    def cost(self):
        return {Resource.WOOL: 1, Resource.GRAIN: 1, Resource.ORE: 1}


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


class VictoryPointCard(DevelopmentCard):
    """_summary_

    Args:
        DevelopmentCard (_type_): _description_

    Returns:
        _type_: _description_
    """

    def description(self):
        return ("Card rewards player with one victory point")
    
    def vp_awarded(self):
        return  1
    
    def name(self):
        return "VP card"
    
    def cost(self):
        return {Resource.WOOL: 1, Resource.GRAIN: 1, Resource.ORE: 1}


class DevelopmentCards(Enum):
    """_summary_

    :param Enum: _description_
    :type Enum: _type_
    :return: _description_
    :rtype: _type_
    """
    
    KNIGHT = Knight()
    LARGEST_ARMY = LargestArmy()
    LONGEST_ROAD = LongestRoad()
    VP = VictoryPointCard()
    

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
    def cost(self):
        return self.card.cost()

