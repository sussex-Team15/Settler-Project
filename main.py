from pprint import pprint
from Tiles import GameTile, ResourceTile
import os
import random
from hexgrid import legal_tile_ids
from development_cards import DevelopmentCards

resources = [
    ResourceTile.FOREST,
    ResourceTile.PASTURE,
    ResourceTile.FIELDS,
    ResourceTile.HILLS,
    ResourceTile.MOUNTAIN,
    ResourceTile.DESERT
]


def info(instance):

    print(f"Tile: {instance.tile_id}")
    print(f"Type: {instance.tile.name()}")
    print(f"Resource: {instance.tile.generate_resource().name()}")
    print(f"Label: {instance.number_label}")
    print()


available_tiles = list(legal_tile_ids())

board = [GameTile(random.randint(0, 12), random.choice(resources), 4, tile_id) for tile_id in available_tiles]

pprint(board)

Development_Cards = [
    DevelopmentCards.CHAPEL,
    DevelopmentCards.KNIGHT,
    DevelopmentCards.LARGEST_ARMY,
    DevelopmentCards.LIBRARY,
    DevelopmentCards.LONGEST_ROAD,
    DevelopmentCards.MARKET,
    DevelopmentCards.MONOPLY,
    DevelopmentCards.PALACE,
    DevelopmentCards.ROAD_BUILDING,
    DevelopmentCards.UNIVERSITY,
    DevelopmentCards.YEAR_OF_PLENTY
]
print()
pprint({x.name(): os.path.exists(x.asset()) for x in Development_Cards})
