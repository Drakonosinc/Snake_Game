import json,os
from pygame.locals import *
class Config():
    def __init__(self):self.base_dir = os.path.abspath(os.path.join(__file__, "../../.."))
    def load_config(self):
        try:
            config_path = os.path.join(self.base_dir, "Config")
        except:self.config(alls=True),self.save_config()
    def config(self,visuals=False,keys=False,sounds=False,AI=False,game=False,alls=False):
        pass
    def save_config(self):
        config_path = os.path.join(self.base_dir, "Config")