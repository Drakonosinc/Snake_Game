from pygame import *
class Apple:
    def __init__(self, x, y, width=20, height=20):
        self.rect = Rect(x, y, width, height)
        self.reset_position = (x, y, width, height)