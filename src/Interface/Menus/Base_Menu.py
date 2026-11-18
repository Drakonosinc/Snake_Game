import pygame
from pyforgeui import RetroBackdrop, RetroVisualFX


class BaseMenu:
    def __init__(self, interface=None):
        self.interface = interface
        if interface:
            self.screen = interface.screen
            self.WIDTH = interface.WIDTH
            self.HEIGHT = interface.HEIGHT
            self.config = interface.config
            if not hasattr(interface, "_retro_backdrop"):
                interface._retro_backdrop = RetroBackdrop(
                    self.WIDTH,
                    self.HEIGHT,
                    accent_color=(56, 189, 248),
                    secondary_color=(34, 197, 94),
                )

    def draw_retro_backdrop(self, show_grid: bool = True, show_particles: bool = True) -> None:
        if self.interface and hasattr(self.interface, "_retro_backdrop"):
            self.interface._retro_backdrop.draw_background(
                self.screen,
                show_grid=show_grid,
                show_particles=show_particles,
            )
        else:
            self.screen.fill((8, 12, 24))

    def draw_post_overlay(self) -> None:
        if self.interface and hasattr(self.interface, "_retro_backdrop"):
            self.interface._retro_backdrop.draw_post_overlay(self.screen)

    def draw_menu_title(
        self,
        font: pygame.font.Font,
        text: str,
        pos: tuple[int, int],
        main_color=(255, 199, 51),
        glow_color=(249, 115, 22),
    ) -> pygame.Rect:
        return RetroVisualFX.draw_neon_title(
            self.screen,
            font,
            text,
            pos,
            color=main_color,
            glow_color=glow_color,
            underline=True,
        )

    def draw_styled_label(
        self,
        font: pygame.font.Font,
        text: str,
        pos: tuple[int, int],
        color=(255, 255, 255),
        glow_color=(56, 189, 248),
        highlight_second_line: bool = False,
    ) -> None:
        surf, (px, py), _, _ = RetroVisualFX.render_text_styled(
            font,
            text,
            color=color,
            shadow=True,
            glow=True,
            glow_color=glow_color,
            glow_radius=3,
            highlight_second_line=highlight_second_line,
            second_line_color=(56, 189, 248),
        )
        self.screen.blit(surf, (int(pos[0]) - px, int(pos[1]) - py))

    def draw_hud_frame(
        self,
        rect: tuple[int, int, int, int] | pygame.Rect,
        accent_color=(56, 189, 248),
        bg_alpha: int = 155,
        corner_size: int = 12,
        header_line_y: int | None = None,
    ) -> None:
        RetroVisualFX.draw_hud_frame(
            self.screen,
            rect,
            accent_color=accent_color,
            bg_alpha=bg_alpha,
            corner_size=corner_size,
            header_line_y=header_line_y,
        )
    def filt(self,WIDTH,HEIGHT,number,color=(0,0,0),position=(0,0)):
        background=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        background.fill((*color, number))
        self.screen.blit(background,position)
    def check_item(self,dic,is_true,is_false,item,**kwargs):
        for key,button in kwargs.items():button.change_item({item:(is_true if dic[key] else is_false)})
    def execute_buttons(self,*args):
        for button in args:button.draw()
    def change_items(self,item,background,number):
        self.config.config_visuals[item]=((self.config.config_visuals[item] + number) % len(self.config.config_visuals[background]))
        self.interface.load_images()
    def on_off(self,dic=None,variable=""):
        if dic:dic[variable]=not dic[variable]
        else:setattr(self,variable,not getattr(self,variable))
    def increase_decrease_variable(self,dic=None,variable="",length=None,number=1,save=True):
        if dic!=None and length!=None:dic[variable]=max(1, dic[variable] + number)
        elif dic!=None:dic[variable]+=number
        else:setattr(self,variable,getattr(self,variable)+number)
        if save:self.config.save_config()
    def fade_transition(self,fade_in,color=(0,0,0),limit=255):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.fill(color)
        alpha=0 if not fade_in else 255
        while (not fade_in and alpha <= limit) or (fade_in and alpha >= limit):
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            self.interface.clock.tick(20)
            alpha += -15 if fade_in else 15
    def change_mains(self,config):
        if fade_in:=config.get("fade_in",True):self.fade_transition(False,config.get("color",(0,0,0)),config.get("limit",255))
        if fade_out:=config.get("fade_out",False):self.fade_transition(True,config.get("color2",(0,0,0)),0)
        target_main = config.get("main", None)
        if target_main == 4 and self.interface.main in (0, 3):
            self.interface.previous_menu = self.interface.main
        self.interface.main = target_main
        if config.get("command",None):config["command"]()
        if config.get("run",False):setattr(self.interface,"running",False),setattr(self.interface, "game_over", True)
        if config.get("recursive",False):self.change_mains({"main":self.interface.main,"fade_in":fade_in,"fade_out":fade_out})
    def type_game(self,mode_one=False,mode_two=False,mode_three=False):
        self.interface.mode_game["Training AI"]=mode_one
        self.interface.mode_game["Player"]=mode_two
        if mode_three:
            self.interface.load_AI()
        self.interface.mode_game["AI"] = bool(mode_three and self.interface.model_training is not None)
    def update_mode_buttons(self,buttons):
        mode_buttons = {"Training AI": buttons['training_ai'],"Player": buttons['player'],"AI": buttons['ai']}
        self.check_item(self.interface.mode_game,self.interface.SKYBLUE,self.interface.WHITE,"color",**mode_buttons)