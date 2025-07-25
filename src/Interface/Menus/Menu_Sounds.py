from .Base_Menu import BaseMenu
class SoundsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (50,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.buttons['sound_menu_button'] = factory.create_TextButton({"text": self.interface.sound_type["sound_menu"],"position": (50,self.HEIGHT/2-100),"command1":lambda:self._sound_on_off("sound_menu","color_menu","value_menu","Sound Menu",self.interface.sound_main,True)})
        self.buttons['sound_game_button'] = factory.create_TextButton({"text": self.interface.sound_type["sound_Game"],"position": (50,self.HEIGHT/2-50),"command1":lambda:self._sound_on_off("sound_Game","color_game","value_game","Sound Game",self.interface.sound_back_game)})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Sounds", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.buttons['sound_menu_button'].change_item({"color":self.interface.sound_type["color_menu"],"text":self.interface.sound_type["sound_menu"]})
        self.buttons['sound_game_button'].change_item({"color":self.interface.sound_type["color_game"],"text":self.interface.sound_type["sound_Game"]})
        self.execute_buttons(*self.buttons.values())
    def _sound_on_off(self,sound:str,color,value=True,type_sound="",sound_back=None,play=False):
        self.interface.sound_type[value]=not self.interface.sound_type[value]
        self.interface.sound_type[color]=self.interface.SKYBLUE if self.interface.sound_type[value] else self.interface.RED
        self.interface.sound_type[sound]=type_sound+" ON" if self.interface.sound_type[value] else type_sound+" OFF"
        sound_back.play(loops=-1) if self.interface.sound_type[value] and play else sound_back.stop()
        self.on_off(self.config.config_sounds,sound.lower())
        self.config.save_config()