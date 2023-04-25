from action import *

class AIPlayer():
    def __init__(self, name, color):
        # Initializes AI player with a name, color, victory points, and various game state attributes
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
        for node in settlement.adjacent_vertices:
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

