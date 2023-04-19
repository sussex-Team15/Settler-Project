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
        if not self.is_accepted:
            print('Must have accepted trade')
        else:
            self.is_accepted = False

    def get_offering_player(self):
        return self.offering_player

    def get_offered_resource(self):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        return self.offered_resources

    def execute_trade(self):
        if self.is_accepted:
            # remove all offered resources from offering players resources
            for resource in self.offering_player.resources:
                if resource in self.offered_resources:
                    self.offering_player.resources.remove(resource)

            # add all offered resources to recipient players resources
            for resource in self.offered_resources:
                self.recieving_player.resources.append(resource)
