from Tiles import ResourceTile


Tile_1 = ResourceTile.MOUNTAIN

print(Tile_1)
print(Tile_1.name())
print(Tile_1.short_name())
print(Tile_1.asset())

print()

resource = Tile_1.generate_resource()
if resource is not None:
    print(resource.asset())
else:
    print(None)
