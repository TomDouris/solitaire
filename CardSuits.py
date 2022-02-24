# CardSuits.py

from enum import Enum

class CardSuits(Enum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4

    def short_name(self):
        short_names = ['H','D','S','C']
        return short_names[self.value - 1]
