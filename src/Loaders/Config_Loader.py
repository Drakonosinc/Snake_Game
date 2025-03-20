import json,os
from pygame.locals import *
class Config():
    def __init__(self):self.base_dir = os.path.abspath(os.path.join(__file__, "../../.."))