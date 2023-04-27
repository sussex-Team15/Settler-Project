# pylint: disable=missing-module-docstring
import random

from src.trade import Trade
from src.building import Settlement, City
from src.resource_ import Resource


class Player:  # pylint: disable=too-many-instance-attributes
    """Player class that controls the behaviour of 
    an indivdual player of the game. Contains attributes
    such as the player name and number of VP'S.

    :param name: String representing the name of the 
    player
    :type name: str
    :param victory_points: Integer representing the number 
    of victory points the player has received.
    :type victory_points: int  
    :param color: A tuple with an r,g,b value representing the color that the player has.
    :type color: tuple
    :param resources: A list of resources that the player has (all of type Resource)
    :type resources: list
    :param settlements: A list of settlements the player has
    :type settlements: list
    :param cities: A list of cities the player has
    :type cities: list
    :param roads: a list of roads the player has (all of type Road)
    :type roads: list
    :param isTurn: a boolean indicating if it is the players turn in the gameloop.
    :type is Turn: bool  
    :param hasLongestRoad: a boolean indicating if the player has the longest road.
    :type hasLongestRoad: bool
    :param has_largest_army: a boolean indicating if the player has the largest army
    :type has_largest_army: bool
    :param trade_offers: a list of trade_offers that the player has received (of type Trade)
    :type trade_offers: list
    """

    def __init__(self, name, color):
        """Constructor Class
        """
        self.name = name
        self.victory_points = 0
        self.color = color
        self.resources = {resource.name(): 0 for resource in Resource if not resource.name() == None}

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
        """This returns 1st dice roll, 2nd dice roll.
        Like this::

            p = Player()
            print(p.roll_dice("2")) = [5,2]

        :param num_dice: number of dice to be rolled
        :type num_dice: int, optional
        :return: A Tuple
        :rtype: tuple
        """
        return tuple(random.randint(1, 6) for i in range(num_dice))

    def build_settlement(self, is_special_round):
        """
        Builds a settlement at specified node, Can only build if player has enough resources
        """

        if not is_special_round:
            self.resources[Resource.BRICK.name()]-= 1
            self.resources[Resource.WOOD.name()]-=1
            self.resources[Resource.WOOL.name()]-=1
            self.resources[Resource.GRAIN.name()]-=1
        
    
       

    def build_city(self, node):
        """
        Builds a city at specified node
        only can build if a settlement is on the node
        """
        self.resources[Resource.ORE.name()]-=3
        self.resources[Resource.GRAIN.name()]-=2
        self.cities.append(node)
        

    def build_road(self, node1, node2, is_special_round):
        """
        Builds a road from node1 to node2. Road will be set to the color of the player building
        """
        if not is_special_round:
            self.resources[Resource.WOOD.name()]-=1
            self.resources[Resource.BRICK.name()]-=1
        
        self.roads.append((node1, node2))
        
        

    def buy_dev_card(self, card_name):
        """
        Buys a development card from the bank
        """

    def make_trade(self, resource, player):
        """Executes a trade of resources between two players

        :param resource: the resources being traded
        :type resource: list
        :param player: player names
        :type player: str
        """
        new_trade = Trade(self, resource, player)
        new_trade.execute_trade()

    def end_turn(self):
        """Ends a players turn
        """
        self.is_turn = False

    def get_resources(self):
        """Returns current players resources

        :return: list of resources
        :rtype: list
        """
        return self.resources

    def add_resource(self, resource):
        """Adds resources to players inventory

        :param resources: resources to be added
        :type resources: list
        """
        if resource in self.resources:
            self.resources[resource] +=1
        else:
            self.resources[resource] = 1

    def remove_resources(self, offered_resources):
        for resource, quantity in offered_resources.items():
            self.resources[resource] -= quantity

    def get_victory_points(self):
        """Returns current players victory points

        :return: Integer value of current victory point count for desired player
        :rtype: int
        """
        return self.victory_points

    def get_longest_road(self):
        """Displays current longest connected road built on the board

        :return: Integer value of longest constructed road
        :rtype: int
        """
        longest_road = self.roads[0].get_length()
        # TODO implement get_length() in Road class
        for road in self.roads[1:]:
            if road.get_length() > longest_road.get_length():
                road = longest_road

        return longest_road
