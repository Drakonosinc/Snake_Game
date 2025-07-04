from .Base_Menu import BaseMenu
class AIMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}