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
    def load_AI(self):
        self.model_path=os.path.join(self.config.base_dir, "AI/best_model.pth")