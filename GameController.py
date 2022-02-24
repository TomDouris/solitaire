# GameController.py

import pygame
from enum import Enum
import json

from Events import Events
from Game import Game
from WinGame import WinGame
from Location import Location

import constants

from Menu import *
from Rules import Rules
from SolitaireStatistics import SolitaireStatistics
from About import About

class GameController:

    class RunObject(Enum):
        MAIN_MENU = 1
        STATISTICS = 2
        RULES = 3
        ABOUT = 4
        GAME = 5
        WIN_GAME = 6

        def run_class(self):
            run_classes = [MainMenu, SolitaireStatistics, Rules, About, Game, WinGame]
            return run_classes[self.value - 1]


    def __init__(self, args):
        self._parse_args(args)
        self._parse_jsonfile()
        pygame.init()
        self.running = True
        self.event = None

        self.DISPLAY_SIDE_LEN = min(pygame.display.Info().current_w-60, pygame.display.Info().current_h-60, constants.FRAME_SIDE_MAX_PIXELS)
        self.CELL_SIDE_LEN = int(round(self.DISPLAY_SIDE_LEN/20))
        self.screen = pygame.display.set_mode((self.DISPLAY_SIDE_LEN, self.DISPLAY_SIDE_LEN))

        pygame.display.set_caption('Solitaire')
        Icon = pygame.image.load('resources/images/Ace-of-Clubs-icon.png')
        pygame.display.set_icon(Icon)
        self.clock = pygame.time.Clock()

        self.font_name = pygame.font.get_default_font()
        self.game = None

        self.timer = 0
        self.dt = 0

        self.run_object_dict = {self.RunObject.MAIN_MENU: MainMenu,
                                self.RunObject.GAME: Game,
                                self.RunObject.WIN_GAME: WinGame}

        self.run_object = self.RunObject.MAIN_MENU

    def _parse_args(self, args):
        lower_case_arg_list = list(map(str.lower, args))
        self.easy_game = 'easy' in lower_case_arg_list

    def _parse_jsonfile(self):
        with open('resources/solitaire.json') as f:
            data = json.load(f)
        self.version_major = data["VERSION_MAJOR"]
        self.version_minor = data["VERSION_MINOR"]
        self.version_build = data["VERSION_BUILD"]

    def run(self):

        run_object = self.run_object.run_class()(self)
        run_object.run()

    def check_events(self):
        self.event = None
        while self.event is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event = Events.QUIT
                    self.running = False
                    if not self.game is None:
                        self.game.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.event = Events.RETURN_KEY
                    if event.key == pygame.K_ESCAPE:
                        self.event = Events.ESCAPE_KEY
                    if event.key == pygame.K_DOWN:
                        self.event = Events.DOWN_KEY
                    if event.key == pygame.K_UP:
                        self.event = Events.UP_KEY
                    if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        self.event = Events.CTRL_Z_KEY
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:   #left mouse button click
                        position = pygame.mouse.get_pos()
                        self.click_location = Location(position[0],position[1])
                        if self.timer == 0:
                            # First mouse click. Start the timer
                            self.previous_click_location = self.click_location
                            self.timer = 0.001
                            self.event = Events.LEFT_MOUSE_CLICK
                        elif self.timer < 0.5:
                            # Clicked again before 0.5 seconds
                            if self.click_location.near(self.previous_click_location):
                                self.event = Events.DOUBLE_LEFT_MOUSE_CLICK
                            else:
                                self.event = Events.LEFT_MOUSE_CLICK
                                self.timer = 0
                        else:
                            self.event = Events.LEFT_MOUSE_CLICK
            # Increase timer after mouse was pressed the first time.
            if self.timer != 0:
                self.timer += self.dt
                if self.timer >= 0.5:
                    # Reset timer after 0.5 seconds.
                    self.timer = 0
            self.dt = self.clock.tick(30) / 1000

    def draw_text(self, text, font_name, font_size, location, color):
        font = pygame.font.SysFont(font_name, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (location.x, location.y)
        self.screen.blit(text_surface, text_rect)
