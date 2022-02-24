# CardDeck.py

import random

from Card import Card
from CardValues import CardValues
from CardSuits import CardSuits

class CardDeck:

#constructor
    def __init__(self, easy_game=False):
        self.cards = []
        if easy_game:
            self._make_easy_deck()
        else:
            for suit in CardSuits:
                for value in CardValues:
                    self.cards.append(Card(value,suit))

    def __str__(self):
        string_value = 'cards:'
        for card in self.cards:
            string_value = string_value + ' ' + str(card)
        return string_value

    def __len__(self):
        return len(self.cards)

    def _make_easy_deck(self):
        self.cards.append(Card(CardValues.QUEEN, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.KING, CardSuits.SPADES))
        self.cards.append(Card(CardValues.ACE, CardSuits.SPADES))

        self.cards.append(Card(CardValues.JACK, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.FIVE, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.SIX, CardSuits.CLUBS))

        self.cards.append(Card(CardValues.EIGHT, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.SEVEN, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.SIX, CardSuits.HEARTS))

        self.cards.append(Card(CardValues.KING, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.FIVE, CardSuits.SPADES))
        self.cards.append(Card(CardValues.JACK, CardSuits.SPADES))

        self.cards.append(Card(CardValues.FOUR, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.EIGHT, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.SEVEN, CardSuits.SPADES))

        self.cards.append(Card(CardValues.QUEEN, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.NINE, CardSuits.SPADES))
        self.cards.append(Card(CardValues.TEN, CardSuits.SPADES))

        self.cards.append(Card(CardValues.FOUR, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.FOUR, CardSuits.SPADES))
        self.cards.append(Card(CardValues.THREE, CardSuits.SPADES))

        self.cards.append(Card(CardValues.THREE, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.THREE, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.TWO, CardSuits.CLUBS))

        self.cards.append(Card(CardValues.KING, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.EIGHT, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.SEVEN, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.SIX, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.FIVE, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.FOUR, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.ACE, CardSuits.CLUBS))

        self.cards.append(Card(CardValues.QUEEN, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.JACK, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.TEN, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.NINE, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.EIGHT, CardSuits.SPADES))
        self.cards.append(Card(CardValues.SEVEN, CardSuits.DIAMONDS))

        self.cards.append(Card(CardValues.JACK, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.ACE, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.TWO, CardSuits.SPADES))
        self.cards.append(Card(CardValues.KING, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.QUEEN, CardSuits.SPADES))

        self.cards.append(Card(CardValues.TEN, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.TWO, CardSuits.DIAMONDS))
        self.cards.append(Card(CardValues.TEN, CardSuits.HEARTS))
        self.cards.append(Card(CardValues.NINE, CardSuits.HEARTS))

        self.cards.append(Card(CardValues.NINE, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.SIX, CardSuits.SPADES))
        self.cards.append(Card(CardValues.FIVE, CardSuits.HEARTS))

        self.cards.append(Card(CardValues.THREE, CardSuits.CLUBS))
        self.cards.append(Card(CardValues.ACE, CardSuits.DIAMONDS))

        self.cards.append(Card(CardValues.TWO, CardSuits.HEARTS))


    def deal(self, number_of_cards, pile):
        # check for valid parameters
        if number_of_cards > len(self.cards):
            raise ValueError(f'number_of_cards is greater than number of cards in pile. number_of_cards:{number_of_cards},\
                pile length:{len(self.cards)}')
        # verify that pile is type CardPile

        for i in range(number_of_cards):
            card = self.cards.pop()
            pile.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)
