import pygame,random
from Entities import *
from Interface.Interface import *
class Snake_Game(interface):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.running=True
        self.game_over=False
        self.exit=False
        self.generation=0
        self.max_score=0
        self.instances()
        self.draw_buttons()
        self.play_music()
    def instances(self):
        self.snake_head=[100,30]
        self.snake_body=[[100,30],[90,30],[80,30],[70,30]]
        self.player = [Player(*i, 25, 25) for i in [[100,30],[90,30],[80,30],[70,30]]]
        self.fruit=Apple(random.randrange(1, (self.WIDTH//10)) * 10,random.randrange(1, (self.HEIGHT//10)) * 10,20,20)
    def draw(self):
            self.screen.blit(self.background_img,[0,0])
            self.screen.blit(self.font_0.render(f"Score: {self.player[0].score}",True,self.SKYBLUE),[0,0])
            self.screen.blit(self.apple_img,self.fruit)
            self.snake_body.insert(0,list(self.snake_head))
            for pos in self.snake_body:
                self.rect_s=pygame.Rect(self.snake_head[0], self.snake_head[1], 25, 25)
                self.screen.blit(self.body_snake,pos)
            self.screen.blit(self.head_snake,self.snake_head)
    def move_snake(self,change):
        if self.pause is False:
            if change == "UP" and self.player[0].direction != "DOWN":self.player[0].direction = "UP"
            if change == "DOWN" and self.player[0].direction != "UP":self.player[0].direction = "DOWN"
            if change == "LEFT" and self.player[0].direction != "RIGHT":self.player[0].direction = "LEFT"
            if change == "RIGHT" and self.player[0].direction != "LEFT":self.player[0].direction = "RIGHT"
            if self.player[0].direction == "UP":
                self.snake_head[1] -= self.player[0].move_speed
                self.body_snake[0][1] -= self.player[0].move_speed
            if self.vdirection == "DOWN":
                self.snake_head[1] += self.player[0].move_speed
                self.body_snake[0][1] += self.player[0].move_speed
            if self.player[0].direction == "LEFT":
                self.snake_head[0] -= self.player[0].move_speed
                self.body_snake[0][0] -= self.player[0].move_speed
            if self.player[0].direction == "RIGHT":
                self.snake_head[0] += self.player[0].move_speed
                self.body_snake[0][0] += self.player[0].move_speed
    def colision(self):
            if self.player[0].check_collision(self.apple):
                self.player[0].score += 1
                self.s_food.play(loops=0)
                self.fruit.respawn_food()
            else:self.body_snake.pop()
            if self.snake_head[0] < -10:self.snake_head[0]=self.WIDTH
            if self.snake_head[0] > self.WIDTH:self.snake_head[0]=-10
            if self.snake_head[1] < 0:self.snake_head[1]=self.HEIGHT
            if self.snake_head[1] > self.HEIGHT:self.snake_head[1]=0
            for body in self.body_snake[1:]:
                if self.snake_head[0] == body[0] and self.snake_head[1] == body[1]:
                    self.game_o=True
                    self.s_dead.play(loops=0)
    def reset(self):
        pass
    def check_score(self):
        if self.score>=self.max_score:self.max_score=self.score
    def run(self):
        while self.running and self.game_over is False:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:self.running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:self.running=False
                    if event.key == pygame.K_UP or event.key==pygame.K_w:self.change_to = "UP"
                    if event.key == pygame.K_DOWN or event.key==pygame.K_s:self.change_to = "DOWN"
                    if event.key == pygame.K_LEFT or event.key==pygame.K_a:self.change_to = "LEFT"
                    if event.key == pygame.K_RIGHT or event.key==pygame.K_d:self.change_to = "RIGHT"
            self.draw()
            self.move_snake(self.player[0].change_to)
            self.colision()
            self.clock.tick(self.FPS)
            pygame.display.flip()