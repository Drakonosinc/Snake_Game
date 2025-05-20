import sys
from Game.Snake_Game import *
from AI.Genetic_Algorithm import *
if __name__=="__main__":
    while True:
        (game:=Snake_Game()).run()
        game.game_over=False
        match game.mode_game:
            case {"Training AI": True}:
                best_model = genetic_algorithm(game, input_size=len(game.ai_handler.get_state()), output_size=4, generations=game.config.config_AI["generation_value"], population_size=game.config.config_AI["population_value"], num_trials=game.config.config_AI["try_for_ai"])
                game.models = best_model
                if game.config.config_AI["model_save"]:save_model(game.models, torch.optim.Adam(game.models.parameters(), lr=0.001),game.model_path)
            case {"Player": True} | {"AI": True}:game.run_with_models()
        if game.exit:break
pygame.quit(),sys.exit()