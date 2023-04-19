class Bank:

    def __init__(self, resources, dev_cards):

        # not sure what bank starts with (to change)
        self.resources = resources
        self.trade_ratios = 4  # default trade ratio -
        # goes to 3 if player has settlement or trades on harbour
        # list as stack (only uses pop and push)
        self.dev_cards = dev_cards

    def get_trade_ratio(self, num_settlements):
        """_summary_

        :param num_settlements: _description_
        :type num_settlements: _type_
        :return: _description_
        :rtype: _type_
        """
        if num_settlements > 0:
            return 3
        return self.trade_ratios

    def null_method(self):
        return (
            self.resources,
            self.trade_ratios,
            self.dev_cards
        )
