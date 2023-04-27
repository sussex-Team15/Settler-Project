from src.resource_ import Resource

class Bank:

    def __init__(self):

        # not sure what bank starts with (to change)
        self.resources = {Resource.BRICK.name(): 19, 
                          Resource.WOOD.name(): 19,
                          Resource.WOOL.name(): 19,
                          Resource.GRAIN.name(): 19,
                          Resource.ORE.name(): 19}
        self.trade_ratio = 4  # default trade ratio - goes to 3 if player has settlement or trades on harbour

    def buy_from_bank(self, player, offered_resources, resource):
        """ purchases a resource from the bank

            Trades the offered resources for the resource

            :return: True if bank or player has required num of resources, else False
            :rtype: boolean
        """
        for resource in offered_resources:
            if resource not in player.resources or player.resources[resource]<4:
                return False # not enough resources 
            player.resources[resource]-=1
        
        if self.resources[resource]<=0:
            return False # bank doesnt have the resource wanted
        
        player.resources[resource]+=1
        self.resources[resource]-=1

        return True
    

    def null_method(self):
        return (
            self.resources,
            self.trade_ratio,
        )
