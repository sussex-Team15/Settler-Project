from enum import Enum


class PieceType(Enum):
    settlement = 'settlement'
    road = 'road'
    city = 'city'
    robber = 'robber'


class Piece(object):
    def __init__(self, type, player):
        self.type = type
        self.player = player

    def __repr__(self):
        return f'Piece({self.type}, {self.player})'
