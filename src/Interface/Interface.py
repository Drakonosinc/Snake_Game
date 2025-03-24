from Loaders.Load_elements import *
from .Elements_interface import *
class interface(load_elements):
    def __init__(self):
        super().__init__()
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys, 7=sound menu
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.sound_type={"sound_menu":f"Sound Menu {"ON" if (x:=self.config.config_sounds["sound_menu"]) else "OFF"}","color_menu":self.SKYBLUE if x else self.RED,"value_menu":x}
    def draw_interfaces(self):
        if self.main==0:self.main_menu()
        if self.main==1:self.game_over_menu()
        if self.main==2:self.mode_game_menu()
        if self.main==3:self.pausa_menu()
        if self.main==4:self.menu_options()
        if self.main==5:self.visuals_menu()
        if self.main==6:self.keys_menu()
        if self.main==7:self.sounds_menu()
        self.draw_generation()
    def draw_buttons(self):
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.buttons_main_menu()
        self.buttons_game_over()
        self.buttons_mode_game()
        self.buttons_pausa()
        self.buttons_menu_options()
        self.buttons_visual()
        self.buttons_keys()
        self.buttons_sounds()
    def filt(self,width,height,number,color=(0,0,0),position=(0,0)):
        background=pygame.Surface((width,height),pygame.SRCALPHA)
        background.fill((*color, number))
        self.screen.blit(background,position)
    def check_item(self,dic,is_true,is_false,item,**kwargs):
        for key,button in kwargs.items():setattr(button,item,(is_true if dic[key] else is_false))
    def execute_buttons(self,*args):
        for button in args:button.draw()
    def main_menu(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.font4.render("Snake Game", True, "orange"),(35,self.height/2-250))
    def buttons_main_menu(self):pass
    def game_over_menu(self):
        self.screen.fill(self.BLACK)
    def buttons_game_over(self):pass
    def mode_game_menu(self):
        self.screen.fill(self.BLACK)
    def buttons_mode_game(self):pass
    def pausa_menu(self):
        self.screen.fill(self.BLACK)
    def buttons_pausa(self):pass
    def menu_options(self):
        self.screen.fill(self.BLACK)
    def buttons_menu_options(self):pass
    def visuals_menu(self):
        self.screen.fill(self.BLACK)
    def buttons_visual(self):pass
    def keys_menu(self):
        self.screen.fill(self.BLACK)
    def buttons_keys(self):pass
    def sounds_menu(self):
        self.screen.fill(self.BLACK)
    def buttons_sounds(self):pass
    def draw_generation(self):
        if self.main==-1 and self.mode_game["Training AI"]:self.screen.blit(self.font3_5.render(f"Generation: {int(self.generation)}", True, "orange"),(35,0))
    def show_score(self,player):
        if self.main==-1 or self.main==1:self.screen.blit(self.font.render(f"Score: {int(player.score)}", True, "orange"),(35,self.height-50))
    def fade_transition(self,fade_in,color=(0,0,0),limit=255):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(color)
        alpha=0 if not fade_in else 255
        while (not fade_in and alpha <= limit) or (fade_in and alpha >= limit):
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            self.clock.tick(20)
            alpha += -15 if fade_in else 15
    def change_mains(self,config):
        if fade_in:=config.get("fade_in",True):self.fade_transition(False,config.get("color",(0,0,0)),config.get("limit",255))
        if fade_out:=config.get("fade_out",False):self.fade_transition(True,config.get("color2",(0,0,0)),0)
        self.main=config.get("main",None)
        if config.get("command",None):config["command"]()
        if config.get("run",False):setattr(self,"running",False),setattr(self, "game_over", True)
        if config.get("recursive",False):self.change_mains({"main":self.main,"fade_in":fade_in,"fade_out":fade_out})