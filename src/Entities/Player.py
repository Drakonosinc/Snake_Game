from pygame import *
class Player:
    def __init__(self, x, y, width=25, height=25):
        self.rect = Rect(x, y, width, height)
        self.reset_position = (x, y, width, height)
        self.reward = 0
        self.score = 0