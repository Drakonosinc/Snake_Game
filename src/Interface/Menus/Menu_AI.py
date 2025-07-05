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
        self._setup_training_ai_buttons()
        self._setup_training_ai_texts()
    def _setup_training_ai_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.config_buttons['increase_generation'] = factory.create_TextButton({"font":self.interface.font3_5,"text": ">","position": (300,self.HEIGHT/2-95),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value'),"command2":self._update_training_ai_texts})
        self.config_buttons['decrease_generation'] = factory.create_TextButton({"font":self.interface.font3_5,"text": "<","position": (120,self.HEIGHT/2-95),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value',True,-1),"command2":self._update_training_ai_texts})
        self.config_buttons['increase_population'] = factory.create_TextButton({"font":self.interface.font3_5,"text": ">","position": (300,self.HEIGHT/2-20),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value'),"command2":self._update_training_ai_texts})
        self.config_buttons['decrease_population'] = factory.create_TextButton({"font":self.interface.font3_5,"text": "<","position": (120,self.HEIGHT/2-20),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value',True,-1),"command2":self._update_training_ai_texts})
    def _setup_training_ai_texts(self):
        factory = self.interface.button_factory_f2_5
    def _update_training_ai_texts(self):pass
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.execute_buttons(*self.buttons.values())