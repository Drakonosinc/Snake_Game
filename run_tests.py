import importlib
import os
import sys
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import pygame
from Game.Snake_Game import Snake_Game
from pyforgeai import build_model, wrap_model


class TestSnakeGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = Snake_Game()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.game.mode_game = {"Training AI": False, "Player": True, "AI": False}
        self.game.reset(True)
        self.game.main = -1

    def test_spritesheets_generated_on_disk(self):
        expected = [
            "head_snake_idle_strip8.png",
            "head_snake_boost_strip8.png",
            "head_snake_hit_strip6.png",
            "body_snake_idle_strip8.png",
            "apple_idle_strip8.png",
            "apple_spin_strip12.png",
        ]
        for fname in expected:
            full = os.path.join(self.game.spritesheet_dir, fname)
            self.assertTrue(os.path.exists(full), f"Missing spritesheet: {fname}")
            surf = pygame.image.load(full)
            self.assertGreater(surf.get_width(), surf.get_height())

    def test_player_move_reset_immutability_and_trail(self):
        p = self.game.player
        initial_body_coords = [(b.x, b.y) for b in p.body]
        for _ in range(5):
            p.move()
        self.assertGreater(len(p.trail.points), 0)
        p.add_segment()
        self.assertEqual(len(p.body), 5)

        p.reset()
        self.assertEqual(len(p.body), 4)
        self.assertEqual([(b.x, b.y) for b in p.body], initial_body_coords)

    def test_apple_pickup_and_death_fx(self):
        p = self.game.player
        self.game.fruit.rect.topleft = p.rect_head.topleft
        self.game.collision()
        self.assertEqual(p.score, 1)
        self.assertGreater(len(self.game.particles.particles), 0)
        self.assertGreater(len(self.game.shockwaves.rings), 0)

        # Trigger death FX
        self.game.mode_game = {"Training AI": True, "Player": False, "AI": False}
        self.game.handle_collision(p, -10)
        self.assertFalse(p.active)
        self.assertGreater(self.game.screen_shake.intensity, 0.0)

    def test_ai_state_and_pytorch_tensorflow_inference(self):
        state = self.game.ai_handler.get_state()
        self.assertEqual(state.shape, (13,))

        pt_model = wrap_model(build_model("Pytorch", 13, 4))
        tf_model = wrap_model(build_model("Tensorflow", 13, 4))

        self.game.ai_handler.actions_AI(pt_model)
        self.game.ai_handler.actions_AI(tf_model)

        # Verify AI cannot reverse 180 degrees from RIGHT to LEFT immediately
        self.game.player.direction = "RIGHT"
        self.game.ai_handler.AI_actions([0.0, 0.0, 10.0, 0.0])  # action 2 = LEFT
        self.assertEqual(self.game.player.direction, "RIGHT")

    def test_qlearning_env_and_draw(self):
        ql_mod = importlib.import_module("AI.Q-learning")
        env = ql_mod.SnakeEnv(game=self.game, render=False)
        state = env.reset()
        self.assertEqual(state.shape, (13,))
        next_state, reward, done = env.step(0)
        self.assertEqual(next_state.shape, (13,))
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)

        # Verify visual draw executes cleanly across all 4 directions
        for d in ("RIGHT", "UP", "LEFT", "DOWN"):
            self.game.player.direction = d
            self.game.draw()

    def test_menus_and_navigation(self):
        self.assertIn("decrease_food_button", self.game.visuals_menu.buttons)
        self.assertIn("increase_food_button", self.game.visuals_menu.buttons)

        btn_back = self.game.options_menu.buttons["back"]
        cb = btn_back.commands[0]

        self.game.main = 3
        self.game.change_mains({"main": 4, "fade_in": False})
        self.assertEqual(self.game.previous_menu, 3)
        cb()
        self.assertEqual(self.game.main, 3)

        # Render all 9 retro-modern menus
        for menu_id in range(9):
            self.game.main = menu_id
            self.game.draw_interfaces()

    def test_live_neural_network_training_background(self):
        self.game.mode_game = {"Training AI": True, "Player": False, "AI": False}
        self.game.main = -1
        model = build_model("Pytorch", 13, 4, hidden_sizes=[128, 64])
        self.game.models = model
        self.game.type_mode()
        self.assertIsNotNone(model.layer_activations)
        self.assertEqual([len(layer) for layer in model.layer_activations], [13, 128, 64, 4])
        self.game.draw()


if __name__ == "__main__":
    unittest.main(verbosity=2)
