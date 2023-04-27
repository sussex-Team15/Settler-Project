from action import *
import random

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


class AIPlayer():
    def __init__(self, name, color):
        # Initializes AI player with a name, color, victory points, and various game state attributes
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

    def take_turn(self, game_state):
        # Given the current game state, generates all possible actions and chooses one to take
        actions = self.get_possible_actions(game_state)
        if not actions:
            return None
        return self.choose_action(actions)

    def get_possible_actions(self, game_state):
        # Given the current game state, generates all possible actions the player can take
        actions = []
        player_state = game_state.player_states[self.name]
        available_resources = player_state.resources.copy()
        # Adds all possible settlement or city building actions for each settlement
        for settlement in player_state.settlements:
            if settlement.is_city:
                actions += self._get_city_actions(settlement, game_state)
            else:
                actions += self._get_settlement_actions(settlement, game_state)
        # Adds all possible road building actions for each road
        for road in player_state.roads:
            actions += self._get_road_actions(road, game_state)
        # Adds all possible trade actions for each resource the player has
        for resource in available_resources:
            actions += self._get_trade_actions(resource, available_resources, game_state)
        return actions

    def _get_settlement_actions(self, settlement, game_state):
        # Given a settlement and current game state, returns all possible actions to build a settlement on a vertex adjacent to the settlement
        actions = []
        for node in settlement.adjacent_vertices: # TODO doesn't work
            if game_state.board.is_vertex_buildable(node):
                action = BuildSettlementAction(node)
                if game_state.is_valid_action(action):
                    actions.append(action)
        return actions

    def _get_city_actions(self, settlement, game_state):
        # Given a city and current game state, returns all possible actions to upgrade a settlement on a vertex adjacent to the city to a city
        actions = []
        for node in settlement.adjacent_vertices:
            if game_state.board.is_vertex_buildable(node):
                action = UpgradeSettlementAction(node)
                if game_state.is_valid_action(action):
                    actions.append(action)
        return actions

    def _get_road_actions(self, road, game_state):
        # Given a road and current game state, returns all possible actions to build a road on an edge adjacent to the road
        actions = []
        for edge in road.adjacent_edges:
            if game_state.board.is_edge_buildable(edge):
                action = BuildRoadAction(self.name, edge)
                if game_state.is_valid_action(action):
                    actions.append(action)
        return actions

    def _get_trade_actions(self, resource, available_resources, game_state):
        # Given a resource and current game state, returns all possible trade actions for trading the resource with another resource the player has
        actions = []
        for other_resource in available_resources:
            if resource != other_resource:
                action = TradeAction(self.name, resource, other_resource)
                if game_state.is_valid_action(action):
                    actions.append(action)
        return actions

    #Random Action
    def choose_action(self, actions):
        return random.choice(actions)

    #String Representation
    def __str__(self):
        return f"AI Player {self.name}"

