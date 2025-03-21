import pygame,os
from pygame.locals import *
from AI.Genetic_Algorithm import *
from .Config_Loader import *
class load_elements():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.config=Config()
        self.config.load_config()
        self.define_colors()
        self.load_fonts()
        self.load_sounds()
        self.config_screen()
        self.load_scores()
    def load_AI(self):
        self.model_path=os.path.join(self.config.base_dir, "AI/best_model.pth")
    def config_screen(self):
        self.WIDTH=self.config.config_visuals["WIDTH"]
        self.HEIGHT=self.config.config_visuals["HEIGHT"]
        self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.load_images()
    def define_colors(self):
        self.GRAY=(127,127,127)
        self.WHITE=(255,255,255)
        self.BLACK=(0,0,0)
        self.GREEN=(0,255,0)
        self.BLUE=(0,0,255)
        self.SKYBLUE=(135,206,235)
        self.YELLOW=(255,255,0)
        self.RED=(255,0,0)
        self.GOLDEN=(255,199,51)
        self.background=self.GRAY
    def load_scores(self):
        self.scores_take=os.path.join(self.base_dir, "Config/score.txt")
    def load_images(self):
        self.image_path=os.path.join(self.base_dir, "images")
        self.apple_img=pygame.image.load(os.path.join(self.image_path,"apple.png"))
        self.apple_img=pygame.transform.scale(self.apple_img,(25,25))
        self.head_snake=pygame.image.load(os.path.join(self.image_path,"head_snake.png"))
        self.head_snake=pygame.transform.scale(self.head_snake,(30,30))
        self.body_snake=pygame.image.load(os.path.join(self.image_path,"body_snake.png"))
        self.body_snake=pygame.transform.scale(self.body_snake,(30,30))
        self.background_img=pygame.image.load(os.path.join(self.image_path,"floor.jpg"))
        self.background_img=pygame.transform.scale(self.background_img,(600,400))
    def load_sounds(self):
        self.sound_path=os.path.join(self.base_dir, "sounds")
        self.s_food=pygame.mixer.Sound(os.path.join(self.sound_path,"food.wav"))
        self.s_game_over=pygame.mixer.Sound(os.path.join(self.sound_path,"game_over.flac"))
        self.s_dead=pygame.mixer.Sound(os.path.join(self.sound_path,"dead.mp3"))
        self.s_main=pygame.mixer.Sound(os.path.join(self.sound_path,"main.wav"))