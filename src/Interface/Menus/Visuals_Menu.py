from .Base_Menu import BaseMenu
class VisualsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.buttons['decrease_player_button'] = factory.create_TextButton({"font": self.interface.font3_5,"text": "<","position": (50,self.HEIGHT/2-100),"command1":lambda:self.change_items("value_snake_head","snake_head",-1)})
        self.buttons['increase_player_button'] = factory.create_TextButton({"font": self.interface.font3_5,"text": ">","position": (self.WIDTH/2-100,self.HEIGHT/2-100),"command1":lambda:self.change_items("value_snake_head","snake_head",1)})
        self.buttons['decrease_body_button'] = factory.create_TextButton({"font": self.interface.font3_5,"text": "<","position": (50,self.HEIGHT/2-50),"command1":lambda:self.change_items("value_snake_body","snake_body",-1)})
        self.buttons['increase_body_button'] = factory.create_TextButton({"font": self.interface.font3_5,"text": ">","position": (self.WIDTH/2-100,self.HEIGHT/2-50),"command1":lambda:self.change_items("value_snake_body","snake_body",1)})
        
        self.buttons['save_visual'] = factory.create_TextButton({"text": "Save config","position": (self.WIDTH/2,self.HEIGHT-85),"command1":self.config.save_config})
        self.buttons['default_visual'] = factory.create_TextButton({"text": "Default config","position": (self.WIDTH/2-40,self.HEIGHT-50),"command1":lambda:self.config.config(visuals=True),"command2":self.interface.load_images})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self._items_visuals()
        self.screen.blit(self.interface.font3.render("Visuals", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons.values())
    def _items_visuals(self):
        self.screen.blit(self.interface.head_snake,(120,self.HEIGHT/2-100))
        self.screen.blit(self.interface.body_snake,(120,self.HEIGHT/2-50))
        self.screen.blit(self.interface.apple_img,(120,self.HEIGHT/2))