from Loaders.Load_elements import *
from pyforgeui import *
from .Menus import *
class interface(load_elements,BaseMenu):
    def __init__(self):
        load_elements.__init__(self)
        BaseMenu.__init__(self,self)
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys, 7=sound menu, 8=AI menu
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.sound_type={"sound_menu":f"Sound Menu {"ON" if (x:=self.config.config_sounds["sound_menu"]) else "OFF"}","color_menu":self.SKYBLUE if x else self.RED,"value_menu":x,
                        "sound_Game":f"Sound Game {"ON" if (j:=self.config.config_sounds["sound_game"]) else "OFF"}","color_game":self.SKYBLUE if j else self.RED,"value_game":j}
        self.initialize_menus()
    def initialize_menus(self):
        self.main_menu = MainMenu(self)
        self.game_over_menu = GameOver(self)
        self.game_mode_menu = GameMode(self)
        self.pause_menu = Pause(self)
        self.options_menu = OptionsMenu(self)
        self.visuals_menu = VisualsMenu(self)
        self.keys_menu = KeysMenu(self)
        self.sounds_menu = SoundsMenu(self)
        self.menu_AI = AIMenu(self)
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
            2: self.game_mode_menu.render,
            3: self.pause_menu.render,
            4: self.options_menu.render,
            5: self.visuals_menu.render,
            6: self.keys_menu.render,
            7: self.sounds_menu.render,
            8: self.menu_AI.render}
        if self.main in menu_routes:menu_routes[self.main]()
    def draw_buttons(self):
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.main_menu.setup_buttons()
        self.game_over_menu.setup_buttons()
        self.game_mode_menu.setup_buttons()
        self.pause_menu.setup_buttons()
        self.options_menu.setup_buttons()
        self.visuals_menu.setup_buttons()
        self.keys_menu.setup_buttons()
        self.sounds_menu.setup_buttons()
        self.menu_AI.setup_buttons()
    def draw_live_network_background(self):
        if self.main != -1 or not (self.mode_game.get("Training AI") or self.mode_game.get("AI")):
            return
        raw_model = getattr(self, "models", None) if self.mode_game.get("Training AI") else getattr(self, "model_training", None)
        if raw_model is None:
            raw_model = getattr(self, "model_training", None)
        if raw_model is not None and hasattr(raw_model, "get_internal_model"):
            raw_model = raw_model.get_internal_model()

        layers_sizes = None
        if raw_model is not None:
            in_sz = getattr(raw_model, "input_size", None)
            hid_sz = getattr(raw_model, "hidden_sizes", None)
            out_sz = getattr(raw_model, "output_size", None)
            if in_sz is not None and hid_sz is not None and out_sz is not None:
                layers_sizes = [int(in_sz), *[int(h) for h in hid_sz], int(out_sz)]
            else:
                try:
                    from pyforgeai import infer_architecture
                    _, inf_in, inf_out, inf_hid = infer_architecture(raw_model)
                    layers_sizes = [int(inf_in), *[int(h) for h in inf_hid], int(inf_out)]
                except Exception:
                    layers_sizes = None
        if not layers_sizes:
            layers_sizes = [13, 128, 64, 4]

        layer_activations = getattr(raw_model, "layer_activations", None) if raw_model is not None else None
        net_rect = (62, 54, self.WIDTH - 124, self.HEIGHT - 88)
        RetroVisualFX.draw_live_neural_network(
            self.screen,
            net_rect,
            layers_sizes=layers_sizes,
            layer_activations=layer_activations,
            accent_color=(56, 189, 248),
            secondary_color=(34, 197, 94),
            pulse_color=(255, 199, 51),
            opacity=110,
            show_frame=True,
            max_visible_neurons=8,
        )

    def draw_generation(self):
        if self.main == -1 and self.mode_game["Training AI"]:
            is_ql = bool(self.config.config_AI.get("type_training", {}).get("q-learning", False))
            label = f"Episode: {int(self.generation)}" if is_ql else f"Generation: {int(self.generation)}"
            self.draw_styled_label(self.font5, label, (8, 30), color=self.GOLDEN, glow_color=(56, 189, 248))

    def show_score(self):
        if self.main == -1 or self.main == 1:
            self.draw_styled_label(self.font5, f"Score: {int(self.player.score)}", (8, 4), color=self.GOLDEN, glow_color=(34, 197, 94))