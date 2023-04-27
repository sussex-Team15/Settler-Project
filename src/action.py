from src.building import Settlement
from src.resource_ import Resource

class Action:
    def __init__(self):
        pass

    def execute(self):
        pass

class BuildSettlementAction(Action):
    def __init__(self, node, ai_player):
        self.node = node
        self.ai_player = ai_player
        self.resources = ai_player.get_resources()

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
            self.ai_player.add_settlement(settlement)
        else:
            print('not enough resources')

class BuildRoadAction(Action):
    def __init__(self, node1, node2, ai_player):
        self.node1 = node1
        self.node2 = node2
        self.ai_player = ai_player
        self.resources = ai_player.get_resources()

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
            self.ai_player.add_road((self.node1, self.node2))
            print(f'road built from {self.node1} to {self.node2}')
        else:
            print("Not enough resources")
