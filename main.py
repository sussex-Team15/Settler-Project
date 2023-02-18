from pprint import pprint
from Tiles import GameTile, ResourceTile
import os
import random
from hexgrid import legal_tile_ids

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
    # print(instance.get_tile_info())
    print()


available_tiles = list(legal_tile_ids())
# print(available_tiles)

board = [GameTile(random.randint(0, 12), random.choice(resources), 4, tile_id) for tile_id in available_tiles]

pprint(board)
print()
print()
for tile in board:
    info(tile)
    print(tile.get_tile_info())
