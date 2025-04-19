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
