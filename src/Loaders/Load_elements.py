import os
import pygame
from pygame.locals import *
from pyforgeai import load_model, save_model
from pyforgefx import Animator, SpriteFXGenerator, SpriteSheet
from .Config_Loader import *


class load_elements:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.config = Config()
        self.config.load_config()
        self.load_AI()
        self.define_colors()
        self.load_fonts()
        self.load_sounds()
        self.config_screen()
        self.new_events()

    def load_AI(self):
        use_tf = bool(self.config.config_AI.get("type_model", {}).get("Tensorflow", False))
        framework = "tensorflow" if use_tf else "pytorch"
        ext = ".npz" if use_tf else ".pth"
        ai_dir = os.path.join(self.config.base_dir, "AI")
        os.makedirs(ai_dir, exist_ok=True)
        self.model_path = os.path.join(ai_dir, f"best_model{ext}")
        fallback_pth = os.path.join(ai_dir, "best_model.pth")
        target = self.model_path if os.path.exists(self.model_path) else fallback_pth
        if os.path.exists(target):
            try:
                self.model_training = load_model(target, 13, 4, framework=framework)
            except Exception:
                self.model_training = None
        else:
            self.model_training = None

    def config_screen(self):
        self.WIDTH, self.HEIGHT = 600, 400
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.load_images()

    def define_colors(self):
        self.GRAY = (127, 127, 127)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.SKYBLUE = (135, 206, 235)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.GOLDEN = (255, 199, 51)
        self.background = self.GRAY

    def image_direct_path(self, image, value):
        return self.config.config_visuals[image][self.config.config_visuals[value]]

    def load_images(self):
        self.image_path = os.path.join(self.config.base_dir, "images")
        self.spritesheet_dir = os.path.join(self.image_path, "spritesheets")
        os.makedirs(self.spritesheet_dir, exist_ok=True)

        food_file = self.image_direct_path("food", "value_foods")
        apple_raw = pygame.image.load(os.path.join(self.image_path, food_file))
        if pygame.display.get_surface():
            apple_raw = apple_raw.convert_alpha()
        self.apple_img = pygame.transform.smoothscale(apple_raw, (25, 25))

        head_file = self.image_direct_path("snake_head", "value_snake_head")
        head_raw = pygame.image.load(os.path.join(self.image_path, head_file))
        if pygame.display.get_surface():
            head_raw = head_raw.convert_alpha()
        self.head_snake = pygame.transform.smoothscale(head_raw, (30, 30))

        body_file = self.image_direct_path("snake_body", "value_snake_body")
        body_raw = pygame.image.load(os.path.join(self.image_path, body_file))
        if pygame.display.get_surface():
            body_raw = body_raw.convert_alpha()
        self.body_snake = pygame.transform.smoothscale(body_raw, (30, 30))

        bg_file = self.image_direct_path("background", "value_background")
        bg_raw = pygame.image.load(os.path.join(self.image_path, bg_file))
        if pygame.display.get_surface():
            bg_raw = bg_raw.convert()
        self.background_img = pygame.transform.scale(bg_raw, (600, 400))

        # Generate / load multi-frame PNG spritesheets
        head_stem = os.path.splitext(os.path.basename(head_file))[0]
        head_idle_path = os.path.join(self.spritesheet_dir, f"{head_stem}_idle_strip8.png")
        head_boost_path = os.path.join(self.spritesheet_dir, f"{head_stem}_boost_strip8.png")
        head_hit_path = os.path.join(self.spritesheet_dir, f"{head_stem}_hit_strip6.png")

        if os.path.exists(head_idle_path) and os.path.exists(head_boost_path) and os.path.exists(head_hit_path):
            head_idle_sheet = SpriteSheet(head_idle_path)
            head_boost_sheet = SpriteSheet(head_boost_path)
            head_hit_sheet = SpriteSheet(head_hit_path)
        else:
            head_idle_sheet = SpriteFXGenerator.generate_bobbing_strip(
                self.head_snake, num_frames=8, amplitude_px=1, glow_color=(74, 222, 128)
            )
            head_boost_sheet = SpriteFXGenerator.generate_thruster_strip(
                self.head_snake,
                num_frames=8,
                flame_color_core=(220, 255, 220),
                flame_color_outer=(34, 197, 94),
                nozzle_side="bottom",
            )
            head_hit_sheet = SpriteFXGenerator.generate_shield_hit_strip(
                self.head_snake, num_frames=6, shield_color=(239, 68, 68)
            )
            head_idle_sheet.save(head_idle_path)
            head_boost_sheet.save(head_boost_path)
            head_hit_sheet.save(head_hit_path)

        self.head_animator = (
            Animator(default_state="idle")
            .add_clip("idle", head_idle_sheet.slice_strip(8), fps=12.0, loop=True)
            .add_clip("boost", head_boost_sheet.slice_strip(8), fps=16.0, loop=True)
            .add_clip("hit", head_hit_sheet.slice_strip(6), fps=18.0, loop=False)
        )

        body_stem = os.path.splitext(os.path.basename(body_file))[0]
        body_idle_path = os.path.join(self.spritesheet_dir, f"{body_stem}_idle_strip8.png")
        if os.path.exists(body_idle_path):
            body_sheet = SpriteSheet(body_idle_path)
        else:
            body_sheet = SpriteFXGenerator.generate_bobbing_strip(
                self.body_snake, num_frames=8, amplitude_px=1, glow_color=None
            )
            body_sheet.save(body_idle_path)
        self.body_animator = Animator(default_state="idle").add_clip(
            "idle", body_sheet.slice_strip(8), fps=10.0, loop=True
        )

        apple_stem = os.path.splitext(os.path.basename(food_file))[0]
        apple_idle_path = os.path.join(self.spritesheet_dir, f"{apple_stem}_idle_strip8.png")
        apple_spin_path = os.path.join(self.spritesheet_dir, f"{apple_stem}_spin_strip12.png")
        if os.path.exists(apple_idle_path) and os.path.exists(apple_spin_path):
            apple_idle_sheet = SpriteSheet(apple_idle_path)
            apple_spin_sheet = SpriteSheet(apple_spin_path)
        else:
            apple_idle_sheet = SpriteFXGenerator.generate_bobbing_strip(
                self.apple_img, num_frames=8, amplitude_px=2, glow_color=(255, 90, 90)
            )
            apple_spin_sheet = SpriteFXGenerator.generate_rotation_strip(
                self.apple_img, num_frames=12, aura_color=(255, 180, 60)
            )
            apple_idle_sheet.save(apple_idle_path)
            apple_spin_sheet.save(apple_spin_path)

        self.apple_animator = (
            Animator(default_state="idle")
            .add_clip("idle", apple_idle_sheet.slice_strip(8), fps=10.0, loop=True)
            .add_clip("spin", apple_spin_sheet.slice_strip(12), fps=14.0, loop=True)
        )

    def load_sounds(self):
        self.sound_path = os.path.join(self.config.base_dir, "sounds")
        self.sound_food = pygame.mixer.Sound(os.path.join(self.sound_path, "food.wav"))
        self.sound_game_over = pygame.mixer.Sound(os.path.join(self.sound_path, "game_over.flac"))
        self.sound_dead = pygame.mixer.Sound(os.path.join(self.sound_path, "dead.mp3"))
        self.sound_touchletters = pygame.mixer.Sound(os.path.join(self.sound_path, "touchletters.wav"))
        self.sound_buttonletters = pygame.mixer.Sound(os.path.join(self.sound_path, "buttonletters.mp3"))
        self.sound_exit = pygame.mixer.Sound(os.path.join(self.sound_path, "exitbutton.wav"))
        self.sound_main = pygame.mixer.Sound(os.path.join(self.sound_path, "main.wav"))
        self.sound_back_game = pygame.mixer.Sound(os.path.join(self.sound_path, "sound_back_game.wav"))

    def load_fonts(self):
        self.font_path = os.path.join(self.config.base_dir, "fonts")
        self.font = pygame.font.SysFont("times new roman", 60)
        self.font_0 = pygame.font.SysFont("times new roman", 30)
        self.font_0_5 = pygame.font.Font(None, 25)
        self.font1 = pygame.font.SysFont("times new roman", 80)
        self.font2 = pygame.font.Font(None, 35)
        self.font2_5 = pygame.font.Font(os.path.join(self.font_path, "ka1.ttf"), 30)
        self.font3 = pygame.font.Font(os.path.join(self.font_path, "ka1.ttf"), 60)
        self.font3_5 = pygame.font.Font(os.path.join(self.font_path, "8bitOperatorPlusSC-Bold.ttf"), 30)
        self.font4 = pygame.font.Font(os.path.join(self.font_path, "ka1.ttf"), 40)
        self.font5 = pygame.font.Font(os.path.join(self.font_path, "ka1.ttf"), 20)
        self.font5_5 = pygame.font.Font(os.path.join(self.font_path, "8bitOperatorPlusSC-Bold.ttf"), 20)

    def new_events(self):
        self.EVENT_RESET_AI = pygame.USEREVENT + 2
        pygame.time.set_timer(self.EVENT_RESET_AI, 90000)
