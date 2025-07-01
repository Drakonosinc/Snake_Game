from .Base_Menu import BaseMenu
from pygame.locals import KEYDOWN
class KeysMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.utils_keys = {key: False for i, key in enumerate(self.config.config_keys.keys()) if i % 2 == 0}
        self.buttons = {}
        self.buttons_keys = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (50,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.buttons_keys['up1_button'] = factory.create_TextButton({"text": self.config.config_keys["Name_key1"],"position": (125,self.HEIGHT/2-100),"command1":lambda:self._change_keys("key_up","Name_key1",self.buttons_keys["up1_button"])})
        self.buttons_keys['down1_button'] = factory.create_TextButton({"text": self.config.config_keys["Name_key3"],"position": (100,self.HEIGHT/2),"command1":lambda:self._change_keys("key_down","Name_key3",self.buttons_keys["down1_button"])})
        self.buttons_keys['left1_button'] = factory.create_TextButton({"text": self.config.config_keys["Name_key5"],"position": (25,self.HEIGHT/2-50),"command1":lambda:self._change_keys("key_left","Name_key5",self.buttons_keys["left1_button"])})
        self.buttons_keys['right1_button'] = factory.self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key7"],"position": (175,self.HEIGHT/2-50),"command1":lambda:self._change_keys("key_right","Name_key7",self.buttons_keys["right1_button"])})
        self.buttons_keys['up2_button'] = factory.create_TextButton({"text": self.config.config_keys["Name_key2"],"position": (self.WIDTH-125,self.HEIGHT/2-100),"command1":lambda:self._change_keys("key_up2","Name_key2",self.buttons_keys["up2_button"])})
        self.buttons_keys['down2_button'] = factory.create_TextButton({"text": self.config.config_keys["Name_key4"],"position": (self.WIDTH-125,self.HEIGHT/2),"command1":lambda:self._change_keys("key_down2","Name_key4",self.buttons_keys["down2_button"])})
        self.buttons['save_visual'] = factory.create_TextButton({"text": "Save config","position": (self.WIDTH/2,self.HEIGHT-85),"command1":self.config.save_config})
        self.buttons['default_visual'] = factory.create_TextButton({"text": "Default config","position": (self.WIDTH/2-40,self.HEIGHT-50),"command1":lambda:(self.config.config(keys=True),self.change_mains({"main":6,"command":self.setup_buttons}))})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Keys", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons.values())
    def _change_keys(self,key,key_name,button=None):
        self.key=key
        self.key_name=key_name
        self.button_key=button
        for k in self.utils_keys.keys():self.utils_keys[k]=False if k!=self.key else not self.utils_keys[self.key]
        self.check_item(self.utils_keys,self.interface.SKYBLUE,self.interface.WHITE,"color",**self.keys_buttons)
    def event_keys(self,event):
        if self.key!=None and (self.utils_keys[self.key] and event.type==KEYDOWN):
            self.config.config_keys[self.key]=event.key
            self.config.config_keys[self.key_name]=event.unicode.upper()
            self.check_item(self.config.config_keys,self.config.config_keys[self.key_name],self.WHITE,"text",**{self.key:self.button_key})
            self.change_keys(self.key,self.key_name)