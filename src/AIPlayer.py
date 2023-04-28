import random
from src.action import BuildRoadAction, BuildSettlementAction
from src.resource_ import Resource
from src.main_refactored import adjacent_nodes, board_mapping

class AIPlayer():
    """
    AIPlayer Class that controls the behavior of an AI player in the game.
    Attributes:

    - name : str
        String representing the name of the player

    - victory_points: int
        Integer representing the number of victory points the player has received.

    - color: tuple
        A tuple with an r,g,b value representing the color that the player has.

    - resources: dict
        a dictionary of resource type string mapped to the amount the player has

    - settlements: list
        a list of settlements the player has

    - cities: list
        a list of cities the player has

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
    -take_turn(self, game_state)
        The aiplayer will take its turn

    -get_possible_actions(self, game_state)
        Given the current game state, generates all possible actions the player can take

    -_get_settlement_actions(self, settlement, game_state)
        returns all possible actions on a vertex adjacent to the settlement

    -_get_city_actions(self, settlement, game_state)
        Returns all possible actions that upgrade a settlement into a city

    -_get_trade_actions(self, resource, available_resources, game_state)
        Returns all possible actions for trading a resource given with another resource the player has

    -choose_action(self, action)
        Randomly chooses an action from the array0

    -__str__(self)
        Returns a string representation of the AIPlayer

    """
    def __init__(self, name, color):
        # Initializes AI player with a name, color, victory points, and various game state attributes
        self.name = name
        self.victory_points = 0
        self.color = color
        self.resources = {resource.name(): 0 for resource in Resource if not resource.name() == None}
        self.settlements = []
        self.roads = []
        self.has_longest_road = False
        self.total_road_num = 0
        self.has_largest_army = False

    def add_road(self, road):
        self.roads.append(road)

    def add_settlement(self, settlement):
        self.settlements.append(settlement)

    def take_turn(self):
        # Given the current game state, generates all possible actions and chooses one to take
        actions = self.get_possible_actions()
        if not actions:
            return None
        return self.choose_action(actions)

    def get_possible_actions(self):
        # Given the current game state, generates all possible actions the player can take
        actions = []
        # Adds all possible settlement or city building actions for each settlement
        for node in board_mapping.board_mapping["nodes"]:
            actions += self._get_settlement_actions(node)
        # Adds all possible road building actions for each road
        actions += self._get_road_actions(adjacent_nodes.adjacent_nodes)
        # Adds all possible trade actions for each resource the player has
        return actions

    def _get_settlement_actions(self, all_nodes):
        # Given a settlement and current game state, returns all possible actions to build a settlement on a vertex adjacent to the settlement
        actions = []
        for node in all_nodes:
            action = BuildSettlementAction(node, self)
            actions.append(action)
        return actions

    def _get_road_actions(self, all_roads):
        # Given a road and current game state, returns all possible actions to build a road on an edge adjacent to the road
        actions = []
        for road in all_roads.adjacent_edges:
            current_road = all_roads[road]
            node1, node2 = current_road[0], current_road[1]
            action = BuildRoadAction(node1, node2, self)
            actions.append(action)
        return actions

    #Random Action
    def choose_action(self, actions):
        return random.choice(actions)

    #String Representation
    def __str__(self):
        return f"AI Player {self.name}"

