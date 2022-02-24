# Rules.py

import pygame

from Runnable import Runnable
import constants
from Events import Events
from Instructions import Instructions

class Rules:

    def __init__(self, controller):
        self.controller = controller
        self.running = True
        self.instructions = Instructions(constants.DEFAULT_INSTRUCTIONS)

    def run(self):
        self.controller.screen.fill(constants.GREEN)

        font = pygame.font.SysFont(constants.FONT_ARIAL, 40, True, False)
        text = font.render("Solitaire Rules", True, constants.BLACK)
        self.controller.screen.blit(text, [constants.FRAME_MAX_X*1/10, constants.FRAME_MAX_Y/5])

        font = pygame.font.SysFont(constants.FONT_ARIAL, 20, True, False)
        text = font.render("Coming Soon", True, constants.BLACK)
        self.controller.screen.blit(text, [constants.FRAME_MAX_X*2/10, constants.FRAME_MAX_Y*2/5])

        self.instructions.draw(self.controller.screen)

        pygame.display.flip()
        
        while self.running:
            self.controller.check_events()
            if not self.controller.running:
                self.running = False
                break
            self.check_input()

    def check_input(self):
        if self.controller.event == Events.ESCAPE_KEY:
            self.controller.run_object = self.controller.RunObject.MAIN_MENU
            self.running = False
