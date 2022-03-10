# CardPile.py

import pygame

from Card import Card
from CardSuits import CardSuits
from Location import Location
import constants

class CardPile:

    #constructor
    def __init__(self, name, cards=None, location=Location(0,0)):

        #check for valid parameters
        if not cards is None:
            for card in cards:
                if not isinstance(card, Card):
                    raise TypeError(f'An element in cards is type {type(card)} is not type Card')
        if not isinstance(location, Location):
            raise TypeError(f'location is type {type(location)} is not type Location')
        self.name = name
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
        self.location = location
        self.selected_card = None
        self.second_click_move_from_allowed = False
        self.drag_from_allowed = False

    def __str__(self):
        string_value = f'{self.name} cards:'
        for card in self.cards:
            string_value = string_value + ' ' + str(card)
        string_value = string_value + ' location:' + str(self.location)
        return string_value

    def __len__(self):
        return len(self.cards)

    def draw(self, screen, selected_card=None, selected_card_location=None):             # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")

    def doubleclick(self, location):
        return False

    def is_valid_move_to(self, from_pile, card):
       return False

    def deselect_card(self):
        if not self.selected_card is None:
            self.selected_card.selected = False

    def selected(self, location):
        return False, None, None

    def intercects(self, other_rect):
        return False

class WastePile(CardPile):

    def __init__(self, name, cards=None, location=Location(0,0)):
        CardPile.__init__(self, name, cards, location)
        self.cards_to_display = 0
        self.second_click_move_from_allowed = True
        self.drag_from_allowed = False

    def draw(self, screen, selected_card=None, selected_card_location=None):
        if len(self.cards) > 0:
            for i in range(self.cards_to_display):
                card = self.cards[len(self.cards)-self.cards_to_display + i]
                card_location = Location(self.location.x + constants.CELL_WIDTH*2/3*i, self.location.y)
                if not selected_card is None and not selected_card_location is None:
                    if selected_card == card:
                        card_location = selected_card_location
                card.draw(screen, card_location, True)

    def selected(self, location):
        if self.cards_to_display > 0:
            last_card_location = Location(self.location.x + constants.CELL_WIDTH*2/3*(self.cards_to_display-1), self.location.y)
            if ((location.x >= last_card_location.x) and
                (location.x <= (last_card_location.x + constants.CELL_WIDTH)) and
                (location.y >= last_card_location.y) and
                (location.y <= (last_card_location.y + constants.CELL_WIDTH))):
                    my_rect = pygame.Rect(last_card_location.x, last_card_location.y, constants.CELL_WIDTH, constants.CELL_WIDTH)
                    return True, self.cards[-1], my_rect
        return False, None, None

class StockPile(CardPile):

    def __init__(self, name, cards=None, location=Location(0,0)):
        CardPile.__init__(self, name, cards, location)

    def draw(self, screen, selected_card=None, selected_card_location=None):
        if len(self.cards) > 0:
            # display top card
            self.cards[len(self.cards)-1].draw(screen, self.location, False)
        else:
            # display boarder if there are no cards in pile
            pygame.draw.rect(screen, constants.BLUE,
                [self.location.x, self.location.y, constants.CELL_WIDTH, constants.CELL_WIDTH],1)

    def selected(self, location):
        if ((location.x >= self.location.x) and
            (location.x <= (self.location.x + constants.CELL_WIDTH)) and
            (location.y >= self.location.y) and
            (location.y <= (self.location.y + constants.CELL_WIDTH))):
            return True, None, None
        else:
            return False, None, None

class FoundationPile(CardPile):

    def __init__(self, name, cards=None, location=Location(0,0)):
        CardPile.__init__(self, name, cards, location)

    def draw(self, screen, selected_card=None, selected_card_location=None):
        if len(self.cards) > 0:
            self.cards[len(self.cards)-1].draw(screen, self.location, True)
        else:
            # display boarder if there are no cards in pile
            pygame.draw.rect(screen, constants.BLUE,
                [self.location.x, self.location.y, constants.CELL_WIDTH, constants.CELL_WIDTH],1)

    def selected(self, location):
        if ((location.x >= self.location.x) and
            (location.x <= (self.location.x + constants.CELL_WIDTH)) and
            (location.y >= self.location.y) and
            (location.y <= (self.location.y + constants.CELL_WIDTH))):
            return True, None, None
        else:
            return False, None, None

    def intercects(self, other_rect):
        my_rect = pygame.Rect(self.location.x, self.location.y, constants.CELL_WIDTH, constants.CELL_WIDTH)
        return my_rect.colliderect(other_rect)

    def is_valid_move_to(self, from_pile, card):

        if card is None:
            return False

        # can only move last card from TableauFaceUpPile
        if isinstance(from_pile, TableauFaceUpPile):
            if not (from_pile.selected_card_index == len(from_pile) - 1):
                return False

        if len(self.cards) == 0:
            if card.value.value == 1:
                return True
        else:
            if self.cards[-1].suit == card.suit and self.cards[-1].value.value + 1 == card.value.value:
                return True

        return False
 
class TableauFaceDownPile(CardPile):

    def __init__(self, name, cards=None, location=Location(0,0)):
        CardPile.__init__(self, name, cards, location)

    def draw(self, screen, selected_card=None, selected_card_location=None):
        if len(self.cards) > 0:
            for i, card in enumerate(self.cards):
                card_location = Location(self.location.x, self.location.y + round(constants.CELL_WIDTH/5)*i)
                card.draw(screen, card_location, False)
        else:
            # display boarder if there are no cards in pile
            pygame.draw.rect(screen, constants.BLUE,
                [self.location.x, self.location.y, constants.CELL_WIDTH, constants.CELL_WIDTH],1)

class TableauFaceUpPile(CardPile):

    def __init__(self, name, my_face_down_pile, cards=None, location=Location(0,0)):
        CardPile.__init__(self, name, cards, location)
        self.selected_card_index = -1
        self.my_face_down_pile = my_face_down_pile
        self.second_click_move_from_allowed = True
        self.drag_from_allowed = False

    def draw(self, screen, selected_card=None, selected_card_location=None):
        mylocation = Location(self.my_face_down_pile.location.x,
        self.my_face_down_pile.location.y + round(constants.CELL_WIDTH/5)*len(self.my_face_down_pile))
        for i, card in enumerate(self.cards):
            card_location = Location(mylocation.x, mylocation.y + round(constants.CELL_WIDTH*2/3)*i)
            if not selected_card is None and not selected_card_location is None:
                if selected_card == card:
                    card_location = selected_card_location
            card.draw(screen, card_location, True)

    def selected(self, location):
        mylocation = Location(self.my_face_down_pile.location.x,
        self.my_face_down_pile.location.y + round(constants.CELL_WIDTH/5)*len(self.my_face_down_pile))
        if len(self.cards) == 0:
            if ((location.x >= mylocation.x) and
                (location.x <= (mylocation.x + constants.CELL_WIDTH)) and
                (location.y >= mylocation.y) and
                (location.y <= (mylocation.y + constants.CELL_WIDTH))):
                return True, None, None
        for i,card in enumerate(self.cards):
            card_location = Location(mylocation.x, mylocation.y + round(constants.CELL_WIDTH*2/3)*i)
            if (i == len(self.cards)-1):        # last card is a little larger
                if ((location.x >= card_location.x) and
                    (location.x <= (card_location.x + constants.CELL_WIDTH)) and
                    (location.y >= card_location.y) and
                    (location.y <= (card_location.y + constants.CELL_WIDTH))):
                    self.selected_card_index = i
                    my_rect = pygame.Rect(card_location.x, card_location.y, constants.CELL_WIDTH, constants.CELL_WIDTH)
                    return True, card, my_rect
            else:
                if ((location.x >= card_location.x) and
                    (location.x <= (card_location.x + constants.CELL_WIDTH)) and
                    (location.y >= card_location.y) and
                    (location.y <= (card_location.y + constants.CELL_WIDTH*2/3))):
                    self.selected_card_index = i
                    offset = Location(location.x - card_location.x, location.y - card_location.y)
                    return True, card, None
        return False, None, None

    def intercects(self, other_rect):
        if len(self.my_face_down_pile) == 0:
            top_card_location = Location(self.my_face_down_pile.location.x, self.my_face_down_pile.location.y)
        else:
            mylocation = Location(self.my_face_down_pile.location.x,
                self.my_face_down_pile.location.y + round(constants.CELL_WIDTH/5)*len(self.my_face_down_pile))
            top_card_location = Location(mylocation.x, mylocation.y + round(constants.CELL_WIDTH)*(len(self.cards)-1))
        my_rect = pygame.Rect(top_card_location.x, top_card_location.y, constants.CELL_WIDTH, constants.CELL_WIDTH)
        return my_rect.colliderect(other_rect)



    def is_valid_move_to(self, from_pile, card):

        if card is None:
            return False

        if len(self.cards) == 0:
            if card.value.value == 13:
                return True
        else:
            top_card = self.cards[-1]
            if ((top_card.suit in (CardSuits.HEARTS,CardSuits.DIAMONDS) and card.suit in (CardSuits.CLUBS,CardSuits.SPADES)) or
                (top_card.suit in (CardSuits.CLUBS,CardSuits.SPADES) and card.suit in (CardSuits.HEARTS,CardSuits.DIAMONDS))):
                if (top_card.value.value == card.value.value + 1):
                   return True
        return False
