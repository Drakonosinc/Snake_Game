from .Base_Menu import BaseMenu
class VisualsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self._items_visuals()
        self.screen.blit(self.interface.font3.render("Visuals", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons.values())
    def _items_visuals(self):
        self.screen.blit(self.interface.head_snake,(120,self.HEIGHT/2-100))
        self.screen.blit(self.interface.body_snake,(120,self.HEIGHT/2-50))
        self.screen.blit(self.interface.apple_img,(120,self.HEIGHT/2))