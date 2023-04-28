class Board:
    def __init__(self):
        self.tiles = []
        self.ports = []
        self.roads = []
        self.settlements = []
        self.cities = []

    def add_tile(self, tile):  # add tile
        self.tiles.append(tile)

    def add_port(self, port):  # TODO are we using ports?
        self.ports.append(port)

    def add_road(self, road):  # TODO unsure how roads work in implementation
        self.roads.append(road)

    def add_settlement(self, settlement):  # add settlement to array
        self.settlements.append(settlement)

    def add_city(self, city):  # add city to array
        self.cities.append(city)
