import random

from src.trade import Trade
from src.building import Settlement, City
from src.resource_ import Resource


class Player:  # pylint: disable=too-many-instance-attributes
    """Player class that controls the behaviour of an indivdual player of the game. Contains attributes such as the player name and number of VP'S.

    :param name: String representing the name of the player
    :type name: str
    :param victory_points: Integer representing the number of victory points the player has received.
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
        


    Methods:

    - build_settlement(self, location)
        builds a settlement at the specified location
    - build_road(self, location1, location2)
        builds a road from location1 to location2
    - buy_dev_card(self,bank)
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
    - roll_dice(self,num_dice = 2)
        returns the values of both the rolled dice in a player's turn
    - get_resources(self)
        return player's current resources
    - add_resources(self, resources)
        add resources to player's inventory
    """

    def __init__(self, name, color):
        """Constructor Class
        """
        self.name = name
        self.victory_points = 0
        self.color = color
        self.resources = []
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

    def build_settlement(self, node):
        """
        Builds a settlement at specified node, Can only build if player has enough resources
        """
        settlement = Settlement(self, node)
        num_lumber, num_brick, num_wool, num_grain = 0, 0, 0, 0
        # cost = 1 lumber 1 brick 1 wool 1 grain

        for resource in self.resources:
            is_wood = resource == Resource.WOOD
            is_brick = resource == Resource.BRICK
            is_grain = resource == Resource.GRAIN
            is_wool = resource == Resource.WOOL
            if is_wood or is_brick or is_grain or is_wool:
                num_lumber += 1
                num_brick += 1
                num_grain += 1
                num_wool += 1

        if any([num_lumber >= 1,
                num_grain >= 1,
                num_brick >= 1,
                num_wool >= 1]):
            self.settlements.append(settlement)
        else:
            print('not enough resources')

    def build_city(self, node):
        """
        Builds a city at specified node
        only can build if a settlement is on the node
        """
        city = City(self, node)
        num_ore = 0
        num_grain = 0

        # check to see if player has enough resources for city
        for resource in self.resources:
            if resource == Resource.GRAIN:
                num_grain += 1
            elif resource == Resource.ORE:
                num_ore += 1

        if num_ore >= 3 and num_grain >= 2:
            # player has enough
            self.cities.append(city)
        else:
            print("Not enough resources")

    def build_road(self, node1, node2):
        """
        Builds a road from node1 to node2. Road will be set to the color of the player building
        """
        # cost 1 lumber 1 brick
        num_lumber = 0
        num_brick = 0

        # check to see if player has enough resources
        for resource in self.resources:
            if resource == Resource.WOOD:
                num_lumber += 1
            elif resource == Resource.BRICK:
                num_brick += 1

        if num_brick >= 1 and num_lumber >= 1:
            # player has enough
            self.roads.append((node1, node2))
            print(f'road built from {node1} to {node2}')
        else:
            print("Not enough resources")

    def buy_dev_card(self, bank):
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

    def add_resources(self, resources):
        """Adds resources to players inventory

        :param resources: resources to be added
        :type resources: list
        """
        self.resources.append(resources)

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
