import pygame,random
from Entities import *
from AI.AI_Controller import *
from Interface.Interface import *
class Snake_Game(interface):
    def __init__(self):
        super().__init__()
        self.models=None
        self.ai_handler=AIHandler(self)
        self.clock=pygame.time.Clock()
        self.FPS=120
        self.running=True
        self.game_over=False
        self.exit=False
        self.generation=0
        self.reset_ai=0
        self.instances()
        self.draw_buttons()
        self.play_music()
    def instances(self):
        self.player = Player(100,30, 25, 25,[[90,30],[80,30],[70,30],[60,30]]) 
        self.fruit = Apple(random.randrange(1, (self.WIDTH//10)) * 10,random.randrange(1, (self.HEIGHT//10)) * 10,20,20)
    def handle_keys(self):
        for event in pygame.event.get():
            self.event_quit(event)
            if self.mode_game["Training AI"]:self.events(event)
            self.event_keydown(event)
            if self.main==6:self.keys_menu.event_keys(event)
            self.scroll.events(event)
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
            if self.main==3 and event.key==K_p:self.main=-1
            elif self.main==-1 and event.key==K_p:self.main=3
            if self.mode_game["Training AI"] and event.key==K_1:save_model(self.models, torch.optim.Adam(self.models.parameters(), lr=0.001),self.model_path)
            if self.mode_game["Player"] and self.main==-1:
                if (event.key in {self.config.config_keys["key_up"], self.config.config_keys["key_up2"]}) and self.player.direction != "DOWN":self.player.direction = "UP"
                if (event.key in {self.config.config_keys["key_down"], self.config.config_keys["key_down2"]}) and self.player.direction != "UP":self.player.direction = "DOWN"
                if (event.key in {self.config.config_keys["key_left"], self.config.config_keys["key_left2"]}) and self.player.direction != "RIGHT":self.player.direction = "LEFT"
                if (event.key in {self.config.config_keys["key_right"], self.config.config_keys["key_right2"]}) and self.player.direction != "LEFT":self.player.direction = "RIGHT"
    def events(self, event):
        if event.type == self.EVENT_RESET_AI and self.main == -1:
            if self.player.reward <= self.reset_ai:self.handle_collision(self.player, -20)
            else:self.reset_ai = self.player.reward
    def restart(self):
        if self.mode_game["Training AI"]:self.reset(False)
        if self.mode_game["Player"] or self.mode_game["AI"]:self.change_mains({"main":1,"color":self.RED,"limit":100,"command":self.reset})
    def reset(self,running=True):
        self.running=running
        self.check_score()
        self.player.reset()
        self.fruit.respawn_food(self.WIDTH,self.HEIGHT)
        self.reset_ai = 0
        pygame.time.set_timer(self.EVENT_RESET_AI, 0)
        pygame.time.set_timer(self.EVENT_RESET_AI, 60000)
    def type_mode(self):
        self.ai_handler.actions_AI(self.models if self.mode_game["Training AI"] else self.model_training)
    def draw(self):
        self.screen.blit(self.background_img,[0,0])
        self.show_score()
        self.draw_generation()
        self.screen.blit(self.apple_img,self.fruit)
        for body in self.player.body:self.screen.blit(self.body_snake,body)
        self.screen.blit(self.head_snake,self.player.rect_head)
        self.draw_interfaces()
    def collision(self):
        if self.player.check_collision(self.fruit):
            self.player.score += 1
            self.player.reward += 10
            self.sound_food.play(loops=0)
            self.fruit.respawn_food(self.WIDTH,self.HEIGHT)
            self.player.add_segment()
        if self.player.rect_head.x < -10:self.player.rect_head.x = self.WIDTH
        if self.player.rect_head.x > self.WIDTH:self.player.rect_head.x = -10
        if self.player.rect_head.y < 0:self.player.rect_head.y = self.HEIGHT
        if self.player.rect_head.y > self.HEIGHT:self.player.rect_head.y = 0
        for body in self.player.body:
            if self.player.collision_snake(self.player.rect_head,body):self.handle_collision(self.player, -10)
    def handle_collision(self, player, reward=-25):
        self.sound_dead.play(loops=0)
        player.reward += reward
        player.active = False
        self.restart()
    def check_score(self):
        if self.player.score>=self.config.config_game["max_score"]:self.config.config_game["max_score"]=self.player.score
    def item_repeat_run(self):
        self.handle_keys()
        self.draw()
        self.clock.tick(self.FPS)
        pygame.display.flip()
    def run(self):
        self.running=True
        while self.running:self.item_repeat_run()
    def run_with_models(self):
        self.running=True
        self.player.reward = 0
        while self.running and self.game_over==False:
            if self.main==-1:
                if self.mode_game["AI"] or self.mode_game["Training AI"]:self.type_mode()
                self.player.move()
                self.collision()
            self.item_repeat_run()
        return self.player.reward