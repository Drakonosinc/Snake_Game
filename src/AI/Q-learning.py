import numpy as np
import torch
from Game.Snake_Game import Snake_Game
from AI.AI_Controller import AIHandler
from pyforgeai import DQNAgent, ReplayMemory, SimpleNN


class SnakeEnv:
    """Wrapper del juego Snake para interfaz Gym-like."""
    def __init__(self):
        self.game = Snake_Game()
        self.handler = AIHandler(self.game)
        self.prev_reward = 0

    @property
    def action_space(self) -> int:
        return 4

    def reset(self) -> np.ndarray:
        self.game.reset(True)
        self.prev_reward = 0
        return self.handler.get_state()

    def step(self, action: int) -> tuple:
        dir_map = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.game.player.direction = dir_map[action]
        self.game.player.move()
        self.game.collision()
        state = self.handler.get_state()
        curr_reward = self.game.player.reward
        reward = curr_reward - self.prev_reward
        self.prev_reward = curr_reward
        done = not self.game.player.active
        return state, reward, done


def train_dqn(episodes: int = 500):
    env = SnakeEnv()
    state = env.reset()
    agent = DQNAgent(state_size=len(state), action_size=env.action_space)
    for episode in range(1, episodes + 1):
        state = env.reset()
        total_reward = 0
        done = False
        while not done:
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            agent.store_transition(state, action, reward, next_state, done)
            agent.optimize_model()
            state = next_state
            total_reward += reward
        print(f"Episodio {episode}/{episodes} - Recompensa total: {total_reward:.2f} - Epsilon: {agent.epsilon:.3f}")
    torch.save(agent.policy_net.state_dict(), 'qlearning_snake.pth')
    return agent


if __name__ == "__main__":
    train_dqn()
