import pygame
from pygame.locals import *
class ElementsFactory:
    def __init__(self,config:dict):
        self.screen=config["screen"]
        self.font=config.get("font",pygame.font.Font(None,25))
        self.color=config.get("color",(255,255,255))
        self.hover_color=config.get("hover_color",(255, 199, 51))
        self.color_back=config.get("color_back",(255,255,255))
        self.sound_hover=config.get("sound_hover",None)
        self.sound_touch=config.get("sound_touch",None)
    def create_TextButton(self,config:dict):
        return TextButton({"screen": self.screen,"font": self.font,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_PolygonButton(self,config:dict):
        return PolygonButton({"screen": self.screen,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_InputText(self,config:dict):
        return Input_text({"screen": self.screen,"font": self.font,"color": self.color,"color_back":self.color_back,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
class TextButton:
    def __init__(self,config:dict):
        self.screen = config["screen"]
        self.font = config.get("font", pygame.font.Font(None, 25))
        self.text = config["text"]
        self.color = config.get("color", (255, 255, 255))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.position = config["position"]
        self.commands = [config.get(f"command{i}") for i in range(1,4)]
        self.sound_hover = config.get("sound_hover")
        self.sound_touch = config.get("sound_touch")
        self.pressed = config.get("pressed",True)
        self.detect_mouse=config.get("detect_mouse",True)
        self.button_states=config.get("button_states",{"detect_hover":True,"presses_touch":True})
        self.rect = pygame.Rect(*self.position, *self.font.size(self.text))
        self.new_events(time=config.get("time",500))
    def new_events(self,time):
        self.EVENT_NEW = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENT_NEW,time)
    def reactivate_pressed(self,event):
        if event.type==self.EVENT_NEW:self.button_states["presses_touch"]=True
    def draw(self):
        self.screen.blit(self.font.render(self.text, True,self.color), self.position)
        if self.detect_mouse:self.mouse_collision(pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def mouse_collision(self,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.screen.blit(self.font.render(self.text,True,self.hover_color),self.position)
            if self.button_states["detect_hover"]:
                if self.sound_hover:self.sound_hover.play(loops=0)
                self.button_states["detect_hover"]=False
        else:self.button_states["detect_hover"]=True
    def pressed_button(self,pressed_mouse,mouse_pos):
        if pressed_mouse[0] and self.rect.collidepoint(mouse_pos) and self.button_states["presses_touch"]:
            if self.sound_touch:self.sound_touch.play(loops=0)
            self.button_states["presses_touch"]=False
            self.execute_commands()
        elif not pressed_mouse[0]:self.button_states["presses_touch"] = True
    def change_item(self,config:dict):
        self.color=config.get("color",self.color)
        self.text=config.get("text",self.text)
        self.detect_mouse=config.get("detect_mouse",self.detect_mouse)
        self.pressed=config.get("pressed",self.pressed)
    def execute_commands(self):
        for command in self.commands:
            if callable(command):command()
class PolygonButton:
    def __init__(self,config:dict):
        self.screen = config["screen"]
        self.position = config["position"]
        self.hover_position = config.get("hover_position",self.position)
        self.color = config.get("color", (255, 255, 255))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.commands = [config.get(f"command{i}") for i in range(1,4)]
        self.sound_hover = config.get("sound_hover")
        self.sound_touch = config.get("sound_touch")
        self.detect_mouse=config.get("detect_mouse",True)
        self.pressed = config.get("pressed",True)
        self.button_states=config.get("button_states",{"detect_hover":True,"presses_touch":True})
        self.rect = pygame.draw.polygon(self.screen, self.color, self.position).copy()
        self.new_events(time=config.get("time",500))
    def new_events(self,time):
        self.EVENT_NEW = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENT_NEW,time)
    def reactivate_pressed(self,event):
        if event.type==self.EVENT_NEW:self.button_states["presses_touch"]=True
    def draw(self):
        pygame.draw.polygon(self.screen, self.color, self.position)
        if self.detect_mouse:self.mouse_collision(pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def mouse_collision(self,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.polygon(self.screen, self.hover_color, self.hover_position)
            if self.button_states["detect_hover"]:
                if self.sound_hover:self.sound_hover.play(loops=0)
                self.button_states["detect_hover"]=False
        else:self.button_states["detect_hover"]=True
    def pressed_button(self,pressed_mouse,mouse_pos):
        if pressed_mouse[0] and self.rect.collidepoint(mouse_pos) and self.button_states["presses_touch"]:
            if self.sound_touch:self.sound_touch.play(loops=0)
            self.button_states["presses_touch"]=False
            self.execute_commands()
        elif not pressed_mouse[0]:self.button_states["presses_touch"] = True
    def change_item(self,config:dict):
        self.color=config.get("color",self.color)
        self.detect_mouse=config.get("detect_mouse",self.detect_mouse)
        self.pressed=config.get("pressed",self.pressed)
    def execute_commands(self):
        for command in self.commands:
            if callable(command):command()
class Input_text:
    def __init__(self,config:dict):
        self.screen=config["screen"]
        self.font = config.get("font", pygame.font.Font(None, 25))
        self.text = config.get("text","")
        self.color=config.get("color",(0,0,0))
        self.color_back=config.get("color_back",(255,255,255))
        self.hover_color=config.get("hover_color",(255, 199, 51))
        self.pressed_color=config.get("pressed_color",(135,206,235))
        self.border_color=config.get("border_color",(127,127,127))
        self.border=config.get("border",2)
        self.commands = [config.get(f"command{i}") for i in range(1,4)]
        self.position = config["position"]
        self.sound_hover = config.get("sound_hover")
        self.sound_touch = config.get("sound_touch")
        self.pressed = config.get("pressed",True)
        self.detect_mouse=config.get("detect_mouse",True)
        self.states=config.get("states",{"detect_hover":True,"presses_touch":True,"active":False})
        self.rect = pygame.Rect(*self.position)
        self.new_events(time=config.get("time",500))
    def new_events(self,time):
        self.EVENT_NEW = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENT_NEW,time)
    def reactivate_pressed(self,event):
        if event.type==self.EVENT_NEW:self.states["presses_touch"]=True
    def change_text(self,event):
        if self.states["active"] and event.type==KEYDOWN:
            if event.key == K_BACKSPACE:self.text=self.text[:-1]
            else:self.text+=event.unicode
    def draw(self):
        pygame.draw.rect(self.screen,self.color_back,self.rect)
        if self.detect_mouse:self.mouse_collision(pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
        input_player=pygame.draw.rect(self.screen,self.border_color,self.rect,self.border)
        self.screen.blit(self.font.render(self.text, True, self.color), (input_player.x+5, input_player.y-2))
    def mouse_collision(self,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen,self.hover_color,self.rect)
            if self.states["detect_hover"]:
                if self.sound_hover:self.sound_hover.play(loops=0)
                self.states["detect_hover"]=False
        else:self.states["detect_hover"]=True
    def pressed_button(self,pressed_mouse,mouse_pos):
        if pressed_mouse[0] and self.rect.collidepoint(mouse_pos) and self.states["presses_touch"]:
            self.states["active"]=True
            if self.sound_touch:self.sound_touch.play(loops=0)
            self.states["presses_touch"]=False
            self.execute_commands()
        if pressed_mouse[0] and not self.rect.collidepoint(mouse_pos):self.states["active"],self.states["presses_touch"]=False,True
        if self.states["active"]:pygame.draw.rect(self.screen,self.pressed_color,self.rect)
    def execute_commands(self):
        for command in self.commands:
            if callable(command):command()
    def show_player(self):return self.text