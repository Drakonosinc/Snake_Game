from .Base_Menu import BaseMenu
class SoundsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}