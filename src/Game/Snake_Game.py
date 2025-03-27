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
        self.player = Player(100,30, 25, 25,[[100,30],[90,30],[80,30],[70,30]]) 
        self.fruit=Apple(random.randrange(1, (self.WIDTH//10)) * 10,random.randrange(1, (self.HEIGHT//10)) * 10,20,20)
    def handle_keys(self):
        for event in pygame.event.get():
            self.event_quit(event)
            self.events(event)
            self.event_keydown(event)
        self.pressed_keys=pygame.key.get_pressed()
        self.pressed_mouse=pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
    def event_quit(self,event):
        if event.type==pygame.QUIT:self.close_game()
    def close_game(self):
        self.sound_exit.play(loops=0)
        self.game_over,self.exit,self.running=True,True,False
    def event_keydown(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:self.running=False
            if (event.key == pygame.K_UP or event.key==pygame.K_w) and self.player[0].direction != "DOWN":self.player[0].direction = "UP"
            if (event.key == pygame.K_DOWN or event.key==pygame.K_s) and self.player[0].direction != "UP":self.player[0].direction = "DOWN"
            if (event.key == pygame.K_LEFT or event.key==pygame.K_a) and self.player[0].direction != "RIGHT":self.player[0].direction = "LEFT"
            if (event.key == pygame.K_RIGHT or event.key==pygame.K_d) and self.player[0].direction != "LEFT":self.player[0].direction = "RIGHT"
    def events(self,event):pass
        # if event.type == self.EVENT_BACKGROUND and self.main==-1:pass
    def restart(self):
        if all(not player.active for player in self.players) and self.mode_game["Training AI"]:self.reset(False,1)
        if self.mode_game["Player"] or self.mode_game["AI"]:self.change_mains({"main":1,"color":self.RED,"limit":100,"command":self.reset})
    def reset(self,running=True,type_reset=0):
        self.running=running
        self.instances()
        if type_reset==0:self.players[0].reset()
    def type_mode(self):
        self.ai_handler.actions_AI(self.models if self.mode_game["Training AI"] else self.model_training)
    def draw(self):
        self.screen.blit(self.background_img,[0,0])
        self.screen.blit(self.font_0.render(f"Score: {self.player.score}",True,self.SKYBLUE),[0,0])
        self.screen.blit(self.apple_img,self.fruit)
        for body in self.player.body:
            self.screen.blit(self.body_snake,body)
            self.move_snake(body)
        self.screen.blit(self.head_snake,self.player.rect_head)
    def move_snake(self,body):
        if self.player.direction == "UP":
            self.player.rect_head.y -= self.player.move_speed
            body.y -= self.player.move_speed
        if self.player.direction == "DOWN":
            self.player.rect_head.y += self.player.move_speed
            body.y += self.player.move_speed
        if self.player.direction == "LEFT":
            self.player.rect_head.x -= self.player.move_speed
            body.x -= self.player.move_speed
        if self.player.direction == "RIGHT":
            self.player.rect_head.x += self.player.move_speed
            body.x += self.player.move_speed
    def collision(self):
        if self.player.check_collision(self.fruit):
            self.player.score += 1
            self.sound_food.play(loops=0)
            self.fruit.respawn_food()
        else:self.player.body.pop()
        if self.player.rect_head.x < -10:self.player.rect_head.x=self.WIDTH
        if self.player.rect_head.x > self.WIDTH:self.player.rect_head.x=-10
        if self.player.rect_head.y < 0:self.player.rect_head.y=self.HEIGHT
        if self.player.rect_head.y > self.HEIGHT:self.player.rect_head.y=0
        for body in self.player.body[1:]:
            if self.player.rect_head.x == body.x and self.player.rect_head.y == body.y:self.sound_dead.play(loops=0)
    def check_score(self):
        if self.score>=self.max_score:self.max_score=self.score
    def run(self):
        while self.running and self.game_over is False:
            self.handle_keys()
            self.draw()
            self.collision()
            self.clock.tick(self.FPS)
            pygame.display.flip()