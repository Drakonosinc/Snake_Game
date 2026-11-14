import random
import pygame
from pygame.locals import K_p, K_r, K_1
from pyforgefx import ParticleEmitter, ScreenShake, ShockwaveManager, StarfieldParallax
from Entities import *
from AI.AI_Controller import *
from Interface.Interface import *


class Snake_Game(interface):
    _DIRECTION_ANGLES = {"RIGHT": 0, "UP": 90, "LEFT": 180, "DOWN": 270}

    def __init__(self):
        super().__init__()
        self.models = None
        self.ai_handler = AIHandler(self)
        self.clock = pygame.time.Clock()
        self.FPS = 120
        self.time_delta = 1.0 / 120.0
        self.running = True
        self.game_over = False
        self.exit = False
        self.generation = 0
        self.reset_ai = 0
        self.previous_menu = 0
        self.starfield = StarfieldParallax(width=self.WIDTH, height=self.HEIGHT, num_stars=45)
        self.particles = ParticleEmitter()
        self.shockwaves = ShockwaveManager()
        self.screen_shake = ScreenShake()
        self.instances()
        self.draw_buttons()
        self.play_music()

    def instances(self):
        self.player = Player(100, 30, 25, 25, [[90, 30], [80, 30], [70, 30], [60, 30]])
        self.fruit = Apple(
            random.randrange(1, (self.WIDTH // 10)) * 10,
            random.randrange(1, (self.HEIGHT // 10)) * 10,
            20,
            20,
        )

    def handle_keys(self):
        for event in pygame.event.get():
            self.event_quit(event)
            if self.mode_game["Training AI"]:
                self.events(event)
            self.event_keydown(event)
            if self.main == 6:
                self.keys_menu.event_keys(event)
            self.scroll.events(event)
        self.pressed_keys = pygame.key.get_pressed()
        self.pressed_mouse = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    def event_quit(self, event):
        if event.type == pygame.QUIT:
            self.close_game()

    def close_game(self):
        self.sound_exit.play(loops=0)
        self.game_over, self.exit, self.running = True, True, False

    def event_keydown(self, event):
        if event.type == pygame.KEYDOWN:
            if self.main == 3 and event.key == K_p:
                self.main = -1
            elif self.main == -1 and event.key == K_p:
                self.main = 3
            if self.main == 1 and event.key == K_r:
                self.reset()
                self.change_mains({"main": -1})
            if self.mode_game["Training AI"] and event.key == K_1 and self.models is not None:
                save_model(self.models, None, self.model_path)
            if self.mode_game["Player"] and self.main == -1:
                if (
                    event.key in {self.config.config_keys["key_up"], self.config.config_keys["key_up2"]}
                    and self.player.direction != "DOWN"
                ):
                    self.player.direction = "UP"
                elif (
                    event.key in {self.config.config_keys["key_down"], self.config.config_keys["key_down2"]}
                    and self.player.direction != "UP"
                ):
                    self.player.direction = "DOWN"
                elif (
                    event.key in {self.config.config_keys["key_left"], self.config.config_keys["key_left2"]}
                    and self.player.direction != "RIGHT"
                ):
                    self.player.direction = "LEFT"
                elif (
                    event.key in {self.config.config_keys["key_right"], self.config.config_keys["key_right2"]}
                    and self.player.direction != "LEFT"
                ):
                    self.player.direction = "RIGHT"

    def events(self, event):
        if event.type == self.EVENT_RESET_AI and self.main == -1:
            if self.player.reward <= self.reset_ai:
                self.handle_collision(self.player, -20)
            else:
                self.reset_ai = self.player.reward

    def restart(self):
        if self.mode_game["Training AI"]:
            self.check_score()
            self.running = False
        if self.mode_game["Player"] or self.mode_game["AI"]:
            self.change_mains({"main": 1, "color": self.RED, "limit": 100, "command": self.reset})

    def reset(self, running=True):
        self.running = running
        self.check_score()
        self.player.reset()
        self.fruit.respawn_food(self.WIDTH, self.HEIGHT)
        self.particles.clear()
        self.shockwaves.clear()
        self.head_animator.play("idle", force_restart=True)
        self.reset_ai = 0
        pygame.time.set_timer(self.EVENT_RESET_AI, 0)
        pygame.time.set_timer(self.EVENT_RESET_AI, 60000)

    def type_mode(self):
        self.ai_handler.actions_AI(self.models if self.mode_game["Training AI"] else self.model_training)

    def draw(self):
        dt = max(1e-3, min(0.05, getattr(self, "time_delta", 1.0 / 120.0)))
        self.head_animator.update(dt)
        self.body_animator.update(dt)
        self.apple_animator.update(dt)
        self.particles.update(dt)
        self.shockwaves.update(dt)
        ox, oy = self.screen_shake.update(dt)

        self.screen.blit(self.background_img, (ox, oy))
        self.starfield.update_and_draw(self.screen, dt, drift_x=-0.4, drift_y=0.2)

        self.show_score()
        self.draw_generation()

        apple_frame = self.apple_animator.get_frame() or self.apple_img
        ax = self.fruit.rect.centerx - apple_frame.get_width() // 2 + ox
        ay = self.fruit.rect.centery - apple_frame.get_height() // 2 + oy
        self.screen.blit(apple_frame, (ax, ay))

        self.player.trail.draw(self.screen, offset=(ox, oy))

        body_frame = self.body_animator.get_frame() or self.body_snake
        for body in self.player.body:
            bx = body.centerx - body_frame.get_width() // 2 + ox
            by = body.centery - body_frame.get_height() // 2 + oy
            self.screen.blit(body_frame, (bx, by))

        head_frame = self.head_animator.get_frame() or self.head_snake
        angle = self._DIRECTION_ANGLES.get(self.player.direction, 0)
        if angle != 0:
            head_frame = pygame.transform.rotate(head_frame, angle)
        hx = self.player.rect_head.centerx - head_frame.get_width() // 2 + ox
        hy = self.player.rect_head.centery - head_frame.get_height() // 2 + oy
        self.screen.blit(head_frame, (hx, hy))

        self.particles.draw(self.screen, offset=(ox, oy))
        self.shockwaves.draw(self.screen, offset=(ox, oy))
        self.draw_interfaces()

    def collision(self):
        if self.player.check_collision(self.fruit):
            fx, fy = self.fruit.rect.centerx, self.fruit.rect.centery
            self.particles.emit_burst(
                x=fx,
                y=fy,
                count=18,
                color=(255, 80, 80),
                secondary_color=(255, 215, 70),
                speed_range=(45.0, 160.0),
                life_range=(0.2, 0.45),
                size_range=(2.0, 5.0),
            )
            self.shockwaves.spawn(fx, fy, max_radius=38.0, speed=180.0, color=(255, 200, 60), width=3)
            self.player.score += 1
            self.player.reward += 10
            self.sound_food.play(loops=0)
            self.fruit.respawn_food(self.WIDTH, self.HEIGHT)
            self.player.add_segment()

        if self.player.rect_head.x < -10:
            self.player.rect_head.x = self.WIDTH
        if self.player.rect_head.x > self.WIDTH:
            self.player.rect_head.x = -10
        if self.player.rect_head.y < 0:
            self.player.rect_head.y = self.HEIGHT
        if self.player.rect_head.y > self.HEIGHT:
            self.player.rect_head.y = 0

        for body in self.player.body:
            if self.player.collision_snake(self.player.rect_head, body):
                self.handle_collision(self.player, -10)
                break

    def handle_collision(self, player, reward=-25):
        hx, hy = player.rect_head.centerx, player.rect_head.centery
        self.head_animator.play("hit", force_restart=True)
        self.particles.emit_burst(
            x=hx,
            y=hy,
            count=24,
            color=(239, 68, 68),
            secondary_color=(250, 204, 21),
            speed_range=(60.0, 190.0),
            life_range=(0.22, 0.55),
            size_range=(2.5, 5.5),
        )
        self.shockwaves.spawn(hx, hy, max_radius=48.0, speed=200.0, color=(239, 68, 68), width=3)
        self.screen_shake.trigger(intensity=8.0, duration=0.25)
        self.sound_dead.play(loops=0)
        player.reward += reward
        player.active = False
        self.restart()

    def check_score(self):
        if self.player.score >= self.config.config_game["max_score"]:
            self.config.config_game["max_score"] = self.player.score

    def item_repeat_run(self):
        self.handle_keys()
        self.draw()
        self.time_delta = self.clock.tick(self.FPS) / 1000.0
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.item_repeat_run()

    def run_with_models(self):
        self.reset(True)
        self.player.reward = 0
        while self.running and not self.game_over:
            if self.main == -1:
                if self.mode_game["AI"] or self.mode_game["Training AI"]:
                    self.type_mode()
                self.player.move()
                self.collision()
            self.item_repeat_run()
        return self.player.reward
