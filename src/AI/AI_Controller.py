import torch
import numpy as np
class AIHandler():
    def __init__(self, game):self.game = game
    def get_state(self):
        return np.array([self.game.player.rect_head.x, self.game.player.rect_head.y
                        ,self.game.fruit.x, self.game.fruit.y,*self.game.body, self.game.player.direction,])
    def actions_AI(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.AI_actions(action)
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()
    def AI_actions(self,action):
        probabilities = self.softmax(action)
        chosen_action = np.argmax(probabilities)
        if chosen_action == 0:self.game.player.direction = "UP"
        elif chosen_action == 1:self.game.player.direction = "DOWN"
        elif chosen_action == 2:self.game.player.direction = "LEFT"
        elif chosen_action == 2:self.game.player.direction = "RIGHT"