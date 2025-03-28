from pygame import *
class Player:
    def __init__(self, x, y, width=25, height=25, body=[]):
        self.rect_head = Rect(x, y, width, height)
        self.body = [Rect(*i, width, height) for i in body]
        self.reset_head_position = (x, y, width, height)
        self.reset_body_position = [(*i, width, height) for i in body]
        self.move_speed = 3
        self.direction = "RIGHT"
        self.reward = 0
        self.score = 0
        self.active = True
    