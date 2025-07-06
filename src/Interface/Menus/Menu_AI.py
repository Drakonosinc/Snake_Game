from .Base_Menu import BaseMenu
class AIMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.config_buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":2})})
        self.buttons['continue'] = factory.create_TextButton({"font": self.interface.font1,"text": "→","position": (self.WIDTH-110,self.HEIGHT-100),"command1":lambda:self.type_game(True) if all(not mode for mode in self.interface.mode_game.values()) else None,"command2":lambda:(self.change_mains({"main":-1,"run":True,"command":None}),self.interface.sound_main.stop(),self.interface.sound_back_game.play(loops=-1)if self.interface.sound_type["value_game"] else None)})
        self.buttons['scroll'] = factory.create_ScrollBar({"position": (self.WIDTH-30, 50, 20, self.HEIGHT-100),"thumb_height": 20})
        self._setup_training_ai_buttons()
        self._setup_training_ai_texts()
    def _setup_training_ai_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.config_buttons['increase_generation'] = factory.create_TextButton({"font":self.interface.font3_5,"text": ">","position": (300,self.HEIGHT/2-95),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value'),"command2":self._update_training_ai_texts})
        self.config_buttons['decrease_generation'] = factory.create_TextButton({"font":self.interface.font3_5,"text": "<","position": (120,self.HEIGHT/2-95),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value',True,-1),"command2":self._update_training_ai_texts})
        self.config_buttons['increase_population'] = factory.create_TextButton({"font":self.interface.font3_5,"text": ">","position": (300,self.HEIGHT/2-20),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value'),"command2":self._update_training_ai_texts})
        self.config_buttons['decrease_population'] = factory.create_TextButton({"font":self.interface.font3_5,"text": "<","position": (120,self.HEIGHT/2-20),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value',True,-1),"command2":self._update_training_ai_texts})
        self.config_buttons['increase_try_for_ai'] = factory.create_TextButton({"font":self.interface.font3_5,"text": ">","position": (300,self.HEIGHT/2+55),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'try_for_ai'),"command2":self._update_training_ai_texts})
        self.config_buttons['decrease_try_for_ai'] = factory.create_TextButton({"font":self.interface.font3_5,"text": "<","position": (120,self.HEIGHT/2+55),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'try_for_ai',True,-1),"command2":self._update_training_ai_texts})
        self.config_buttons['save_model'] = factory.create_TextButton({"text": "OFF","color": self.interface.SKYBLUE,"position": (self.WIDTH/2+10,self.HEIGHT/2+100),"command1":lambda:self.on_off(self.config.config_AI,"model_save"),"command2":self.config.save_config})
    def _setup_training_ai_texts(self):
        factory = self.interface.button_factory_f2_5
        self.config_buttons['text_C'] = factory.create_Text({"text":(f"Config Training AI"),"position":(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))),"detect_mouse":False})
        self.config_buttons['text_G'] = factory.create_Text({"text":(f"Generation Size\n{self.config.config_AI['generation_value']:^36}"),"position":(50,self.HEIGHT/2-125),"detect_mouse":False})
    def _update_training_ai_texts(self):pass
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.execute_buttons(*self.buttons.values(),*self.config_buttons.values())