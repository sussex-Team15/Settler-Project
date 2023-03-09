from random import *


def rollDice(numberOfDice):  # can be used for any number of dice
    return sum(randint(1, 6) for _ in range(numberOfDice))


result = rollDice(2)
