# Instructions.py

import pygame

import constants
from Location import Location

class Instructions:

    def __init__(self, instructions):
    	self.instructions = instructions

    def draw(self, screen):
        font = pygame.font.SysFont(constants.FONT_ARIAL, int(round(constants.CELL_WIDTH*1/2)), False, False)
        for i, instruction in enumerate(self.instructions):
        	text = font.render(instruction, True, constants.BLACK)
        	screen.blit(text, [constants.FRAME_MAX_X/25, constants.FRAME_MAX_Y*20/25 + constants.FRAME_MAX_Y*1/25*i])
