from .Base_Menu import BaseMenu
class GameMode(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":0})})
        self.buttons['continue'] = factory.create_TextButton({"font": self.interface.font1,"text": "→","position": (self.WIDTH-110,self.HEIGHT-100),"command1":lambda:self.type_game(False,True) if all(not mode for mode in self.interface.mode_game.values()) else None,"command2":lambda:(self.change_mains({"main":-1,"run":True,"command":None}),self.interface.sound_main.stop(),self.interface.sound_back_game.play(loops=-1)if self.interface.sound_type["value_game"] else None)})
        self.buttons['training_ai'] = factory.create_TextButton({"text": "Training AI","position": (50,self.HEIGHT/2-100),"command1":lambda:self.type_game(True),"command2":lambda:self.change_mains({"main":8})})
        self.buttons['player'] = factory.create_TextButton({"text": "Player","position": (50,self.HEIGHT/2-50),"command1":lambda:self.type_game(False,True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"Player":self.player_button,"Training AI":self.Training_AI_button,"AI":self.ai_button})})
    def _update_mode_buttons(self, selected_mode):
        mode_buttons = {"Training AI": self.buttons['training_ai'],"Player": self.buttons['player'],"AI": self.buttons['ai']}
        self.check_item(self.interface.mode_game,self.interface.SKYBLUE,self.interface.WHITE,"color",**mode_buttons)
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Mode Game", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons.values())