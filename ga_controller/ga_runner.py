import pygad
import yaml
from fitness_evaluator import evaluate_solution

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SERVERS = config["servers"]
GA_CONFIG = config["ga"]

NUM_SERVERS = len(SERVERS)

def fitness_func(ga_instance, solution, solution_idx):
    return evaluate_solution(solution)

def run_ga():
    best_fitness_per_gen = []
    patience = 20  # Number of generations with no improvement before stopping
    best_fitness = None
    generations_since_improvement = 0

    def on_generation(ga):
        nonlocal best_fitness, generations_since_improvement
        current_fitness = ga.best_solution()[1]
        best_fitness_per_gen.append(current_fitness)
        if best_fitness is None or current_fitness > best_fitness:
            best_fitness = current_fitness
            generations_since_improvement = 0
        else:
            generations_since_improvement += 1
        # Early stopping condition
        if generations_since_improvement >= patience:
            print(f"Early stopping: No improvement in {patience} generations.")
            ga.stop_run = True

    ga_instance = pygad.GA(
        num_generations=GA_CONFIG["generations"],
        num_parents_mating=GA_CONFIG["parents_mating"],
        fitness_func=fitness_func,
        sol_per_pop=GA_CONFIG["population_size"],
        num_genes=NUM_SERVERS,
        init_range_low=0.1,
        init_range_high=1.0,
        mutation_percent_genes=GA_CONFIG["mutation_percent"],
        mutation_type="random",
        gene_space={'low': 0.1, 'high': 1.0},
        on_generation=on_generation
    )

    ga_instance.run()
    ga_instance.best_fitness_per_gen = best_fitness_per_gen
    return ga_instance
