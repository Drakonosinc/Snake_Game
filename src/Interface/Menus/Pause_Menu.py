from .Base_Menu import BaseMenu
class Pause(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}