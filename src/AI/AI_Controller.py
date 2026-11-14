import torch
import numpy as np


class AIHandler:
    def __init__(self, game):
        self.game = game
        self.direction_to_int = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}

    def get_state(self):
        direction_value = self.direction_to_int.get(self.game.player.direction, 0)
        max_body_segments = 4
        body_coords = []
        for segment in self.game.player.body[:max_body_segments]:
            if hasattr(segment, "x") and hasattr(segment, "y"):
                body_coords.extend([segment.x, segment.y])
            else:
                body_coords.extend([0, 0])
        while len(body_coords) < max_body_segments * 2:
            body_coords.extend([0, 0])
        state = [
            self.game.player.rect_head.x,
            self.game.player.rect_head.y,
            self.game.fruit.rect.x,
            self.game.fruit.rect.y,
            direction_value,
        ]
        state.extend(body_coords[:8])
        return np.array(state, dtype=np.float32)

    def _infer(self, model, state: np.ndarray) -> np.ndarray:
        if hasattr(model, "predict"):
            out = model.predict(state)
            return np.asarray(out, dtype=np.float32).reshape(-1)
        with torch.no_grad():
            tensor_in = torch.tensor(state, dtype=torch.float32)
            out = model(tensor_in)
            if hasattr(out, "detach"):
                return out.detach().cpu().numpy().reshape(-1)
            return np.asarray(out, dtype=np.float32).reshape(-1)

    def actions_AI(self, model):
        if model is None:
            return
        state = self.get_state()
        action = self._infer(model, state)
        self.AI_actions(action)

    def softmax(self, x):
        x = np.asarray(x, dtype=np.float32).reshape(-1)
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()

    def AI_actions(self, action):
        probabilities = self.softmax(action)
        chosen_action = int(np.argmax(probabilities))
        cur = self.game.player.direction
        if chosen_action == 0 and cur != "DOWN":
            self.game.player.direction = "UP"
        elif chosen_action == 1 and cur != "UP":
            self.game.player.direction = "DOWN"
        elif chosen_action == 2 and cur != "RIGHT":
            self.game.player.direction = "LEFT"
        elif chosen_action == 3 and cur != "LEFT":
            self.game.player.direction = "RIGHT"
