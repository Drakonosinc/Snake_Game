from Loaders.Load_elements import *
from .Elements_interface import *
class interface(load_elements):
    def __init__(self):
        super().__init__()
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys, 7=sound menu
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
    def draw_interfaces(self):
        self.main_menu()
        self.menu_options()
        self.mode_game_menu()
        self.game_over_menu()
        self.pausa_menu()
        self.sounds_menu()
        self.visuals_menu()
        self.keys_menu()
        self.draw_generation()
    def draw_buttons(self):
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
    def main_menu(self):pass
    def menu_options(self):pass
    def mode_game_menu(self):pass
    def game_over_menu(self):pass
    def pausa_menu(self):pass
    def sounds_menu(self):pass
    def visuals_menu(self):pass
    def keys_menu(self):pass
    def draw_generation(self):
        if self.main==-1 and self.mode_game["Training AI"]:self.screen.blit(self.font3_5.render(f"Generation: {int(self.generation)}", True, "orange"),(35,0))