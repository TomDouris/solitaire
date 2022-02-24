# Menu.py

import pygame
from enum import Enum
from collections import OrderedDict

from Runnable import Runnable
from Events import Events
import constants
from Location import Location
from Instructions import Instructions

class Menu(Runnable):
    def __init__(self, controller):
        self.controller = controller
        self.mid_w = self.controller.DISPLAY_SIDE_LEN / 2
        self.mid_h = self.controller.DISPLAY_SIDE_LEN / 2
        self.running = True

    def blit_screen(self):
        self.controller.screen.blit(self.controller.screen, (0,0))
        pygame.display.update()


class MainMenu(Menu):

    class MenuItem(Enum):
        START_GAME = 1
        STATISTICS = 2
        RULES = 3
        ABOUT = 4

    def __init__(self, controller):
        Menu.__init__(self, controller)
        self.selected_menu_item = self.MenuItem.START_GAME
        self.menu_item_dict = OrderedDict()
        self.menu_item_dict[self.MenuItem.START_GAME] = [['Start Game', constants.FONT_COMIC, 30, Location(self.mid_w, self.mid_h -30)],
                                                         self.MenuItem.STATISTICS, self.MenuItem.ABOUT, self.controller.RunObject.GAME]
        self.menu_item_dict[self.MenuItem.STATISTICS] = [['Statistics', constants.FONT_COMIC, 30, Location(self.mid_w, self.mid_h )],
                                                         self.MenuItem.RULES, self.MenuItem.START_GAME, self.controller.RunObject.STATISTICS]
        self.menu_item_dict[self.MenuItem.RULES] = [['Rules', constants.FONT_COMIC, 30, Location(self.mid_w, self.mid_h + 30)],
                                                         self.MenuItem.ABOUT, self.MenuItem.STATISTICS, self.controller.RunObject.RULES]
        self.menu_item_dict[self.MenuItem.ABOUT] = [['About', constants.FONT_COMIC, 30, Location(self.mid_w, self.mid_h + 60)],
                                                         self.MenuItem.START_GAME, self.MenuItem.RULES, self.controller.RunObject.ABOUT]
        self.instructions = Instructions(constants.MAIN_MENU_INSTRUCTIONS)

    def run(self):
        self.display_menu()
        while self.running:
            self.controller.check_events()
            if not self.controller.running:
                self.running = False
                break
            if self.controller.event == Events.ESCAPE_KEY:
                self.running = False
                self.controller.running = False
            if self.controller.event == Events.DOWN_KEY:
                self.selected_menu_item = self.menu_item_dict[self.selected_menu_item][1]
                self.display_menu()
            if self.controller.event == Events.UP_KEY:
                self.selected_menu_item = self.menu_item_dict[self.selected_menu_item][2]
                self.display_menu()
            if self.controller.event == Events.RETURN_KEY:
                self.controller.run_object = self.menu_item_dict[self.selected_menu_item][3]
                self.running = False
            self.controller.event = None

    def display_menu(self):
        self.controller.screen.fill(constants.GREEN)

        self.controller.draw_text('Main Menu', constants.FONT_ARIAL, 40, Location(self.controller.DISPLAY_SIDE_LEN / 2, constants.FRAME_MAX_Y/5), constants.BLACK)

        for menu_item, menu_item_value in self.menu_item_dict.items():
            if menu_item == self.selected_menu_item:
                color = constants.BLACK
            else:
                color = constants.WHITE
            self.controller.draw_text(*menu_item_value[0], color)

        self.instructions.draw(self.controller.screen)

        self.blit_screen()
