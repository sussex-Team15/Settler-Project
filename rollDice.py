from random import *

def rollDice(numberOfDice): #can be used for any number of dice
    result = 0 #store total here
    for i in range(0, numberOfDice):
        number = randint(1,6)
        print("The dice has rolled a",number,)#print the individual die scores
        result += number
    return result

result = rollDice(2)
