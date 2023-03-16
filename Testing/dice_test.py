import pytest
import sys
from rollDice import rollDice

def test_rolldice():
    numDice = 2
    result = rollDice(numDice)
    

    assert 1 <= result <= 12


