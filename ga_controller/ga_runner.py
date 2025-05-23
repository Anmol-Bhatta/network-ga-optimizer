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
        gene_space={'low': 0.1, 'high': 1.0}
    )

    ga_instance.run()
    return ga_instance
