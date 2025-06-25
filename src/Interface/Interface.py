from Loaders.Load_elements import *
from .Elements_interface import *
from .Menus import *
class interface(load_elements,BaseMenu):
    def __init__(self):
        load_elements.__init__(self)
        BaseMenu.__init__(self,self)
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys, 7=sound menu, 8=AI menu
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.sound_type={"sound_menu":f"Sound Menu {"ON" if (x:=self.config.config_sounds["sound_menu"]) else "OFF"}","color_menu":self.SKYBLUE if x else self.RED,"value_menu":x,
                        "sound_Game":f"Sound Game {"ON" if (j:=self.config.config_sounds["sound_game"]) else "OFF"}","color_game":self.SKYBLUE if j else self.RED,"value_game":j}
        self.utils_keys = {key: False for i, key in enumerate(self.config.config_keys.keys()) if i % 2 == 0}
        self.key=None
        self.initialize_menus()
    def initialize_menus(self):
        self.main_menu = MainMenu(self)
        self.game_over_menu = GameOver(self)
        self.game_mode_menu = GameMode(self)
    def play_music(self):
        self.check_sounds()
        self.sound_main.set_volume(0.5)
    def check_sounds(self):
        self.sound_back_game.stop()
        self.sound_main.play(loops=-1) if self.sound_type["value_menu"] else None
    def draw_interfaces(self):
        menu_routes = {
            0: self.main_menu.render,
            1: self.game_over_menu.render,
            2: self.game_mode_menu.render,}
        if self.main==3:self.pausa_menu()
        elif self.main==4:self.menu_options()
        elif self.main==5:self.visuals_menu()
        elif self.main==6:self.keys_menu()
        elif self.main==7:self.sounds_menu()
        elif self.main==8:self.menu_AI()
        if self.main in menu_routes:menu_routes[self.main]()
    def draw_buttons(self):
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.main_menu.setup_buttons()
        self.game_over_menu.setup_buttons()
        self.game_mode_menu.setup_buttons()
        self.buttons_config_AI()
        self.buttons_pausa()
        self.buttons_menu_options()
        self.buttons_visual()
        self.buttons_keys()
        self.buttons_sounds()
    def buttons_mode_game(self):
        self.Training_AI_button = self.button_factory_f2_5.create_TextButton({"text": "Training AI","position": (50,self.HEIGHT/2-100),"command1":lambda:self.type_game(True),"command2":lambda:self.change_mains({"main":8})})
        self.player_button = self.button_factory_f2_5.create_TextButton({"text": "Player","position": (50,self.HEIGHT/2-50),"command1":lambda:self.type_game(False,True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"Player":self.player_button,"Training AI":self.Training_AI_button,"AI":self.ai_button})})
        self.ai_button = self.button_factory_f2_5.create_TextButton({"text": "AI","position": (50,self.HEIGHT/2),"command1":lambda:self.type_game(False,False,True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"AI":self.ai_button,"Player":self.player_button,"Training AI":self.Training_AI_button})})
        
        
    def pausa_menu(self):
        self.filt(self.WIDTH,self.HEIGHT,150,self.GRAY)
        self.screen.blit(self.font3.render("Pause", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons_in_pausa)
    def buttons_pausa(self):
        self.reset_button = self.button_factory_f2_5.create_TextButton({"text": "Reset","position": (50,self.HEIGHT/2-100),"command1":self.reset,"command2":lambda:self.change_mains({"main":-1})})
        self.option_button = self.button_factory_f2_5.create_TextButton({"text": "Option","position": (50,self.HEIGHT/2-50),"command1":self.reset,"command2":lambda:self.change_mains({"main":4,"run":True}),"command3":self.check_sounds})
        self.menu_button = self.button_factory_f2_5.create_TextButton({"text": "Menu","position": (50,self.HEIGHT/2),"command1":self.reset,"command2":lambda:self.change_mains({"main":0,"run":True}),"command3":self.check_sounds})
        self.exit_button = self.button_factory_f2_5.create_TextButton({"text": "Exit","position": (50,self.HEIGHT/2+50),"sound_touch": self.sound_exit,"command1":self.close_game})
        self.buttons_in_pausa=[self.reset_button,self.option_button,self.menu_button,self.exit_button]
    def menu_options(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.font3.render("Options", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons_in_menu_options)
    def buttons_menu_options(self):
        self.visual_button = self.button_factory_f2_5.create_TextButton({"text": "Visuals","position": (50,self.HEIGHT/2-100),"command1":lambda:self.change_mains({"main":5})})
        self.sounds_button = self.button_factory_f2_5.create_TextButton({"text": "Sounds","position": (50,self.HEIGHT/2-50),"command1":lambda:self.change_mains({"main":7})})
        self.keys_button = self.button_factory_f2_5.create_TextButton({"text": "Keys","position": (50,self.HEIGHT/2),"command1":lambda:self.change_mains({"main":6})})
        self.back_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (50,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":0})})
        self.buttons_in_menu_options=[self.visual_button,self.sounds_button,self.keys_button,self.back_button]
    def visuals_menu(self):
        self.screen.fill(self.BLACK)
        self.items_visuals()
        self.screen.blit(self.font3.render("Visuals", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons_in_visuals)
    def items_visuals(self):
        self.screen.blit(self.head_snake,(120,self.HEIGHT/2-100))
        self.screen.blit(self.body_snake,(120,self.HEIGHT/2-50))
        self.screen.blit(self.apple_img,(120,self.HEIGHT/2))
    def buttons_visual(self):
        self.back_visual_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.decrease_player_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": "<","position": (50,self.HEIGHT/2-100),"command1":lambda:self.change_items("value_snake_head","snake_head",-1)})
        self.increase_player_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": ">","position": (self.WIDTH/2-100,self.HEIGHT/2-100),"command1":lambda:self.change_items("value_snake_head","snake_head",1)})
        self.decrease_body_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": "<","position": (50,self.HEIGHT/2-50),"command1":lambda:self.change_items("value_snake_body","snake_body",-1)})
        self.increase_body_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": ">","position": (self.WIDTH/2-100,self.HEIGHT/2-50),"command1":lambda:self.change_items("value_snake_body","snake_body",1)})
        self.decrease_food_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": "<","position": (50,self.HEIGHT/2),"command1":lambda:self.change_items("value_foods","food",-1)})
        self.increase_food_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": ">","position": (self.WIDTH/2-100,self.HEIGHT/2),"command1":lambda:self.change_items("value_foods","food",1)})
        self.save_visuals_button = self.button_factory_f2_5.create_TextButton({"text": "Save config","position": (self.WIDTH/2,self.HEIGHT-85),"command1":self.config.save_config})
        self.default_visuals_button = self.button_factory_f2_5.create_TextButton({"text": "Default config","position": (self.WIDTH/2-40,self.HEIGHT-50),"command1":lambda:self.config.config(visuals=True),"command2":self.load_images})
        self.buttons_in_visuals=[self.back_visual_button,self.decrease_player_button,self.increase_player_button,self.decrease_body_button,self.increase_body_button,self.decrease_food_button,self.increase_food_button,self.save_visuals_button,self.default_visuals_button]
    def keys_menu(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.font3.render("Keys", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons_in_keys)
    def buttons_keys(self):
        self.back_keys_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (50,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.up1_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key1"],"position": (125,self.HEIGHT/2-100),"command1":lambda:self.change_keys("key_up","Name_key1",self.up1_button)})
        self.down1_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key3"],"position": (100,self.HEIGHT/2),"command1":lambda:self.change_keys("key_down","Name_key3",self.down1_button)})
        self.left1_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key5"],"position": (25,self.HEIGHT/2-50),"command1":lambda:self.change_keys("key_left","Name_key5",self.left1_button)})
        self.right1_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key7"],"position": (175,self.HEIGHT/2-50),"command1":lambda:self.change_keys("key_right","Name_key7",self.right1_button)})
        self.up2_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key2"],"position": (self.WIDTH-125,self.HEIGHT/2-100),"command1":lambda:self.change_keys("key_up2","Name_key2",self.up2_button)})
        self.down2_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key4"],"position": (self.WIDTH-125,self.HEIGHT/2),"command1":lambda:self.change_keys("key_down2","Name_key4",self.down2_button)})
        self.left2_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key6"],"position": (self.WIDTH-50,self.HEIGHT/2-50),"command1":lambda:self.change_keys("key_left2","Name_key6",self.left2_button)})
        self.right2_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key8"],"position": (self.WIDTH-190,self.HEIGHT/2-50),"command1":lambda:self.change_keys("key_right2","Name_key8",self.right2_button)})
        self.save_keys_button = self.button_factory_f2_5.create_TextButton({"text": "Save config","position": (self.WIDTH/2,self.HEIGHT-85),"command1":self.config.save_config})
        self.default_keys_button = self.button_factory_f2_5.create_TextButton({"text": "Default config","position": (self.WIDTH/2-40,self.HEIGHT-50),"command1":lambda:(self.config.config(keys=True),self.change_mains({"main":6,"command":self.buttons_keys}))})
        self.keys_buttons={"key_up":self.up1_button,"key_up2":self.up2_button,"key_down":self.down1_button,"key_down2":self.down2_button,"key_left":self.left1_button,"key_left2":self.left2_button,"key_right":self.right1_button,"key_right2":self.right2_button}
        self.buttons_in_keys=[self.back_keys_button,self.save_keys_button,self.default_keys_button,*self.keys_buttons.values()]
    def change_keys(self,key,key_name,button=None):
        self.key=key
        self.key_name=key_name
        self.button_key=button
        for k in self.utils_keys.keys():self.utils_keys[k]=False if k!=self.key else not self.utils_keys[self.key]
        self.check_item(self.utils_keys,self.SKYBLUE,self.WHITE,"color",**self.keys_buttons)
    def event_keys(self,event):
        if self.key!=None and (self.utils_keys[self.key] and event.type==KEYDOWN):
            self.config.config_keys[self.key]=event.key
            self.config.config_keys[self.key_name]=event.unicode.upper()
            self.check_item(self.config.config_keys,self.config.config_keys[self.key_name],self.WHITE,"text",**{self.key:self.button_key})
            self.change_keys(self.key,self.key_name)
    def sounds_menu(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.font3.render("Sounds", True, "orange"),(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))))
        self.execute_buttons(*self.buttons_in_sounds)
        self.sound_menu_button.change_item({"color":self.sound_type["color_menu"],"text":self.sound_type["sound_menu"]})
        self.sound_game_button.change_item({"color":self.sound_type["color_game"],"text":self.sound_type["sound_Game"]})
    def buttons_sounds(self):
        self.back_sounds_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (50,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.sound_menu_button = self.button_factory_f2_5.create_TextButton({"text": self.sound_type["sound_menu"],"position": (50,self.HEIGHT/2-100),"command1":lambda:self.sound_on_off("sound_menu","color_menu","value_menu","Sound Menu",self.sound_main,True)})
        self.sound_game_button = self.button_factory_f2_5.create_TextButton({"text": self.sound_type["sound_Game"],"position": (50,self.HEIGHT/2-50),"command1":lambda:self.sound_on_off("sound_Game","color_game","value_game","Sound Game",self.sound_back_game)})
        self.buttons_in_sounds=[self.back_sounds_button,self.sound_menu_button,self.sound_game_button]
    def sound_on_off(self,sound:str,color,value=True,type_sound="",sound_back=None,play=False):
        self.sound_type[value]=not self.sound_type[value]
        self.sound_type[color]=self.SKYBLUE if self.sound_type[value] else self.RED
        self.sound_type[sound]=type_sound+" ON" if self.sound_type[value] else type_sound+" OFF"
        sound_back.play(loops=-1) if self.sound_type[value] and play else sound_back.stop()
        self.on_off(self.config.config_sounds,sound.lower())
        self.config.save_config()
    def menu_AI(self):
        self.screen.fill(self.BLACK)
        self.execute_buttons(*self.buttons_in_config_AI,self.scroll,*self.text_in_training_ai)
        self.save_model.change_item({"color":self.SKYBLUE if self.config.config_AI["model_save"] else self.RED,"text":"ON" if self.config.config_AI["model_save"] else "OFF"})
        self.scroll.update_elements([*self.buttons_in_config_AI[:-2],*self.text_in_training_ai])
    def text_training_ai(self):
        if not hasattr(self, "text_in_training_ai"):
            self.text_C=self.button_factory_f2_5.create_Text({"text":(f"Config Training AI"),"position":(int(self.WIDTH * (52 / 600)),int(self.HEIGHT * (20 / 400 ))),"detect_mouse":False})
            self.text_G=self.button_factory_f2_5.create_Text({"text":(f"Generation Size\n{self.config.config_AI['generation_value']:^36}"),"position":(50,self.HEIGHT/2-125),"detect_mouse":False})
            self.text_P=self.button_factory_f2_5.create_Text({"text":(f"Population Size\n{self.config.config_AI['population_value']:^36}"),"position":(50,self.HEIGHT/2-50),"detect_mouse":False})
            self.text_A=self.button_factory_f2_5.create_Text({"text":(f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{39 if self.config.config_AI['try_for_ai']<10 else 36}}"),"position":(50,self.HEIGHT/2+25),"detect_mouse":False})
            self.text_S=self.button_factory_f2_5.create_Text({"text":(f"Save model"),"position":(50,self.HEIGHT/2+100),"detect_mouse":False})
            self.text_in_training_ai=[self.text_C,self.text_G,self.text_P,self.text_A,self.text_S]
        else:
            self.text_G.change_item({"text": f"Generation Size\n{self.config.config_AI['generation_value']:^36}"})
            self.text_P.change_item({"text": f"Population Size\n{self.config.config_AI['population_value']:^36}"})
            self.text_A.change_item({"text": f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{39 if self.config.config_AI['try_for_ai']<10 else 36}}"})
    def buttons_config_AI(self):
        self.increase_generation = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (300,self.HEIGHT/2-95),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value'),"command2":self.text_training_ai})
        self.decrease_generation = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (120,self.HEIGHT/2-95),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value',True,-1),"command2":self.text_training_ai})
        self.increase_population = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (300,self.HEIGHT/2-20),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value'),"command2":self.text_training_ai})
        self.decrease_population = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (120,self.HEIGHT/2-20),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value',True,-1),"command2":self.text_training_ai})
        self.increase_try_for_ai = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (300,self.HEIGHT/2+55),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'try_for_ai'),"command2":self.text_training_ai})
        self.decrease_try_for_ai = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (120,self.HEIGHT/2+55),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'try_for_ai',True,-1),"command2":self.text_training_ai})
        self.save_model = self.button_factory_f2_5.create_TextButton({"text": "OFF","color": self.SKYBLUE,"position": (self.WIDTH/2+10,self.HEIGHT/2+100),"command1":lambda:self.on_off(self.config.config_AI,"model_save"),"command2":self.config.save_config})
        self.continue_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "→","position": (self.WIDTH-110,self.HEIGHT-100),"command1":lambda:self.type_game(True) if all(not mode for mode in self.mode_game.values()) else None,"command2":lambda:(self.change_mains({"main":-1,"run":True,"command":None}),self.sound_main.stop(),self.sound_back_game.play(loops=-1)if self.sound_type["value_game"] else None)})
        self.B_mode_game_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":2})})
        self.buttons_in_config_AI=[self.increase_generation,self.decrease_generation,self.increase_population,self.decrease_population,self.increase_try_for_ai,self.decrease_try_for_ai,self.save_model,self.continue_button,self.B_mode_game_button]
        self.scroll=self.button_factory_f2_5.create_ScrollBar({"position": (self.WIDTH-30, 50, 20, self.HEIGHT-100),"thumb_height": 20})
        self.text_training_ai()
    def draw_generation(self):
        if self.main==-1 and self.mode_game["Training AI"]:self.screen.blit(self.font5.render(f"Generation: {int(self.generation)}", True, "orange"),(0,25))
    def show_score(self):
        if self.main==-1 or self.main==1:self.screen.blit(self.font5.render(f"Score: {int(self.player.score)}", True, "orange"),(0,0))