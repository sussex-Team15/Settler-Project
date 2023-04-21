import random

from src.trade import Trade
from src.building import Settlement, City
from src.resource_ import Resource


class Player:  # pylint: disable=too-many-instance-attributes
    """
    Player class that controls the
    behaviour of an indivdual player of the game.

    Contains attributes such as the player name and number of VP'S.

    Attributes:

    - name : str
        String representing the name of the player
    - victory_points: int
        Integer representing the number
        of victory points the player has received.
    - color: tuple
        A tuple with an r,g,b value representing the color that the player has.
    - resources: dict
        a dictionary of resource type mapped to the amount the player has
    - settlements: list
        A list of settlements the player has
    - cities: list
        A list of cities the player has
    - roads: list
        a list of roads the player has (all of type Road)
    - isTurn: boolean
        a boolean indicating if it is the players turn in the gameloop.
    - hasLongestRoad: boolean
        a boolean indicating if the player has the longest road.
    - has_largest_army: boolean
        a boolean indicating if the player has the largest army
    - trade_offers: list
        a list of trade_offers that the player has received (of type Trade)


    Methods:

    - build_settlement(self, location)
        builds a settlement at the specified location
    - build_road(self, location1, location2)
        builds a road from location1 to location2
    - buy_card(self)
        buys card from the bank
    - play_card(self, card)
        uses the selected card
    - make_trade(self, resource, player)
        activates a trade with
        the specified player offering the specified Resource
    - end_turn(self)
        ends player's turn
    - get_resources(self)
        returns list of resources player has
    - get_victory_points(self)
        returns number of victory points player has
    - get_longest_road(self):
        returns the longest road that the player currently has

    """

    def __init__(self, name, color):
        self.name = name
        self.victory_points = 0
        self.color = color
        self.resources = {}
        for r in Resource:
            self.resources[r] = 0

        self.settlements = []
        self.cities = []
        self.roads = []
        self.is_turn = False
        self.has_longest_road = False
        self.total_road_num = 0
        self.has_largest_army = False
        self.trade_offers = []

    # can be used for any number of dice (default =2)
    def roll_dice(self, num_dice=2):
        """
        This returns 1st dice roll, 2nd dice roll.
        Like this::

            p = Player()
            p.roll_dice("...")

        :param num_dice: number of dice to be rolled
        :type num_dice: int, optional
        :return: Tuple
        """
        return tuple(random.randint(1, 6) for i in range(num_dice))

    def build_settlement(self, node):
        """
        Builds a settlement at specified node 
        Can only build if player has enough resources

        """
        self.resources[Resource.BRICK.name()]-=1
        self.resources[Resource.WOOD.name()]-=1
        self.resources[Resource.WOOL.name()]-=1
        self.resources[Resource.GRAIN.name()]-=1
        self.settlements.append(node)
       

    def build_city(self, node):
        """
        Builds a city at specified node
        only can build if a settlement is on the node
        """
        self.resources[Resource.ORE.name()]-=3
        self.resources[Resource.GRAIN.name()]-=2
        self.cities.append(node)
        

    def build_road(self, node1, node2):
        """
        builds a road from node1 to node2.
        Road will be set to the color of the player building
        """
        self.resources[Resource.WOOD]-=1
        self.resources[Resource.BRICK]-=1
        self.roads.append((node1, node2))
        print(f'road built from {node1} to {node2}')
        

    def buy_dev_card(self, bank):
        '''
        Buys a development card from the bank

            Paramaters: self
        '''

    def make_trade(self, resource, player):
        new_trade = Trade(self, resource, player)
        new_trade.execute_trade()

    def end_turn(self):
        self.is_turn = False

    def get_resources(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.resources

    def add_resource(self, resource):
        if resource in self.resources:
            self.resources[resource] +=1
        else:
            self.resources[resource] = 1

    def get_victory_points(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.victory_points

    def get_longest_road(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        longest_road = self.roads[0].get_length()
        # TODO implement get_length() in Road class
        for road in self.roads[1:]:
            if road.get_length() > longest_road.get_length():
                road = longest_road

        return longest_road
