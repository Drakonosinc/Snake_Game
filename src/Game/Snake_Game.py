import pygame,random
from Entities import *
from Interface import Interface
class Snake_Game(Interface):
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
        head=[100,30]
        body=[[100,30],[90,30],[80,30],[70,30]]
        self.snake = [Player((*i, 25, 25)) for i in [[100,30],[90,30],[80,30],[70,30]]]
        self.fruit_position=Apple(random.randrange(1, (self.WIDTH//10)) * 10,random.randrange(1, (self.HEIGHT//10)) * 10,20,20)
    def draw(self):
        if self.pause is False:
            self.screen.blit(self.background_img,[0,0])
            self.screen.blit(self.font_0.render(f"Score: {self.score}",True,self.skyblue),[0,0])
            self.screen.blit(self.apple_img,self.fruit_position)
            self.body_s.insert(0,list(self.head_s))
            for pos in self.body_s:
                self.rect_s=pygame.Rect(self.head_s[0], self.head_s[1], 25, 25)
                self.screen.blit(self.body_snake,pos)
            self.screen.blit(self.head_snake,self.head_s)
    def move_snake(self,change):
        if self.pause is False:
            if change == "UP" and self.direction != "DOWN":self.direction = "UP"
            if change == "DOWN" and self.direction != "UP":self.direction = "DOWN"
            if change == "LEFT" and self.direction != "RIGHT":self.direction = "LEFT"
            if change == "RIGHT" and self.direction != "LEFT":self.direction = "RIGHT"
            if self.direction == "UP":
                self.head_s[1] -= self.s_speed
                self.body_s[0][1] -= self.s_speed
            if self.direction == "DOWN":
                self.head_s[1] += self.s_speed
                self.body_s[0][1] += self.s_speed
            if self.direction == "LEFT":
                self.head_s[0] -= self.s_speed
                self.body_s[0][0] -= self.s_speed
            if self.direction == "RIGHT":
                self.head_s[0] += self.s_speed
                self.body_s[0][0] += self.s_speed
    def colision(self):
        if self.pause is False:
            if self.rect_s.colliderect(self.rect_f):
                self.score += 1
                self.s_food.play(loops=0)
                self.fruit_spawn = False
                if not self.fruit_spawn:
                    self.fruit_position = [random.randrange(1, (self.screen_width//10)) * 10,random.randrange(1, (self.screen_height//10)) * 10]
                    self.fruit_spawn = True
            else:self.body_s.pop()
            if self.head_s[0] < -10:self.head_s[0]=self.screen_width
            if self.head_s[0] > self.screen_width:self.head_s[0]=-10
            if self.head_s[1] < 0:self.head_s[1]=self.screen_height
            if self.head_s[1] > self.screen_height:self.head_s[1]=0
            for body in self.body_s[1:]:
                if self.head_s[0] == body[0] and self.head_s[1] == body[1]:
                    self.game_o=True
                    self.s_dead.play(loops=0)
    def reset(self):
        pass
    def pause_menu(self):
        if self.pause and self.inter is False and self.game_o is False:
            text_pause=self.font.render("Pause",True,self.black)
            self.screen.blit(text_pause,(self.screen_width/2-70,self.screen_height/2-150))
    def score_snake(self):
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
            self.move_snake(self.change_to)
            self.colision()
            self.score_snake()
            self.pause_menu()
            self.save_scores()
            self.clock.tick(self.FPS)
            pygame.display.flip()