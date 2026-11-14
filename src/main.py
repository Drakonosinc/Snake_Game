import importlib
import sys
import pygame
from Game.Snake_Game import Snake_Game
from pyforgeai import genetic_algorithm, save_model


def _evaluate_snake_model(game, model):
    game.models = model
    res = game.run_with_models()
    if isinstance(res, (list, tuple)):
        return float(res[0]) if res else 0.0
    return float(res)


if __name__ == "__main__":
    game = Snake_Game()
    while not game.exit:
        game.run()
        if game.exit:
            break
        game.game_over = False
        use_tf = bool(game.config.config_AI.get("type_model", {}).get("Tensorflow", False))
        framework = "tensorflow" if use_tf else "pytorch"
        use_qlearning = bool(game.config.config_AI.get("type_training", {}).get("q-learning", False))

        match game.mode_game:
            case {"Training AI": True}:
                if use_qlearning:
                    ql_mod = importlib.import_module("AI.Q-learning")
                    best_model = ql_mod.train_dqn(
                        episodes=game.config.config_AI["generation_value"],
                        game=game,
                        framework=framework,
                        render=True,
                    )
                else:
                    best_model = genetic_algorithm(
                        target=lambda m: _evaluate_snake_model(game, m),
                        input_size=len(game.ai_handler.get_state()),
                        output_size=4,
                        generations=game.config.config_AI["generation_value"],
                        population_size=game.config.config_AI["population_value"],
                        num_trials=game.config.config_AI["try_for_ai"],
                        framework=framework,
                        stop_fn=lambda: bool(getattr(game, "exit", False)) or game.main == 0,
                        on_generation_fn=lambda g: setattr(game, "generation", g),
                    )
                if best_model is not None:
                    game.models = best_model
                    if game.config.config_AI["model_save"]:
                        game.load_AI()
                        save_model(best_model, None, game.model_path)
                        game.load_AI()
                game.mode_game["Training AI"] = False
                if not game.exit:
                    game.main = 0
            case {"Player": True} | {"AI": True}:
                game.run_with_models()
    pygame.quit()
    sys.exit()

