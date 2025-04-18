import json,os
from pygame.locals import *
class Config():
    def __init__(self):self.base_dir = os.path.abspath(os.path.join(__file__, "../../.."))
    def load_config(self):
        try:
            self.config_path = os.path.join(self.base_dir, "Config")
            with open(os.path.join(self.config_path,"config.json"), 'r') as file:config = json.load(file)
            self.config_visuals = config["config_visuals"]
            self.config_keys = config["config_keys"]
            self.config_sounds = config["config_sounds"]
            self.config_AI = config["config_AI"]
            self.config_game = config["config_game"]
        except:self.config(alls=True),self.save_config()
    def config(self,visuals=False,keys=False,sounds=False,AI=False,game=False,alls=False):
        if visuals or alls:self.config_visuals={"background":["bg.jpg"],"value_background":0,
                            "snake_head":["head_snake.png"],"value_snake_head":0,
                            "snake_body":["body_snake.png"],"value_snake_body":0,
                            "food":["apple.png"],"value_foods":0}
        if keys or alls:self.config_keys={"key_up":K_UP,"Name_key1":"UP","key_up2":K_w,"Name_key2":"W",
                                        "key_down":K_DOWN,"Name_key3":"DOWN","key_down2":K_s,"Name_key4":"S",
                                        "key_left":K_LEFT,"Name_key5":"LEFT","key_left2":K_a,"Name_key6":"A",
                                        "key_right":K_RIGHT,"Name_key7":"RIGHT","key_right2":K_d,"Name_key8":"D"}
        if sounds or alls:self.config_sounds={"sound_menu":True,"sound_game":True}
        if AI or alls:self.config_AI={"generation_value":100,"population_value":20,"try_for_ai":3,"model_save":False,"type_training":["genetic","q-learning"],"type_model":["DQN","CNN"]}
        if game or alls:self.config_game={"max_score":0}
    def save_config(self):
        self.config_path = os.path.join(self.base_dir, "Config")
        config = {"config_visuals": self.config_visuals,"config_keys": self.config_keys,"config_sounds":self.config_sounds,"config_AI":self.config_AI,"config_game": self.config_game}
        with open(os.path.join(self.config_path,"config.json"), 'w') as file:json.dump(config, file, indent=4)