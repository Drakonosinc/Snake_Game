from random import randint
from pygame import *
class Apple:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.reset_position = (x, y, width, height)
    def reset(self):
        self.rect = Rect(*self.reset_position)
    def respawn_food(self, width, height):
        self.rect.x = randint(1, (width-20)//10) * 10
        self.rect.y = randint(1, (height-20)//10) * 10