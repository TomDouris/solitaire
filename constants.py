# constants.py

FRAME_SIDE_MAX_PIXELS = 800

FRAME_MAX_X = 800
FRAME_MAX_Y = 800
CELL_WIDTH = 40

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_WHITE = (242, 242, 242)
LIGHT_BLUE = (204, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

CARD_VALUES =["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
CARD_SUITS = ["H","D","S","C"]

# card pile types
PILE_SINGLE_PILE = 1
PILE_OVERLAP_DOWN = 2
PILE_TYLED_DOWN = 3

KLONDIKE_INSTRUCTIONS = [
    'Drag cards with mouse to move',
    'Double click on card to move to Foundation Pile',
    'Press Ctrl-z to undo last move',
    'Press Esc to quit game and return to main menu'
]

MAIN_MENU_INSTRUCTIONS = [
    'Use Up and Down Arrows to navigate Menu Items',
    'Press Enter to select a Menu Item',
    'Press Esc quit Program'
]

DEFAULT_INSTRUCTIONS = [
    'Press Esc to return to Main Menu'
]

FONT_ARIAL = "Arial"
FONT_COMIC = "Comic Sans MS"