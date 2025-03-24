from pygame import *
class Apple:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.reset_position = (x, y, width, height)
    def reset(self):
        self.rect = Rect(*self.reset_position)