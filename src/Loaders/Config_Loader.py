import json
import os
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d


class Config:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(__file__, "../../.."))
        self.config_path = os.path.join(self.base_dir, "Config")

    def _normalize_ai_config(self):
        if not isinstance(self.config_AI, dict):
            self.config(AI=True)
            return
        genetic_cfg = self.config_AI.get("genetic", {})
        self.config_AI.setdefault("generation_value", genetic_cfg.get("generation_value", 100))
        self.config_AI.setdefault("population_value", genetic_cfg.get("population_value", 20))
        self.config_AI.setdefault("try_for_ai", genetic_cfg.get("try_for_ai", 3))
        self.config_AI.setdefault("model_save", genetic_cfg.get("model_save", False))

        tt = self.config_AI.get("type_training", {"genetic": True, "q-learning": False})
        if isinstance(tt, dict):
            is_gen = bool(tt.get("genetic", tt.get("Genetic", True)))
            self.config_AI["type_training"] = {"genetic": is_gen, "q-learning": not is_gen}
        else:
            self.config_AI["type_training"] = {"genetic": True, "q-learning": False}

        tm = self.config_AI.get("type_model", {"Pytorch": True, "Tensorflow": False})
        if isinstance(tm, dict):
            is_pt = bool(tm.get("Pytorch", True))
            self.config_AI["type_model"] = {"Pytorch": is_pt, "Tensorflow": not is_pt}
        else:
            self.config_AI["type_model"] = {"Pytorch": True, "Tensorflow": False}

    def load_config(self):
        try:
            self.config_path = os.path.join(self.base_dir, "Config")
            with open(os.path.join(self.config_path, "config.json"), "r", encoding="utf-8") as file:
                config = json.load(file)
            self.config_visuals = config["config_visuals"]
            self.config_keys = config["config_keys"]
            self.config_sounds = config["config_sounds"]
            self.config_AI = config["config_AI"]
            self._normalize_ai_config()
            self.config_game = config["config_game"]
        except Exception:
            self.config(alls=True)
            self.save_config()

    def config(self, visuals=False, keys=False, sounds=False, AI=False, game=False, alls=False):
        if visuals or alls:
            self.config_visuals = {
                "background": ["bg.jpg"],
                "value_background": 0,
                "snake_head": ["head_snake.png"],
                "value_snake_head": 0,
                "snake_body": ["body_snake.png"],
                "value_snake_body": 0,
                "food": ["apple.png"],
                "value_foods": 0,
            }
        if keys or alls:
            self.config_keys = {
                "key_up": K_UP,
                "Name_key1": "UP",
                "key_up2": K_w,
                "Name_key2": "W",
                "key_down": K_DOWN,
                "Name_key3": "DOWN",
                "key_down2": K_s,
                "Name_key4": "S",
                "key_left": K_LEFT,
                "Name_key5": "LEFT",
                "key_left2": K_a,
                "Name_key6": "A",
                "key_right": K_RIGHT,
                "Name_key7": "RIGHT",
                "key_right2": K_d,
                "Name_key8": "D",
            }
        if sounds or alls:
            self.config_sounds = {"sound_menu": True, "sound_game": True}
        if AI or alls:
            self.config_AI = {
                "generation_value": 100,
                "population_value": 20,
                "try_for_ai": 3,
                "model_save": False,
                "type_training": {"genetic": True, "q-learning": False},
                "type_model": {"Pytorch": True, "Tensorflow": False},
            }
        if game or alls:
            self.config_game = {"max_score": 0}

    def save_config(self):
        self.config_path = os.path.join(self.base_dir, "Config")
        os.makedirs(self.config_path, exist_ok=True)
        config = {
            "config_visuals": self.config_visuals,
            "config_keys": self.config_keys,
            "config_sounds": self.config_sounds,
            "config_AI": self.config_AI,
            "config_game": self.config_game,
        }
        with open(os.path.join(self.config_path, "config.json"), "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)
