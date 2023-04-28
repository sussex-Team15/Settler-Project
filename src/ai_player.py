import random
from src.action import BuildRoadAction, BuildSettlementAction
from src.resource_ import Resource

from src.player import Player

class AIPlayer(Player):
    """
    AIPlayer Class that controls the behavior of an AI player in the game.
    Attributes

    :param name : String representing the name of the player
    :type name: str
    :param victory_points: Integer representing the number of victory points the player has received.
    :type victory_points: int
    :param color: A tuple with an r,g,b value representing the color that the player has.
    :type color: tuple
    :param resources: a dictionary of resource type string mapped to the amount the player has
    :type resources: dict
    :param settlements: a list of settlements the player has
    :type settlements: list
    :param cities: a list of cities the player has
    :type cities: list
    :param roads: a list of roads the player has (all of type Road)
    :type roads: list
    :param isTurn: a boolean indicating if it is the players turn in the gameloop.
    :type isTurn: boolean
    :param hasLongestRoad: a boolean indicating if the player has the longest road.
    :type hasLongestRoad: boolean
    :param has_largest_army: a boolean indicating if the player has the largest army
    :type has_largest_army: boolean
    :param trade_offers: a list of trade_offers that the player has received (of type Trade)
    :type trade_offers: list
    """
    def take_turn(self, adjacent_nodes, board_mapping, node_buttons):
        """Constructor Class
        """
        # Given the current game state, generates all possible actions and chooses one to take
        actions = self.get_possible_actions(adjacent_nodes, board_mapping, node_buttons)
        if not actions:
            return None
        return self.choose_action(actions)

    def get_possible_actions(self, adjacent_nodes, board_mapping, node_buttons):
        """
        Given the current game state, generates all possible actions the player can take. This includes
        settlement or city building actions, road building actions, and trade actions.

        :return: A list of possible actions.
        :rtype: list[Action]
        """
        # Given the current game state, generates all possible actions the player can take
        actions = []
        # Adds all possible settlement or city building actions for each settlement
        for node_button in node_buttons:
            actions += self._get_settlement_actions(node_button)
        # Adds all possible road building actions for each road
        actions += self._get_road_actions(adjacent_nodes[0])
        # Adds all possible trade actions for each resource the player has
        return actions
    


    def _get_settlement_actions(self, all_nodes):
        """
        Given a settlement and current game state, returns all possible actions to build a settlement on a vertex adjacent to the settlement.

        :param all_nodes: A list of all nodes on the board.
        :type all_nodes: list[Node]
        :return: A list of possible actions to build a settlement.
        :rtype: list[BuildSettlementAction]
        """
        # Given a settlement and current game state, returns all possible actions to build a settlement on a vertex adjacent to the settlement
        actions = []
        for node in all_nodes:
            action = BuildSettlementAction(node, self)
            actions.append(action)
        return actions

    def _get_road_actions(self, all_roads):
        """
        Given a road and current game state, returns all possible actions to build a road on an edge adjacent to the road.

        :param all_roads: A list of all roads on the board.
        :type all_roads: list[Road]
        :return: A list of possible actions to build a road.
        :rtype: list[BuildRoadAction]
        """
        # Given a road and current game state, returns all possible actions to build a road on an edge adjacent to the road
        actions = []
        for road in all_roads:
            current_road = all_roads[road]
            node1, node2 = current_road[0], current_road[1]
            action = BuildRoadAction(node1, node2, self)
            actions.append(action)
        return actions

    #Random Action
    def choose_action(self, actions):
        """
        Chooses an action randomly from a list of possible actions.

        :param actions: A list of possible actions.
        :type actions: list[Action]
        :return: The chosen action.
        :rtype: Action
        """
        return random.choice(actions)

    #String Representation
    def __str__(self):
        """
        Returns the string representation of the AI player.

        :return: The string representation of the AI player.
        :rtype: str
        """
        return f"AI Player {self.name}"

