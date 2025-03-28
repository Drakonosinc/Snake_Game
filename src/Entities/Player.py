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
    def move(self):
        head_pos = (self.rect_head.x, self.rect_head.y)
        if self.direction == "UP": self.rect_head.y -= self.move_speed
        if self.direction == "DOWN": self.rect_head.y += self.move_speed
        if self.direction == "LEFT": self.rect_head.x -= self.move_speed
        if self.direction == "RIGHT": self.rect_head.x += self.move_speed
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y
        if len(self.body) > 0:
            self.body[0].x = head_pos[0]
            self.body[0].y = head_pos[1]
    def add_segment(self):
        if len(self.body) > 0:self.body.append(Rect(self.body[-1].x, self.body[-1].y, self.body[-1].width, self.body[-1].height))
        else:self.body.append(Rect(self.rect_head.x, self.rect_head.y, self.rect_head.width, self.rect_head.height))
    