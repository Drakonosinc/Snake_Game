import numpy as np
from Game.Snake_Game import Snake_Game
from AI.AI_Controller import AIHandler
from pyforgeai import IEnvironment, QLearningTrainer, save_model


class SnakeEnv(IEnvironment):
    """Gym-like IEnvironment wrapper for Snake_Game."""

    def __init__(self, game: Snake_Game | None = None, render: bool = False):
        self.game = game if game is not None else Snake_Game()
        self.handler = AIHandler(self.game)
        self.prev_reward = 0.0
        self.render_mode = render
        self._steps = 0

    @property
    def state_size(self) -> int:
        return 13

    @property
    def action_size(self) -> int:
        return 4

    @property
    def action_space(self) -> int:
        return 4

    def reset(self) -> np.ndarray:
        self.game.reset(True)
        self.game.player.reward = 0
        self.prev_reward = 0.0
        self._steps = 0
        return self.handler.get_state()

    def step(self, action: int) -> tuple[np.ndarray, float, bool]:
        self._steps += 1
        dir_map = ["UP", "DOWN", "LEFT", "RIGHT"]
        opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        chosen = dir_map[int(action) % 4]
        if chosen != opposite.get(self.game.player.direction):
            self.game.player.direction = chosen
        self.game.player.move()
        self.game.collision()
        if self.render_mode and self.game.main == -1:
            self.game.item_repeat_run()
        state = self.handler.get_state()
        curr_reward = float(self.game.player.reward)
        reward = curr_reward - self.prev_reward
        self.prev_reward = curr_reward
        done = (not self.game.player.active) or (self._steps >= 1500) or bool(getattr(self.game, "exit", False))
        return state, reward, done


def train_dqn(
    episodes: int = 100,
    game: Snake_Game | None = None,
    framework: str = "pytorch",
    render: bool = True,
):
    env = SnakeEnv(game=game, render=render)
    trainer = QLearningTrainer(
        env=env,
        episodes=episodes,
        framework=framework,
        stop_fn=lambda: bool(getattr(env.game, "exit", False)),
        on_episode_fn=lambda ep, _r, _e: setattr(env.game, "generation", ep),
    )
    return trainer.train()


if __name__ == "__main__":
    model = train_dqn(episodes=50, render=False)
    save_model(model, None, "qlearning_snake.pth")

