from .Base_Menu import BaseMenu
class KeysMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}