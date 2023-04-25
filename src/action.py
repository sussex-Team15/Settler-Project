from trade import Trade
from building import Settlement, City
from resource_ import Resource

class Action:
    def __init__(self):
        pass

    def execute(self):
        pass

class BuildSettlementAction(Action):
    def __init__(self, node):
        self.settlements = []
        self.resources = []
        self.node = node

    def execute(self):
        settlement = Settlement(self, self.node)
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

class BuildRoadAction(Action):
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.roads = []
        self.resources = []

    def execute(self):
        """
        builds a road from node1 to node2.
        Road will be set to the color of the player building
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
            self.roads.append((self.node1, self.node2))
            print(f'road built from {self.node1} to {self.node2}')
        else:
            print("Not enough resources")

class UpgradeSettlementAction(Action):
    def __init__(self, node):
        self.node = node
        self.resources = []

    def execute(self):
        """
        Builds a city at specified node
        only can build if a settlement is on the node
        """
        city = City(self, self.node)
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

class TradeAction(Action):
    def __init__(self, offering_player, requesting_player, resource):
        self.offering_player = offering_player
        self.requesting_player = requesting_player
        self.resource = resource

    def execute(self):
        trade = Trade(self.offering_player, self.requesting_player, self.resource)
