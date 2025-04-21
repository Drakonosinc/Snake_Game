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
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.memory = ReplayMemory(memory_size)
    def select_action(self, state: np.ndarray) -> int:
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        with torch.no_grad():
            tensor_state = torch.tensor(state, dtype=torch.float32)
            q_values = self.policy_net(tensor_state)
            return int(torch.argmax(q_values).item())
    def store_transition(self, state, action, reward, next_state, done):
        self.memory.push((state, action, reward, next_state, done))
    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return
        transitions = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*transitions)
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1)
        current_q = self.policy_net(states).gather(1, actions)
        next_q = self.target_net(next_states).max(1)[0].detach().unsqueeze(1)
        expected_q = rewards + (1 - dones) * self.gamma * next_q
        loss = nn.MSELoss()(current_q, expected_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.steps_done += 1
        if self.steps_done % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

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
if __name__ == "__main__":train_dqn()