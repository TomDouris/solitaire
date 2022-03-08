# Game.py

import pygame

from Runnable import Runnable
import constants
from Events import Events
from KlondikeSolitaireBoard import KlondikeSolitaireBoard
from CardDeck import CardDeck

class Game(Runnable):

    def __init__(self, controller):
        self.controller = controller
        card_deck = CardDeck(controller.easy_game)
        if not controller.easy_game:
            card_deck.shuffle()
        self.board = KlondikeSolitaireBoard(self, card_deck)
        self.running = True

    def run(self):

        self.board.draw(self.controller.screen)
        while self.running:

            self.controller.check_events()

            if not self.controller.running:
                self.running = False
                break
            
            elif self.controller.event == Events.ESCAPE_KEY:
                self.running = False
                self.controller.run_object = self.controller.RunObject.MAIN_MENU

            elif self.controller.event == Events.LEFT_MOUSE_DOWN:
                self.board.left_mouse_down(self.controller.mouse_location)

            elif self.controller.event == Events.LEFT_MOUSE_UP:
                self.board.left_mouse_up(self.controller.mouse_location)
                self.board.draw(self.controller.screen)

            elif self.controller.event == Events.LEFT_MOUSE_MOTION:
                self.board.left_mouse_motion(self.controller.mouse_location)
                self.board.draw(self.controller.screen)

            elif self.controller.event == Events.CTRL_Z_KEY:
                self.board.undo()
                self.board.draw(self.controller.screen)

            if self.board.is_game_won():
                self.running = False
                self.controller.run_object = self.controller.RunObject.WIN_GAME
        
