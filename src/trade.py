# pylint: disable=missing-module-docstring
class Trade:
    """Trade Class that controls behaviour of all trading actions that occur within the game

    :param offering_player: Name of player offering resources
    :type offering_player: str, optional
    :param offered_resources: Resources offered by offering_player
    :type offered_resources: str, optional
    :param receiving_player: Name of player receiving offered_resources
    :type receiving_player: str, optional
    :param is_accepted: boolean value designating whether or not the offer has been accepted
    :type is_accepted: bool
    """

    def __init__(self, offering_player, offered_resources,
                 recieving_player):
        """Constructor Class
        """
        self.offering_player = offering_player
        self.offered_resources = offered_resources
        self.recieving_player = recieving_player
        self.is_accepted = False

    def accept_trade(self):
        """Returns true as the trade has been accepted

        :return: True statement
        :rtype: bool
        """
        self.is_accepted = True

    def cancel_trade(self):
        """Cancels trade between two players

        :return: A message displaying or not the trade has been accepted or not
        :rtype: Union[str, bool]
        """
        if not self.is_accepted:
            print('Must have accepted trade')
        else:
            self.is_accepted = False

    def get_offering_player(self):
        """Returns name of player offering resources to trade

        :return: Player name offering resources
        :rtype: Union[str, optional]
        """
        return self.offering_player

    def get_offered_resource(self):
        """Returns resources being offered to trade

        :return: resources to be traded
        :rtype: Union[str, optional]
        """
        return self.offered_resources

    def execute_trade(self):
        """Executes the trade process so that the 
        resources move from the offering_player to 
        the receiving_player and ensures the 
        offering_player no longer has the resources 
        available.
        """
        if self.is_accepted:
            # remove all offered resources from offering players resources
            for resource in self.offering_player.resources:
                if resource in self.offered_resources:
                    self.offering_player.resources.remove(resource)

            # add all offered resources to recipient players resources
            for resource in self.offered_resources:
                self.recieving_player.resources.append(resource)
