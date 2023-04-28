# pylint: disable=missing-module-docstring
from src.resource_ import Resource


class Bank:
    """Bank class that controls behaviour of the bank in the game

    :param resources: bank's resources
    :type resources: list
    :param trade_ratios: standard ratio for all players
    trading with the bank, 4 of the same card for one
    from the bank
    :type trade_ratios: int
    :param dev_cards: list of development cards in the bank's inventory
    :type dev_cards: list

    """

    def __init__(self):
        """Constructor Method"""
        # not sure what bank starts with (to change)
        self.resources = {
            Resource.BRICK.name(): 19,
            Resource.WOOD.name(): 19,
            Resource.WOOL.name(): 19,
            Resource.GRAIN.name(): 19,
            Resource.ORE.name(): 19,
        }
        self.trade_ratio = 4  # default trade ratio - goes to 3 if player has settlement or trades on harbour

    def buy_from_bank(self, player, offered_resources, resource):
        """purchases a resource from the bank

        Trades the offered resources for the resource

        :return: True if bank or player has required num of resources, else False
        :rtype: boolean
        """
        for resource in offered_resources:
            if (
                resource not in player.resources
                or player.resources[resource] < 4
            ):
                return False  # not enough resources
            player.resources[resource] -= 1

        if self.resources[resource] <= 0:
            return False  # bank doesnt have the resource wanted

        player.resources[resource] += 1
        self.resources[resource] -= 1

        return True

    def null_method(self):
        """Returns all current information about the bank

        :return: The current values of the bank's 'resources',
        'trade_ratios' and 'dev_cards' inventory
        :rtype: Union[List[str],int]
        """
        return (
            self.resources,
            self.trade_ratio,
        )
