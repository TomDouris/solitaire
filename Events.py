# Events.py

from enum import Enum

class Events(Enum):
    RETURN_KEY = 1
    ESCAPE_KEY = 2
    LEFT_MOUSE_CLICK = 3
    DOUBLE_LEFT_MOUSE_CLICK = 4
    UP_KEY = 5
    DOWN_KEY = 6
    BACKSPACE_KEY = 7
    CTRL_Z_KEY = 8
    QUIT = 9
    LEFT_MOUSE_DOWN = 10
    LEFT_MOUSE_UP = 11
    LEFT_MOUSE_MOTION = 12