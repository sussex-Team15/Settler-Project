class Bank:
    """Bank class that controls behaviour of the bank in the game

    Attributes:

    :param resources: bank's resources
    :type resources: list
    :param trade_ratios: standard ratio for all players trading with the bank, 4 of the same card for one from the bank
    :type trade_ratios: int
    :param dev_cards: list of development cards in the bank's inventory
    :type dev_cards: list
    """
    def __init__(self, resources, dev_cards):
        """Constructor Method
        """
        # not sure what bank starts with (to change)
        self.resources = resources
        self.trade_ratios = 4  # default trade ratio -
        # goes to 3 if player has settlement or trades on harbour
        # list as stack (only uses pop and push)
        self.dev_cards = dev_cards

    def get_trade_ratio(self, num_settlements):
        """Returns the trade ratio as an integer value based on how many settlements are constructed.

        :param num_settlements: Current number of settlements constructed on the board
        :type num_settlements: int
        :return: The trade ratio as a number
        :rtype: int
        """
        if num_settlements > 0:
            return 3
        return self.trade_ratios

    def null_method(self):
        """Returns all current information about the bank

        :return: The current values of the bank's 'resources','trade_ratios' and 'dev_cards' inventory
        :rtype: Union[List[str],int]
        """
        return (
            self.resources,
            self.trade_ratios,
            self.dev_cards
        )
