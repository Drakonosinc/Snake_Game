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
        self.WIDTH,self.HEIGHT=600,400
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
    def load_images(self):
        self.image_path=os.path.join(self.config.base_dir, "images")
        self.apple_img=pygame.image.load(os.path.join(self.image_path,self.config.config_visuals["food"][self.config.config_visuals["value_foods"]]))
        self.apple_img=pygame.transform.scale(self.apple_img,(25,25))
        self.head_snake=pygame.image.load(os.path.join(self.image_path,self.config.config_visuals["snake_head"][self.config.config_visuals["value_snake_head"]]))
        self.head_snake=pygame.transform.scale(self.head_snake,(30,30))
        self.body_snake=pygame.image.load(os.path.join(self.image_path,self.config.config_visuals["snake_body"][self.config.config_visuals["value_snake_body"]]))
        self.body_snake=pygame.transform.scale(self.body_snake,(30,30))
        self.background_img=pygame.image.load(os.path.join(self.image_path,self.config.config_visuals["background"][self.config.config_visuals["value_background"]]))
        self.background_img=pygame.transform.scale(self.background_img,(600,400))
    def load_sounds(self):
        self.sound_path=os.path.join(self.config.base_dir, "sounds")
        self.sound_food=pygame.mixer.Sound(os.path.join(self.sound_path,"food.wav"))
        self.sound_game_over=pygame.mixer.Sound(os.path.join(self.sound_path,"game_over.flac"))
        self.sound_dead=pygame.mixer.Sound(os.path.join(self.sound_path,"dead.mp3"))
        self.sound_touchletters=pygame.mixer.Sound(os.path.join(self.sound_path,"touchletters.wav"))
        self.sound_buttonletters=pygame.mixer.Sound(os.path.join(self.sound_path,"buttonletters.mp3"))
        self.sound_exit=pygame.mixer.Sound(os.path.join(self.sound_path,"exitbutton.wav"))
        self.sound_main=pygame.mixer.Sound(os.path.join(self.sound_path,"main.wav"))
    def load_fonts(self):
        self.font_path = os.path.join(self.config.base_dir, "fonts")
        self.font=pygame.font.SysFont("times new roman",60)
        self.font_0=pygame.font.SysFont("times new roman",30)
        self.font_0_5=pygame.font.Font(None,25)
        self.font1=pygame.font.SysFont("times new roman", 80)
        self.font2=pygame.font.Font(None,35)
        self.font2_5=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),30)
        self.font3=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),60)
        self.font3_5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),30)
        self.font4=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),75)
        self.font5=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),20)
        self.font5_5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),20)
    def load_scores(self):
        self.scores_take=os.path.join(self.config.base_dir, "Config/score.txt")
    def save_scores(self,max_score):
        with open(self.scores_take, "w") as archive:archive.write(str(max_score) + "\n")