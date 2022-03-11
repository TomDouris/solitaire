# Card.py

import pygame
import traceback

import constants
from CardValues import CardValues
from CardSuits import CardSuits

class Card:

    #constructor
    def __init__(self,value,suit):

        #check for valid parameters

        if not isinstance(value, CardValues):
            raise TypeError(f"value is type {type(value)} not type CardValues, value:{value}")

        if not isinstance(suit, CardSuits):
            raise TypeError(f"suit is type {type(value)} not type CardSuits, suit:{suit}")

        self.value = value
        self.suit = suit

    # This method gets called when using == on the object
    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    # This method gets called when printing the object
    def __str__(self):
        return f'{self.value.short_name()}{self.suit.short_name()}'

    def draw(self, screen, location, face_up):

        if face_up:
            #fill
            color = constants.WHITE
            pygame.draw.rect(screen, color, [location.x, location.y, constants.CELL_WIDTH, constants.CELL_WIDTH],0)
            #border
            pygame.draw.rect(screen, constants.BLACK, 
                [location.x, location.y, constants.CELL_WIDTH,constants.CELL_WIDTH],1)

            #text
            font = pygame.font.SysFont(constants.FONT_ARIAL, int(round(constants.CELL_WIDTH*1/2,0)), True, False)
            valtext = str(self)
            if self.suit in(CardSuits.HEARTS,CardSuits.DIAMONDS):
                color = constants.RED
            else:
                color = constants.BLACK
            text = font.render(str(self), True, color)
            screen.blit(text, [location.x + constants.CELL_WIDTH/12, location.y])
        else:
            #fill
            pygame.draw.rect(screen, constants.BLUE,
                [location.x, location.y, constants.CELL_WIDTH, constants.CELL_WIDTH],0)
            #boarder
            pygame.draw.rect(screen, constants.BLACK,
                [location.x, location.y, constants.CELL_WIDTH, constants.CELL_WIDTH],1)
