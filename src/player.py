import random
from trade import Trade


class Player:
    """
    Player class that controls the behaviour of an indivdual player of the game.
    Contains attributes such as the player name and number of VP'S.

    Attributes:
    
    - name : str
        String representing the name of the player
    - victory_points: int
        Integer representing the number of victory points the player has received.
    - color: tuple
        A tuple with an r,g,b value representing the color that the player has.
    - resources: list
        A list of resources that the player has (all of type Resource)
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
    - hasLargestArmy: boolean
        a boolean indicating if the player has the largest army
    - tradeOffers: list
        a list of tradeOffers that the player has received (of type Trade)


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
        activates a trade with the specified player offering the specified Resource
    - end_turn(self)
        ends player's turn
    - get_resources(self)
        returns list of resources player has
    - get_victory_points(self)
        returns number of victory points player has
    - get_longest_road(self):
        returns the longest road that the player currently has
    
    """

    def __init__(self, name):
        self.name = name
        self.victory_points = 0
        # TODO add implementation for self.color initialisation
        self.resources = []
        self.settlements = []
        self.cities = []
        self.roads = []
        self.isTurn = False
        self.hasLongestRoad = False
        self.hasLargestArmy = False
        self.tradeOffers = []

    def rollDice(self, numberOfDice=2):  # can be used for any number of dice (default =2)
        """
        simulates a dice roll

        Args:
            numberOfDice: number of dice to be rolled
        
        Returns: total sum of dice roll
        """
        return sum(random.randint(1, 6) for _ in range(numberOfDice))
    
    
    def build_settlement(self, location):
        
        pass

    def build_road(self, location1, location2):
        pass

    def buy_card(self):
        pass
    
    def make_trade(self, resource, player):
        new_trade = Trade(self, resource, player)
        new_trade.execute_trade()

    def end_turn(self):
        pass

    def get_resources(self):
        return self.resources
    
    def get_victory_points(self):
        return self.victory_points
    
    def get_longest_road(self):
        longest_road = self.roads[0].get_length() 
        # TODO implement get_length() in Road class
        for road in self.roads[1:]:
            if road.get_length()>longest_road.get_length():
                road = longest_road
        
        return longest_road


