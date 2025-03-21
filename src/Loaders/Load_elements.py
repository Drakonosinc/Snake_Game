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