from .Base_Menu import BaseMenu
class MainMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['play'] = factory.create_TextButton({"text": "PLAY","position": (self.WIDTH/2-60, self.HEIGHT/2-100),"command1":lambda:self.change_mains({"main":2})})
        self.buttons['quit'] = factory.create_TextButton({"text": "QUIT","position": (self.WIDTH/2-60,self.HEIGHT/2-55),"sound_touch": self.sound_exit,"command1": self.close_game})
        
    def render(self):pass