import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque
from Game.Snake_Game import Snake_Game
from AI.AI_Controller import AIHandler
from AI.Neural_Network import SimpleNN
class ReplayMemory:
    def __init__(self, capacity: int):
        self.memory = deque(maxlen=capacity)
    def push(self, transition: tuple):
        self.memory.append(transition)
    def sample(self, batch_size: int):
        return random.sample(self.memory, batch_size)
    def __len__(self) -> int:
        return len(self.memory)
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
        # Reinicia el juego y devuelve el estado inicial
        self.game.reset(True)
        self.prev_reward = 0
        return self.handler.get_state()

    def step(self, action: int) -> tuple:
        # Ejecuta la acción y retorna (next_state, reward, done)
        dir_map = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.game.player.direction = dir_map[action]
        self.game.player.move()
        self.game.collision()
        state = self.handler.get_state()
        curr_reward = self.game.player.reward
        reward = curr_reward - self.prev_reward
        self.prev_reward = curr_reward
        done = not self.game.player.active
        if done:
            # Opcional: reiniciar internamente para la próxima llamada a reset
            pass
        return state, reward, done

class DQNAgent:
    def __init__(self,state_size: int,action_size: int,lr: float = 1e-3,gamma: float = 0.99,epsilon_start: float = 1.0
                ,epsilon_end: float = 0.01,epsilon_decay: float = 0.995,memory_size: int = 10000,batch_size: int = 64,target_update: int = 100):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.steps_done = 0
        self.target_update = target_update
        self.policy_net = SimpleNN(state_size, action_size)
        self.target_net = SimpleNN(state_size, action_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
