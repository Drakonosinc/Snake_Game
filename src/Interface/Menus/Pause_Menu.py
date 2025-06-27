from .Base_Menu import BaseMenu
class Pause(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['reset'] = factory.create_TextButton({"text": "Reset","position": (50,self.HEIGHT/2-100),"command1":self.interface.reset,"command2":lambda:self.change_mains({"main":-1})})
        self.buttons['options'] = factory.create_TextButton({"text": "Option","position": (50,self.HEIGHT/2-50),"command1":self.interface.reset,"command2":lambda:self.change_mains({"main":4,"run":True}),"command3":self.interface.check_sounds})
        self.buttons['menu'] = factory.create_TextButton({"text": "Menu","position": (50,self.HEIGHT/2),"command1":self.interface.reset,"command2":lambda:self.change_mains({"main":0,"run":True}),"command3":self.interface.check_sounds})
        self.buttons['exit'] = factory.create_TextButton({"text": "Exit","position": (50,self.HEIGHT/2+50),"sound_touch": self.interface.sound_exit,"command1":self.interface.close_game})
    def render(self):
        self.filt(self.WIDTH,self.HEIGHT,150,self.interface.GRAY)
        self.screen.blit(self.interface.font3.render("Pause", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons.values())