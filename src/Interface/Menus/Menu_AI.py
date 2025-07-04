from .Base_Menu import BaseMenu
class AIMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.execute_buttons(*self.buttons.values())