import pygame,random,os
class Snake_Game():
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.white=(255,255,255)
        self.black=(0,0,0)
        self.gray=(128,128,128)
        self.green=(0,255,0)
        self.skyblue=(0,191,255)
        self.background = self.gray
        pygame.display.set_caption("Snake")
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.scores_take=os.path.join(os.path.dirname(__file__), "score.txt")
        self.image_path=os.path.join(os.path.dirname(__file__), "images")
        self.apple_img=pygame.image.load(os.path.join(self.image_path,"apple.png"))
        self.apple_img=pygame.transform.scale(self.apple_img,(25,25))
        self.head_snake=pygame.image.load(os.path.join(self.image_path,"head_snake.png"))
        self.head_snake=pygame.transform.scale(self.head_snake,(30,30))
        self.body_snake=pygame.image.load(os.path.join(self.image_path,"body_snake.png"))
        self.body_snake=pygame.transform.scale(self.body_snake,(30,30))
        self.background_img=pygame.image.load(os.path.join(self.image_path,"floor.jpg"))
        self.background_img=pygame.transform.scale(self.background_img,(600,400))
        self.sound_path=os.path.join(os.path.dirname(__file__), "sounds")
        self.s_food=pygame.mixer.Sound(os.path.join(self.sound_path,"food.wav"))
        self.s_game_over=pygame.mixer.Sound(os.path.join(self.sound_path,"game_over.flac"))
        self.s_dead=pygame.mixer.Sound(os.path.join(self.sound_path,"dead.mp3"))
        self.s_main=pygame.mixer.Sound(os.path.join(self.sound_path,"main.wav"))
        self.running=True
        self.s_speed=3
        self.score=0
        self.game_o=False
        self.reset=False
        self.pause=False
        self.v_pause=0
        self.inter=True
        self.max_score=0
        self.head_s=[100,30]
        self.body_s=[[100,30],[90,30],[80,30],[70,30]]
        self.direction="RIGHT"
        self.change_to=self.direction
        self.fruit_position=[random.randrange(1, (self.screen_width//10)) * 10,random.randrange(1, (self.screen_height//10)) * 10]
        self.fruit_spawn=True
        self.gane_o=False
        self.rect_s=pygame.Rect(0, 0, 25, 25)
        self.rect_f=pygame.Rect(0, 0, 20, 20)
        self.font=pygame.font.SysFont("times new roman",60)
        self.font_0=pygame.font.SysFont("times new roman",30)
        self.s_v=True
    def draw(self):
        if self.pause is False:
            self.screen.blit(self.background_img,[0,0])
            self.screen.blit(self.font_0.render(f"Score: {self.score}",True,self.skyblue),[0,0])
            self.rect_f=pygame.Rect(self.fruit_position[0],self.fruit_position[1], 20, 20)
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
    def game_over(self):
        if self.game_o and self.inter is False:
            self.screen.fill(self.background)
            self.screen.blit(self.font.render("Game Over",True,self.black),(self.screen_width/2-135,self.screen_height/2-170))
            self.screen.blit(self.font_0.render("To restart press R",True,self.black),(self.screen_width/2-100,self.screen_height/2-100))
            self.reset=True
            if self.s_v:
                self.s_game_over.play(loops=0)
                self.s_v=False
    def reset_game(self):
        if self.reset:
            self.fruit_position=[random.randrange(1, (self.screen_width//10)) * 10,random.randrange(1, (self.screen_height//10)) * 10]
            self.head_s=[100,30]
            self.body_s=[[100,30],[90,30],[80,30],[70,30]]
            self.direction="RIGHT"
            self.change_to=self.direction
            self.score=0
            self.s_v=True
            self.game_o=False
            self.inter=True
            self.pause=True
            self.reset=False
    def interface(self):
        if self.inter:
            self.s_main.play(loops=-1)
            self.screen.fill(self.black)
            self.pause=True
            x = self.screen_width / 2 - 65
            y = self.screen_height / 2 - 100
            self.rect_inter = pygame.Rect(x + 46, y , 50, 19)
            self.rect_inter1 = pygame.Rect(x + 46, y +35, 50, 19)
            self.screen.blit(self.font.render("Snake Game",True,self.white), (x-84, y-80))
            self.screen.blit(self.font_0.render("Play", True, self.green), (x+45, y-10))
            self.screen.blit(self.font_0.render("Exit", True, self.green), (x+45, y+25))
            self.screen.blit(self.font_0.render(f"Highest Score {self.max_score}", True, self.skyblue), (0, self.screen_height-40))
        else:self.s_main.stop()
    def pause_menu(self):
        if self.pause and self.inter is False and self.game_o is False:
            text_pause=self.font.render("Pause",True,self.black)
            self.screen.blit(text_pause,(self.screen_width/2-70,self.screen_height/2-150))
    def score_snake(self):
        if self.score>=self.max_score:
            self.max_score=self.score
    def save_scores(self):
        with open(self.scores_take, "w") as archive:
            archive.write(str(self.max_score) + "\n")
    def load_scores(self):
        with open(self.scores_take, "r") as archive:
            score = archive.readline()
            self.max_score = int(score)
    def run(self):
        self.load_scores()
        while self.running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:self.running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:self.running=False
                    if event.key == pygame.K_UP or event.key==pygame.K_w:self.change_to = "UP"
                    if event.key == pygame.K_DOWN or event.key==pygame.K_s:self.change_to = "DOWN"
                    if event.key == pygame.K_LEFT or event.key==pygame.K_a:self.change_to = "LEFT"
                    if event.key == pygame.K_RIGHT or event.key==pygame.K_d:self.change_to = "RIGHT"
                    if event.key == pygame.K_p:
                        self.pause=True
                        self.v_pause+=1
                        if self.v_pause%2==0:self.pause=False
                    if event.key == pygame.K_r:self.reset_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_inter.collidepoint(event.pos) and self.inter:
                        self.inter=False
                        self.pause=False
                    if self.rect_inter1.collidepoint(event.pos) and self.inter:self.running=False
            self.draw()
            self.move_snake(self.change_to)
            self.colision()
            self.score_snake()
            self.pause_menu()
            self.game_over()
            self.interface()
            self.save_scores()
            self.clock.tick(self.FPS)
            pygame.display.flip()
if __name__=="__main__":(game:=Snake_Game()).run()
pygame.quit()