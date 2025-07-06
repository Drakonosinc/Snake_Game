from Loaders.Load_elements import *
from .Elements_interface import *
from .Menus import *
class interface(load_elements,BaseMenu):
    def __init__(self):
        load_elements.__init__(self)
        BaseMenu.__init__(self,self)
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys, 7=sound menu, 8=AI menu
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.sound_type={"sound_menu":f"Sound Menu {"ON" if (x:=self.config.config_sounds["sound_menu"]) else "OFF"}","color_menu":self.SKYBLUE if x else self.RED,"value_menu":x,
                        "sound_Game":f"Sound Game {"ON" if (j:=self.config.config_sounds["sound_game"]) else "OFF"}","color_game":self.SKYBLUE if j else self.RED,"value_game":j}
        self.initialize_menus()
    def initialize_menus(self):
        self.main_menu = MainMenu(self)
        self.game_over_menu = GameOver(self)
        self.game_mode_menu = GameMode(self)
        self.pause_menu = Pause(self)
        self.options_menu = OptionsMenu(self)
        self.visuals_menu = VisualsMenu(self)
        self.keys_menu = KeysMenu(self)
        self.sounds_menu = SoundsMenu(self)
        self.menu_AI = AIMenu(self)
    def play_music(self):
        self.check_sounds()
        self.sound_main.set_volume(0.5)
    def check_sounds(self):
        self.sound_back_game.stop()
        self.sound_main.play(loops=-1) if self.sound_type["value_menu"] else None
    def draw_interfaces(self):
        menu_routes = {
            0: self.main_menu.render,
            1: self.game_over_menu.render,
            2: self.game_mode_menu.render,
            3: self.pause_menu.render,
            4: self.options_menu.render,
            5: self.visuals_menu.render,
            6: self.keys_menu.render,
            7: self.sounds_menu.render,
            8: self.menu_AI.render}
        if self.main in menu_routes:menu_routes[self.main]()
    def draw_buttons(self):
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.main_menu.setup_buttons()
        self.game_over_menu.setup_buttons()
        self.game_mode_menu.setup_buttons()
        self.pause_menu.setup_buttons()
        self.options_menu.setup_buttons()
        self.visuals_menu.setup_buttons()
        self.keys_menu.setup_buttons()
        self.sounds_menu.setup_buttons()
        self.menu_AI.setup_buttons()
        self.buttons_config_AI()
    def menu_AI(self):
        self.save_model.change_item({"color":self.SKYBLUE if self.config.config_AI["model_save"] else self.RED,"text":"ON" if self.config.config_AI["model_save"] else "OFF"})
        self.scroll.update_elements([*self.buttons_in_config_AI[:-2],*self.text_in_training_ai])
    def text_training_ai(self):
        if not hasattr(self, "text_in_training_ai"):
            
            
            
            
            
            self.text_in_training_ai=[self.text_C,self.text_G,self.text_P,self.text_A,self.text_S]
        else:
            self.text_G.change_item({"text": f"Generation Size\n{self.config.config_AI['generation_value']:^36}"})
            self.text_P.change_item({"text": f"Population Size\n{self.config.config_AI['population_value']:^36}"})
            self.text_A.change_item({"text": f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{39 if self.config.config_AI['try_for_ai']<10 else 36}}"})
    def draw_generation(self):
        if self.main==-1 and self.mode_game["Training AI"]:self.screen.blit(self.font5.render(f"Generation: {int(self.generation)}", True, "orange"),(0,25))
    def show_score(self):
        if self.main==-1 or self.main==1:self.screen.blit(self.font5.render(f"Score: {int(self.player.score)}", True, "orange"),(0,0))