# Runnable.py

class Runnable:

    #constructor
    def __init__(self, controller):

        self.controller = controller

    def run(self):             # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")