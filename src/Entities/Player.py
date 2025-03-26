from pygame import *
class Player:
    def __init__(self, x, y, width=25, height=25):
        self.rect = Rect(x, y, width, height)
        self.reset_position = (x, y, width, height)
        self.move_speed = 3
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.reward = 0
        self.score = 0
        self.active = True
    def move(self, change):
        if change == "UP" and self.direction != "DOWN":self.direction = "UP"
        if change == "DOWN" and self.direction != "UP":self.direction = "DOWN"
        if change == "LEFT" and self.direction != "RIGHT":self.direction = "LEFT"
        if change == "RIGHT" and self.direction != "LEFT":self.direction = "RIGHT"
        # if self.direction == "UP":self.rect.y -= self.move_speed
        # if self.direction == "DOWN":self.rect.y += self.move_speed
        # if self.direction == "LEFT":self.rect.x -= self.move_speed
        # if self.direction == "RIGHT":self.rect.x += self.move_speed
    def reset(self):
        self.rect = Rect(*self.reset_position)
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.scores = 0
        self.active = True
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)