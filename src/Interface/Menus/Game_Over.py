from .Base_Menu import BaseMenu
class GameOver(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['reset'] = factory.create_TextButton({"text": "Press R to Restart","position": (50,self.HEIGHT/2-100),"command1":self.interface.reset,"command2":lambda:self.change_mains({"main":-1})})
        self.buttons['main'] = factory.create_TextButton({"text": "Exit The Menu","position": (50,self.HEIGHT/2-50),"command1":self.interface.reset,"command2":lambda:self.change_mains({"main":0,"run":True,"command":self.interface.check_sounds})})
        self.buttons['quit'] = factory.create_TextButton({"text": "Exit The Game","position": (50,self.HEIGHT/2),"sound_touch": self.interface.sound_exit,"command1":self.interface.close_game})
    def render(self):
        self.filt(self.WIDTH, self.HEIGHT, 175, (28, 6, 14))
        self.draw_hud_frame(
            (34, int(self.HEIGHT / 2 - 114), 365, 160),
            accent_color=(239, 68, 68),
            bg_alpha=170,
            corner_size=12,
        )
        self.draw_menu_title(
            self.interface.font3,
            "Game Over",
            (int(self.WIDTH * (52 / 600)), int(self.HEIGHT * (20 / 400))),
            main_color=(255, 95, 95),
            glow_color=(239, 68, 68),
        )
        self.execute_buttons(*self.buttons.values())
        self.draw_post_overlay()