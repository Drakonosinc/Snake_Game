import torch
import numpy as np
class AIController():
    def __init__(self):
        pass
    def get_state(self):
        return np.array([])
    def actions_AI(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.AI_actions(action)