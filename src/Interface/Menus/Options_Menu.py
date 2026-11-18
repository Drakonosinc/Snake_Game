from .Base_Menu import BaseMenu
class OptionsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (50,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":getattr(self.interface, "previous_menu", 0)})})
        self.buttons['visual'] = factory.create_TextButton({"text": "Visuals","position": (50,self.HEIGHT/2-100),"command1":lambda:self.change_mains({"main":5})})
        self.buttons['sound'] = factory.create_TextButton({"text": "Sounds","position": (50,self.HEIGHT/2-50),"command1":lambda:self.change_mains({"main":7})})
        self.buttons['keys'] = factory.create_TextButton({"text": "Keys","position": (50,self.HEIGHT/2),"command1":lambda:self.change_mains({"main":6})})
    def render(self):
        self.draw_retro_backdrop(show_grid=True, show_particles=True)
        self.draw_hud_frame(
            (34, int(self.HEIGHT / 2 - 114), 235, 158),
            accent_color=(56, 189, 248),
            bg_alpha=150,
            corner_size=12,
        )
        self.draw_menu_title(
            self.interface.font3,
            "Options",
            (int(self.WIDTH * (52 / 600)), int(self.HEIGHT * (20 / 400))),
        )
        self.execute_buttons(*self.buttons.values())
        self.draw_post_overlay()