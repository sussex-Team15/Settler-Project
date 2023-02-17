from Tiles import ResourceTile
import os


Resources = [
    ResourceTile.FOREST,
    ResourceTile.PASTURE,
    ResourceTile.FIELDS,
    ResourceTile.HILLS,
    ResourceTile.MOUNTAIN,
    ResourceTile.DESERT
]

for tile in Resources:
    Tile_1 = tile
    print()
    print(Tile_1.name())
    print(Tile_1.asset())
    print(os.path.exists(Tile_1.asset()))
    resource = Tile_1.generate_resource()
    if resource is not None:
        print(resource.asset())
        print(os.path.exists(resource.asset()))
    else:
        print(None)
