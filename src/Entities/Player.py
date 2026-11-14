from pygame import Rect
from pyforgefx import TrailRenderer


class Player:
    def __init__(self, x, y, width=25, height=25, body=None):
        if body is None:
            body = []
        self.rect_head = Rect(x, y, width, height)
        self.body = [Rect(i[0], i[1], width, height) for i in body]
        self.reset_head_position = (x, y, width, height)
        self.reset_body_position = [(i[0], i[1], width, height) for i in body]
        self.move_speed = 3
        self.direction = "RIGHT"
        self.reward = 0
        self.score = 0
        self.active = True
        self.trail = TrailRenderer(max_points=14, color=(74, 222, 128), tail_color=(16, 185, 129), start_radius=7.0)

    def move(self):
        head_pos = (self.rect_head.x, self.rect_head.y)
        if self.direction == "UP":
            self.rect_head.y -= self.move_speed
        elif self.direction == "DOWN":
            self.rect_head.y += self.move_speed
        elif self.direction == "LEFT":
            self.rect_head.x -= self.move_speed
        elif self.direction == "RIGHT":
            self.rect_head.x += self.move_speed

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        if len(self.body) > 0:
            self.body[0].x = head_pos[0]
            self.body[0].y = head_pos[1]

        tail_ref = self.body[-1] if self.body else self.rect_head
        self.trail.push(tail_ref.centerx, tail_ref.centery)

    def add_segment(self):
        ref = self.body[-1] if self.body else self.rect_head
        dx, dy = 0, 0
        if self.direction == "RIGHT":
            dx = -self.move_speed
        elif self.direction == "LEFT":
            dx = self.move_speed
        elif self.direction == "DOWN":
            dy = -self.move_speed
        elif self.direction == "UP":
            dy = self.move_speed
        self.body.append(Rect(ref.x + dx, ref.y + dy, ref.width, ref.height))

    def reset(self):
        self.rect_head = Rect(*self.reset_head_position)
        self.body = [Rect(*coords) for coords in self.reset_body_position]
        self.direction = "RIGHT"
        self.score = 0
        self.active = True
        self.trail.clear()

    def check_collision(self, other_rect):
        target = other_rect.rect if hasattr(other_rect, "rect") else other_rect
        return self.rect_head.colliderect(target)

    def collision_snake(self, rect, other_rect):
        return (
            rect.x == other_rect.x
            and rect.y == other_rect.y
            and rect.width == other_rect.width
            and rect.height == other_rect.height
        )
