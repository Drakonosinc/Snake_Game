from .Base_Menu import BaseMenu
class MainMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['play'] = factory.create_TextButton({"text": "PLAY","position": (self.WIDTH/2-60, self.HEIGHT/2-100),"command1":lambda:self.change_mains({"main":2})})
        self.buttons['quit'] = factory.create_TextButton({"text": "QUIT","position": (self.WIDTH/2-60,self.HEIGHT/2-55),"sound_touch": self.interface.sound_exit,"command1": self.interface.close_game})
        self.buttons['options'] = factory.create_TextButton({"text": "OPTIONS","position": (self.WIDTH-180,self.HEIGHT-50),"command1":lambda:self.change_mains({"main":4})})
    def render(self):
        self.draw_retro_backdrop(show_grid=True, show_particles=True)
        self.draw_hud_frame(
            (int(self.WIDTH / 2 - 108), int(self.HEIGHT / 2 - 115), 216, 110),
            accent_color=(34, 197, 94),
            bg_alpha=150,
            corner_size=12,
        )
        self.draw_hud_frame(
            (self.WIDTH - 196, self.HEIGHT - 60, 184, 50),
            accent_color=(56, 189, 248),
            bg_alpha=150,
            corner_size=10,
        )
        self.draw_menu_title(
            self.interface.font3,
            "Snake Game",
            (int(self.WIDTH * (52 / 600)), int(self.HEIGHT * (20 / 400))),
        )
        self.execute_buttons(self.buttons['play'], self.buttons['quit'], self.buttons['options'])
        self.draw_post_overlay()