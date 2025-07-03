from .Base_Menu import BaseMenu
class SoundsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (50,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.buttons['sound_menu_button'] = factory.create_TextButton({"text": self.interface.sound_type["sound_menu"],"position": (50,self.HEIGHT/2-100),"command1":lambda:self.sound_on_off("sound_menu","color_menu","value_menu","Sound Menu",self.interface.sound_main,True)})
        self.buttons['sound_game_button'] = factory.create_TextButton({"text": self.interface.sound_type["sound_Game"],"position": (50,self.HEIGHT/2-50),"command1":lambda:self.sound_on_off("sound_Game","color_game","value_game","Sound Game",self.interface.sound_back_game)})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Sounds", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.buttons['sound_menu_button'].change_item({"color":self.interface.sound_type["color_menu"],"text":self.interface.sound_type["sound_menu"]})
        self.buttons['sound_game_button'].change_item({"color":self.interface.sound_type["color_game"],"text":self.interface.sound_type["sound_Game"]})
        self.execute_buttons(*self.buttons.values())