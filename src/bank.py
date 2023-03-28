from trade import Trade
from development_cards import DevelopmentCard
from resource_ import *

class Bank:

    def __init__(self, resources, trade_ratios, dev_cards, vp_cards):

        self.resources = resources #not sure what bank starts with (to change)
        self.trade_ratios = 4 # default trade ratio - 
        #goes to 3 if player has settlement or trades on harbour
        self.dev_cards  = [] # list as stack (only uses pop and push)
    

    def get_trade_ratio(self, num_settlements):
        if num_settlements>0:
            return 3
        return self.trade_ratios
