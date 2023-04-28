import random
from src.action import BuildRoadAction, BuildSettlementAction
from src.resource_ import Resource

from src.player import Player

class AIPlayer(Player):

    def take_turn(self, adjacent_nodes, board_mapping):
        # Given the current game state, generates all possible actions and chooses one to take
        actions = self.get_possible_actions(adjacent_nodes, board_mapping)
        if not actions:
            return None
        return self.choose_action(actions)

    def get_possible_actions(self, adjacent_nodes, board_mapping):
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

