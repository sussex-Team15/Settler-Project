import abc
import os

from enum import Enum
from utils import ASSET_DIR, FILE_EXTENSIONS, DEVELOPMENT_CARDS_DIR


class DevelopmentCard(abc.ABC):
    def name(self):
        return self.__class__.__name__.title().replace('_', ' ')

    @abc.abstractmethod
    def description(self):
        pass

    @abc.abstractmethod
    def vp_awarded(self):
        return 0  # 0 for false and anyother num for the amount of VP awarded

    def asset(self):

        found_files = [file for file in os.listdir(
            DEVELOPMENT_CARDS_DIR) if self.__class__.__name__.lower() in file]
        if found_files:
            for file in found_files:
                extension = f".{file.split('.')[1]}"
                if extension in FILE_EXTENSIONS:
                    return os.path.join(DEVELOPMENT_CARDS_DIR, file)

        act_class = self.__class__.__name__.lower()
        base_class = self.__class__.__bases__[0].__name__.lower()
        raise NotImplementedError(f"no asset files found for "
                                  f"{act_class}' "
                                  f"{base_class}")


class Chapel(DevelopmentCard):

    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class Knight(DevelopmentCard):

    def description(self):
        return ("Move the Robber. Steal 1 resource card "
                "from the owner of an adjacent settlement")

    def vp_awarded(self):
        return 0


class Largest_Army(DevelopmentCard):

    def description(self):
        return ("The first player to play 3 Knight cards "
                "gets this card. Another player who plays more "
                "Knight cards will take this card")

    def vp_awarded(self):
        return 2


class Library(DevelopmentCard):

    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class Longest_Road(DevelopmentCard):

    def description(self):
        return ("This Card Goes to the player with the longes unbroken"
                " road of at least 5 segments. Another player who builds"
                " a longer Road will take this card")

    def vp_awarded(self):
        return 2


class Market(DevelopmentCard):

    def description(self):
        return "+1 Victor Point"

    def vp_awarded(self):
        return 1


class Monopoly(DevelopmentCard):

    def description(self):
        return ("When you play this card, announce 1 type of resource."
                " All other players must give you all their resource cards "
                "of that type")

    def vp_awarded(self):
        return 0


class Palace(DevelopmentCard):

    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class Road_Building(DevelopmentCard):

    def description(self):
        return ("Place 2 new roads as if you had just built them")

    def vp_awarded(self):
        return 0


class University(DevelopmentCard):

    def description(self):
        return "+1 Victory Point"

    def vp_awarded(self):
        return 1


class Year_of_Plenty(DevelopmentCard):

    def description(self):
        return ("take any 2 resources from the bank add them to your hand."
                " They can be 2 of the same resource or 2 different resources")

    def vp_awarded(self):
        return 0


class DevelopmentCards(Enum):

    CHAPEL = Chapel()
    KNIGHT = Knight()
    LARGEST_ARMY = Largest_Army()
    LIBRARY = Library()
    LONGEST_ROAD = Longest_Road()
    MARKET = Market()
    MONOPLY = Monopoly()
    PALACE = Palace()
    ROAD_BUILDING = Road_Building()
    UNIVERSITY = University()
    YEAR_OF_PLENTY = Year_of_Plenty()

    def __init__(self, card):
        self.card = card

    def name(self):
        return self.card.name()

    def asset(self):
        return self.card.asset()
