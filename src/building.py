from resource_ import Resource


class Building:
    def __init__(self, owner, node):
        self.owner = owner
        self.node = node


class Settlement(Building):

    def __init__(self, owner, node):
        super().__init__(owner, node)
        self.cost = [Resource.BRICK, Resource.WOOL,
                     Resource.GRAIN, Resource.WOOD]

    def build_settlement(self, resources):
        enough_resource = all(
            [resource in resources for resource in self.cost])
        if enough_resource:
            # TODO: node needs to be object instance of a Node class
            self.node.has_settlement = True


class City(Building):

    def __init__(self, owner, node):
        super().__init__(owner, node)
        self.valid_node = False
        if self.node.has_settlement:
            self.valid_node = True
        self.cost = [Resource.GRAIN, Resource.GRAIN,
                     Resource.ORE, Resource.ORE, Resource.ORE]
