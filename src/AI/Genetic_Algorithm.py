import random
import torch
from typing import List, Tuple, Optional
from tqdm import tqdm  # Barra de progreso para el bucle de generaciones
from .Neural_Network import SimpleNN  # Import explícito en lugar de wildcard

def fitness_function(model: SimpleNN, game) -> float:
    """Evalúa el fitness de un modelo en el juego y retorna el puntaje."""
    game.models = model  # Asignar modelo al juego para evaluación
    score = game.run_with_models()
    print(f"Score: {score}")
    return score

def initialize_population(size, input_size, output_size):
    population = []
    for _ in range(size):
        model = SimpleNN(input_size, output_size)
        population.append(model)
    return population

def evaluate_population(population: List[SimpleNN], game, num_trials: int = 3) -> List[float]:
    """Evalúa cada modelo en la población y retorna la lista de fitness promedio."""
    fitness_scores = []
    for model in population:
        score = [fitness_function(model, game) for _ in range(num_trials)]
        fitness_scores.append(sum(score) / num_trials)
    min_score = abs(min(fitness_scores)) if min(fitness_scores) < 0 else 0
    fitness_scores = [score + min_score + 1 for score in fitness_scores]  # Asegúrate de que todos los fitness sean positivos
    return fitness_scores

def select_parents(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:weights = [1 / len(fitness_scores)] * len(fitness_scores)
    else:weights = [score / total_fitness for score in fitness_scores]
    selected = random.choices(population, weights=weights, k=len(population))
    return selected

def crossover(parent1, parent2):
    child1, child2 = (
        SimpleNN(parent1.fc1.in_features, parent2.fc3.out_features),
        SimpleNN(parent2.fc1.in_features, parent1.fc3.out_features),
    )
    for p1, p2, c1, c2 in zip(parent1.parameters(), parent2.parameters(), child1.parameters(), child2.parameters()):
        mask = torch.rand_like(p1) > 0.5
        c1.data.copy_(torch.where(mask, p1.data, p2.data))
        c2.data.copy_(torch.where(mask, p2.data, p1.data))
    return child1, child2

def mutate(model, mutation_rate=0.02, strong_mutation_rate=0.1):
    with torch.no_grad():
        for param in model.parameters():
            if random.random() < mutation_rate:param.add_(torch.clamp(torch.randn(param.size()) * 0.2, -0.5, 0.5))
            if random.random() < strong_mutation_rate:param.add_(torch.clamp(torch.randn(param.size()) * 0.7, -1.0, 1.0))
    return model

def genetic_algorithm(game, input_size: int, output_size: int, generations: int = 100, population_size: int = 20, initial_mutation_rate: float = 0.01, strong_mutation_rate: float = 0.05, elitism_rate: float = 0.05, num_trials: int = 3) -> SimpleNN:
    """Ejecuta algoritmo genético para optimizar redes neuronales."""
    population = initialize_population(population_size, input_size, output_size)
    elite_size = max(1, int(elitism_rate * population_size))
    mutation_rate = initial_mutation_rate
    previous_best_score = float('-inf')

    for generation in tqdm(range(generations), desc="Generaciones GA"):
        game.generation = generation
        fitness_scores = evaluate_population(population, game, num_trials)

        # Ajuste adaptativo de mutación
        current_best_score = max(fitness_scores)
        if current_best_score <= previous_best_score:
            mutation_rate = min(mutation_rate * 1.5, 0.1)
        else:
            mutation_rate = initial_mutation_rate
        previous_best_score = current_best_score

        # Selección de élite
        elite_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:elite_size]
        elites = [population[i] for i in elite_indices]

        # Selección de padres y reproducción
        parents = select_parents(population, fitness_scores)
        next_population = elites[:]

        for i in range(0, len(parents) - elite_size, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child1, child2 = crossover(parent1, parent2)
            next_population.append(mutate(child1, mutation_rate, strong_mutation_rate))
            if len(next_population) < population_size:
                next_population.append(mutate(child2, mutation_rate, strong_mutation_rate))

        # Inyección de diversidad cada 10 generaciones
        if generation % 10 == 0:
            num_random = population_size // 5
            random_models = initialize_population(num_random, input_size, output_size)
            next_population = next_population[:population_size - num_random] + random_models

        population = next_population[:population_size]

    # Selección del mejor modelo
    fitness_scores = evaluate_population(population, game, num_trials)
    best_model = population[fitness_scores.index(max(fitness_scores))]
    return best_model

def save_model(model, optimizer, path):
    print("save model")
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, path)

def load_model(path, input_size, output_size, optimizer=None):
    try:
        print("load model")
        model = SimpleNN(input_size, output_size)
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint['model_state_dict'])
        if optimizer:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model
    except FileNotFoundError:
        print(f"The file {path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None