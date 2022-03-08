#Location.py

import constants

class Location():

    #constructor
    def __init__(self, x, y):

        #check for valid parameters
        if (isinstance)(x, float):
            x = int(x)
        if not isinstance(x, int):
            raise TypeError(f"Argument x must be of type int, not {type(x)} x:{x}")
        if (isinstance)(y, float):
            y = int(y)
        if not isinstance(y, int):
            raise TypeError(f"Argument y must be of type int, not {type(y)} y:{y}")
        self.x = x
        self.y = y

    def __str__(self):
        return f'x:{self.x} y:{self.y}'

    # This method gets called when using == on the object
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def near(self, other, pixels=5):
        return abs(self.x - other.x) <= pixels and abs(self.y - other.y) <= pixels