from player import Player

class Trade:

    def __init__(self, offering_player, offered_resources,
                 recieving_player):
        self.offering_player = offering_player
        self.offered_resources = offered_resources
        self.recieving_player = recieving_player
        self.is_accepted = False
        
    
    def accept_trade(self):
        self.is_accepted = True
    
    def cancel_trade(self):
        if self.is_accepted == False:
            print('Must have accepted trade')
        else:
            self.is_accepted = False

    
    def get_offering_player(self):
        return self.offering_player
    
    def get_offered_resource(self):
        return self.offered_resources
    
    def execute_trade(self):
        if self.is_accepted:
            #remove all offered resources from offering players resources
            for resource in self.offering_player.resources:
                if resource in self.offered_resources:
                    self.offering_player.resources.remove(resource)

            # add all offered resources to recipient players resources

            self.recieving_player.resources.extend(self.offered_resources)


# tests:

Eddie = Player('Eddie')
Eddie.resources.extend([1,2,4,5,6,7,8,93]) # integers just for simplicity
Noah = Player('Noah')

new_trade = Trade(Eddie, Eddie.resources[:5], Noah)
new_trade.accept_trade()
new_trade.execute_trade()

print(f'Eddie Resources {Eddie.resources}')
print(f'Noah resources: {Noah.resources}')