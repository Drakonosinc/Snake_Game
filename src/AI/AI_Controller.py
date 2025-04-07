import torch
import numpy as np
class AIHandler():
    def __init__(self, game):
        self.game = game
        self.direction_to_int = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}
    def get_state(self):
        direction_value = self.direction_to_int.get(self.game.player.direction, 0)
        max_body_segments = 4
        body_coords = []
        for segment in self.game.player.body[:max_body_segments]:
            if hasattr(segment, 'x') and hasattr(segment, 'y'):body_coords.extend([segment.x, segment.y])
            else:body_coords.extend([0, 0])
        while len(body_coords) < max_body_segments * 2:body_coords.extend([0, 0])
        state = [self.game.player.rect_head.x,self.game.player.rect_head.y,self.game.fruit.rect.x,self.game.fruit.rect.y,direction_value]
        state.extend(body_coords[:8])
        return np.array(state, dtype=np.float32)
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
        elif chosen_action == 3:self.game.player.direction = "RIGHT"