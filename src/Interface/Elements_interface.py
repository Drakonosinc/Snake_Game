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
    def create_Text(self,config:dict):
        return Text({"screen": self.screen,"font": self.font,"color": self.color,"hover_color": self.hover_color,**config})
    def create_TextButton(self,config:dict):
        return TextButton({"screen": self.screen,"font": self.font,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_PolygonButton(self,config:dict):
        return PolygonButton({"screen": self.screen,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_InputText(self,config:dict):
        return Input_text({"screen": self.screen,"font": self.font,"color": self.color,"color_back":self.color_back,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_ScrollBar(self,config:dict):
        return ScrollBar({"screen": self.screen,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_ComboBox(self,config:dict):
        return ComboBox({"screen": self.screen,"font": self.font,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
class ElementBehavior:
    def __init__(self, config: dict):
        self.screen = config["screen"]
        self.position = config["position"]
        self.sound_hover = config.get("sound_hover")
        self.sound_touch = config.get("sound_touch")
        self.detect_mouse=config.get("detect_mouse",True)
        self.pressed = config.get("pressed",True)
        self.states=config.get("states",{"detect_hover":True,"presses_touch":True,"click_time": None,"active":False})
        self.commands = [config.get(f"command{i}") for i in range(1,4)]
        self.new_events(time=config.get("time",500))
    def events(self, event):pass
    def new_events(self,time):
        self.EVENT_NEW = pygame.USEREVENT + self.define_event()
        pygame.time.set_timer(self.EVENT_NEW,time)
    def define_event(self):return 1
    def reactivate_pressed(self,event):
        if event.type==self.EVENT_NEW:self.states["presses_touch"]=True
    def draw_hover_effect(self):raise NotImplementedError
    def mouse_collision(self,rect,mouse_pos,draw=None):
        if rect.collidepoint(mouse_pos):
            self.draw_hover_effect() if draw is None else draw()
            if self.states["detect_hover"]:
                if self.sound_hover:self.sound_hover.play(loops=0)
                self.states["detect_hover"]=False
        else:self.states["detect_hover"]=True
    def pressed_button(self,rect,pressed_mouse,mouse_pos,draw=None):
        current_time = pygame.time.get_ticks()
        if pressed_mouse[0] and rect.collidepoint(mouse_pos) and self.states["presses_touch"]:
            self.states["active"]=True
            self.states["presses_touch"]=False
            self.states["click_time"] = current_time
        if self.states["click_time"] is not None:
            if current_time - self.states["click_time"] >= 200:
                if self.sound_touch:self.sound_touch.play(loops=0)
                self.states["click_time"] = None
                self.states["presses_touch"] = True
                self.execute_commands()
        if pressed_mouse[0] and not rect.collidepoint(mouse_pos):self.states["active"],self.states["presses_touch"]=False,True
        if self.states["active"]:self.draw_pressed_effect() if draw is None else draw()
    def draw_pressed_effect(self):return NotImplementedError
    def filter_rects_collision(self,rects: dict, mouse_pos, draws: list, option: bool=False):
        for rect, draw in zip(rects, draws):
            if rects[rect].collidepoint(mouse_pos):
                if option is True: self.pressed_button(rects[rect], pygame.mouse.get_pressed(), mouse_pos, draw)
                else:self.mouse_collision(rects[rect], mouse_pos, draw)
            if all(not rects[rect].collidepoint(mouse_pos) for rect in rects):self.states["detect_hover"],self.states["presses_touch"] = True,True
    def execute_commands(self):
        try:
            for command in self.commands:
                if callable(command):command()
        except TypeError:return None
class Text:
    def __init__(self,config:dict):
        self.screen = config["screen"]
        self.font = config.get("font", pygame.font.Font(None, 25))
        self.Behavior = ElementBehavior(config)
        self.text = config.get("text","")
        self.color = config.get("color", (255, 255, 255))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.position = config["position"]
        self.rect = pygame.Rect(*self.position, *self.font.size(self.text))
    def draw(self):
        self.screen.blit(self.font.render(self.text, True,self.color), self.position)
        if self.Behavior.detect_mouse:self.Behavior.mouse_collision(self.rect,pygame.mouse.get_pos(),self.draw_hover_effect)
    def draw_hover_effect(self):return self.screen.blit(self.font.render(self.text,True,self.hover_color),self.position)
    def change_item(self,config:dict):
        self.position = config.get("position",self.position)
        self.color=config.get("color",self.color)
        self.text=config.get("text",self.text)
class TextButton(Text,ElementBehavior):
    def __init__(self,config:dict):
        Text.__init__(self, config)
        ElementBehavior.__init__(self, config)
    def draw(self):
        super().draw()
        if self.pressed:self.pressed_button(self.rect,pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def change_item(self,config:dict):
        super().change_item(config)
        self.detect_mouse=config.get("detect_mouse",self.detect_mouse)
        self.pressed=config.get("pressed",self.pressed)
class PolygonButton(ElementBehavior):
    def __init__(self,config:dict):
        super().__init__(config)
        self.hover_position = config.get("hover_position",self.position)
        self.color = config.get("color", (255, 255, 255))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.rect = pygame.draw.polygon(self.screen, self.color, self.position).copy()
    def draw(self):
        pygame.draw.polygon(self.screen, self.color, self.position)
        if self.detect_mouse:self.mouse_collision(self.rect,pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(self.rect,pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def draw_hover_effect(self):return pygame.draw.polygon(self.screen, self.hover_color, self.hover_position)
    def change_item(self,config:dict):
        self.color=config.get("color",self.color)
        self.detect_mouse=config.get("detect_mouse",self.detect_mouse)
        self.pressed=config.get("pressed",self.pressed)
class Input_text(ElementBehavior):
    def __init__(self,config:dict):
        super().__init__(config)
        self.font = config.get("font", pygame.font.Font(None, 25))
        self.text = config.get("text","")
        self.color=config.get("color",(0,0,0))
        self.color_back=config.get("color_back",(255,255,255))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.pressed_color=config.get("pressed_color",(135,206,235))
        self.border_color=config.get("border_color",(127,127,127))
        self.border=config.get("border",2)
        self.rect = pygame.Rect(*self.position)
    def change_text(self,event):
        if self.states["active"] and event.type==KEYDOWN:
            if event.key == K_BACKSPACE:self.text=self.text[:-1]
            else:self.text+=event.unicode
    def draw(self):
        pygame.draw.rect(self.screen,self.color_back,self.rect)
        if self.detect_mouse:self.mouse_collision(self.rect,pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(self.rect,pygame.mouse.get_pressed(),pygame.mouse.get_pos())
        input_player=pygame.draw.rect(self.screen,self.border_color,self.rect,self.border)
        self.screen.blit(self.font.render(self.text, True, self.color), (input_player.x+5, input_player.y-2))
    def draw_hover_effect(self):return pygame.draw.rect(self.screen,self.hover_color,self.rect)
    def draw_pressed_effect(self):return pygame.draw.rect(self.screen,self.pressed_color,self.rect)
    def show_player(self):return self.text
class ScrollBar(ElementBehavior):
    def __init__(self, config: dict):
        super().__init__(config)
        self.rect = pygame.Rect(*self.position)
        self.hover_color=config.get("hover_color",(255, 199, 51))
        self.thumb_height = config.get("thumb_height", max(20, int(self.position[3] * config.get("thumb_ratio", 0.2))))
        self.thumb_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.thumb_height)
        self.color = config.get("color", (200, 200, 200))
        self.color_thumb = config.get("color_bar", (135, 206, 235))
        self.commands = config.get("command1")
        self.elements = None
        self.dragging = False
        self.drag_offset = 0
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.thumb_rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_offset = event.pos[1] - self.thumb_rect.y
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_y = event.pos[1] - self.drag_offset
            new_y = max(self.rect.top, min(new_y, self.rect.bottom - self.thumb_height))
            self.thumb_rect.y = new_y
            self.scroll_elements()
    def scroll_elements(self):
        max_scroll = self.content_height
        if max_scroll == 0:proportion = 0.0
        else:proportion = (self.thumb_rect.y - self.rect.y) / (self.rect.height - self.thumb_height)
        offset = int(proportion * max_scroll)
        for el, (x0, y0) in zip(self.elements, self.initial_positions):
            new_y = y0 - offset
            el.position = (x0, new_y)
            if isinstance(el.rect, dict):
                for key in el.rect:
                    item = el.rect[key]
                    if hasattr(item, 'y'):item.y = new_y
                    elif hasattr(item, 'rect') and hasattr(item, 'position'):
                        item.rect.y = new_y
                        item.position = (item.position[0], new_y)
            else:el.rect.y = new_y
        if callable(self.commands):self.commands(proportion)
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, self.color_thumb, self.thumb_rect)
        if self.detect_mouse:self.mouse_collision(self.thumb_rect,pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(self.thumb_rect,pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def draw_hover_effect(self):return pygame.draw.rect(self.screen, self.hover_color, self.thumb_rect)
    def update_elements(self, elements: list):
        if self.elements is None:
            self.elements = elements
            self.initial_positions = [(el.position[0], el.position[1]) for el in self.elements]
            if self.elements:
                top = min(y for _, y in self.initial_positions)
                bottom = self.return_rect()
                self.content_height = bottom - top
            else:self.content_height = self.rect.height
    def return_rect(self):
        for el in self.elements:
            if isinstance(el.rect, dict):return max(el.rect.bottom for el in self.elements.values() if isinstance(el.rect, dict))
            else:return max(el.rect.bottom for el in self.elements if not isinstance(el.rect, dict))
class ComboBox(TextButton):
    def __init__(self, config: dict):
        super().__init__(config)
        self.type_dropdown = self.icon_dropdown(config.get("type_dropdown", "down"))
        self.dropdown = config.get("size", (self.font.size(self.text)[0]+self.font.size(self.type_dropdown)[0], 200))
        self.hover_dropdown=config.get("hover_dropdown",(135,206,235))
        self.is_dropdown_open = False
        self.selected_index = None
        self.options = []
        self.option_buttons = []
        self.button_dropdown = TextButton({
            "screen": self.screen,
            "font": self.font,
            "color": self.color,
            "hover_color": self.hover_dropdown,
            "position": (self.position[0]+self.font.size(self.text)[0], int(self.position[1])),
            "text": self.type_dropdown,
            "sound_hover": self.sound_hover,
            "sound_touch": self.sound_touch,
            "command1": lambda: setattr(self, 'is_dropdown_open', not self.is_dropdown_open)})
        self.rect = {"button": pygame.Rect(*self.position, *self.font.size(self.text)),
                    "dropdown": self.button_dropdown}
    def icon_dropdown(self,type_dropdown):
        match type_dropdown:
            case "down":return " V"
            case "up":return " Λ"
            case "right":return " >"
            case "left":return " <"
    def get_rect_dropdown(self):
        match self.type_dropdown:
            case " V":return pygame.Rect(self.position[0], self.position[1] + self.font.get_height(), *self.dropdown)
            case " Λ":return None
            case " >":return None
            case " <":return None
    def draw(self):
        self.screen.blit(self.font.render(self.text, True,self.color),(self.position))
        self.button_dropdown.draw()
        if self.is_dropdown_open:self.draw_rect_dropdown()
        else:self.button_dropdown.change_item({"color": self.color})
        if self.detect_mouse:self.mouse_collision(self.rect["button"],pygame.mouse.get_pos(),self.draw_hover_effect)
        if self.pressed:self.pressed_button(self.rect["button"],pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def draw_hover_effect(self):return self.screen.blit(self.font.render(f"{self.text}{self.type_dropdown}", True,self.hover_color), (self.position))
    def draw_rect_dropdown(self):
        self.button_dropdown.change_item({"color": self.hover_dropdown})
        self.dropdown_rect = self.get_rect_dropdown()
        pygame.draw.rect(self.screen, self.hover_dropdown, self.dropdown_rect)
        for button in self.option_buttons:button.draw()
    def charge_elements(self, options: list[str]):
        self.options = options
        for i, option in enumerate(options):
            x = self.position[0]
            y = self.position[1] + self.font.get_height() + i * (self.font.get_height() + 5)
            position = (x, y)
            button = TextButton({
                "screen": self.screen,
                "font": self.font,
                "color": self.color,
                "hover_color": self.hover_color,
                "position": position,
                "text": option,
                "command1": lambda idx=i: self.select_option(idx)})
            self.option_buttons.append(button)
        if options and not self.text:
            self.text = options[0]
            self.selected_index = 0
    def select_option(self, index):
        if 0 <= index < len(self.options):
            self.text = self.options[index]
            self.selected_index = index
            self.is_dropdown_open = False
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect["dropdown"].collidepoint(event.pos):self.is_dropdown_open = not self.is_dropdown_open
            elif self.is_dropdown_open and not self.dropdown_rect.collidepoint(event.pos):self.is_dropdown_open = False