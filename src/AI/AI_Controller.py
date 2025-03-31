import torch
import numpy as np
class AIController():
    def __init__(self, game):self.game = game
    def get_state(self):
        return np.array([self.game.player.rect_head.x, self.game.player.rect_head.y,self.game.fruit.x, self.game.fruit.y,
                        ])
    def actions_AI(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.AI_actions(action)
    def AI_actions(self,action):
        pass