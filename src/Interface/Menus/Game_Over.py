from .Base_Menu import BaseMenu
class GameOver(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['main'] = factory.create_TextButton({"text": "Exit The Menu","position": (50,self.HEIGHT/2-50),"command1":self.interface.reset,"command2":lambda:self.change_mains({"main":0,"run":True,"command":self.interface.check_sounds})})
    def render(self):
        self.filt(self.WIDTH,self.HEIGHT,150,self.interface.RED)
        self.screen.blit(self.interface.font3.render("Game Over", True, self.interface.BLACK),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons.values())