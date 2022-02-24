# CardValues.py

from enum import Enum

class CardValues(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def short_name(self):
        short_names = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        return short_names[self.value - 1]
