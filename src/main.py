import sys
from Game.Snake_Game import *
from pyforgeai import genetic_algorithm, save_model


def _evaluate_snake_model(game, model):
    game.models = model
    res = game.run_with_models()
    if isinstance(res, (list, tuple)):
        return float(res[0]) if res else 0.0
    return float(res)


if __name__ == "__main__":
    while True:
        (game := Snake_Game()).run()
        game.game_over = False
        match game.mode_game:
            case {"Training AI": True}:
                best_model = genetic_algorithm(
                    target=lambda m: _evaluate_snake_model(game, m),
                    input_size=len(game.ai_handler.get_state()),
                    output_size=4,
                    generations=game.config.config_AI["generation_value"],
                    population_size=game.config.config_AI["population_value"],
                    num_trials=game.config.config_AI["try_for_ai"],
                    stop_fn=lambda: bool(getattr(game, "exit", False)),
                    on_generation_fn=lambda g: setattr(game, "generation", g),
                )
                game.models = best_model
                if game.config.config_AI["model_save"] and best_model is not None:
                    save_model(game.models, torch.optim.Adam(game.models.parameters(), lr=0.001), game.model_path)
            case {"Player": True} | {"AI": True}:
                game.run_with_models()
        if game.exit:
            break
pygame.quit(), sys.exit()
