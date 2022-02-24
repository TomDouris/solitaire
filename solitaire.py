# solitaire.py

import sys

from GameController import GameController

game_controller = GameController(sys.argv[1:])

while game_controller.running:
	game_controller.run()