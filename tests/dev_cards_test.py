# pylint: disable=missing-module-docstring
from src.development_cards import DevelopmentCards


def test_chapel():
    """Test the Chapel Development Card"""
    chapel = DevelopmentCards.CHAPEL
    assert chapel.description() == "+1 Victory Point"
    assert chapel.vp_awarded() == 1


def test_knight():
    """Test the Knight Development Card"""
    knight = DevelopmentCards.KNIGHT
    assert knight.description() == (
        "Move the Robber. Steal 1 resource card "
        "from the owner of an adjacent settlement"
    )
    assert knight.vp_awarded() == 0


def test_largest_army():
    """Test the Largest Army Development Card"""
    largest_army = DevelopmentCards.LARGEST_ARMY
    assert largest_army.description() == (
        "The first player to play 3 Knight "
        "cards gets this card. Another "
        "player who plays more Knight "
        "cards will take this card"
    )
    assert largest_army.vp_awarded() == 2


def test_library():
    """Test the Library Development Card"""
    library = DevelopmentCards.LIBRARY
    assert library.description() == "+1 Victory Point"
    assert library.vp_awarded() == 1


def test_longest_road():
    """Test the Longest Road Development Card"""
    longest_road = DevelopmentCards.LONGEST_ROAD
    assert longest_road.description() == (
        "This Card Goes to the player with "
        "the longes unbroken road of at "
        "least 5 segments. Another player "
        "who builds a longer Road will "
        "take this card"
    )
    assert longest_road.vp_awarded() == 2


def test_market():
    """Test the Market Development Card"""
    market = DevelopmentCards.MARKET
    assert market.description() == "+1 Victory Point"
    assert market.vp_awarded() == 1


def test_monopoly():
    """Test the Monopoly Development Card"""
    monopoly = DevelopmentCards.MONOPLY
    assert monopoly.description() == (
        "When you play this card, announce 1 "
        "type of resource. All other players "
        "must give you all their resource "
        "cards of that type"
    )
    assert monopoly.vp_awarded() == 0


def test_palace():
    """Test the Palace Development Card"""
    palace = DevelopmentCards.PALACE
    assert palace.description() == "+1 Victory Point"
    assert palace.vp_awarded() == 1


def test_road_building():
    """Test the Road Building Development Card"""
    road_building = DevelopmentCards.ROAD_BUILDING
    assert road_building.description() == (
        "Place 2 new roads as if you" " had just built them"
    )
    assert road_building.vp_awarded() == 0


def test_university():
    """Test the University Development Card"""
    university = DevelopmentCards.UNIVERSITY
    assert university.description() == "+1 Victory Point"
    assert university.vp_awarded() == 1


def test_year_of_plenty():
    """Test the Year of Plenty Development Card"""
    year_of_plenty = DevelopmentCards.YEAR_OF_PLENTY
    assert year_of_plenty.description() == (
        "take any 2 resources from the "
        "bank add them to your hand. They "
        "can be 2 of the same resource "
        "or 2 different resources"
    )
    assert year_of_plenty.vp_awarded() == 0
