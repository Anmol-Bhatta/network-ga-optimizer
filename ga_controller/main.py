from ga_runner import run_ga
from fitness_evaluator import normalize_distribution
import yaml

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SERVERS = config["servers"]

# Run GA
print("Running Genetic Algorithm optimization...")
ga_instance = run_ga()

# Get best solution
best_solution, best_fitness, _ = ga_instance.best_solution()
normalized_best = normalize_distribution(best_solution)

print("\nBest Traffic Allocation:")
for i, ratio in enumerate(normalized_best):
    percent = round(ratio * 100, 2)
    print(f"Server {i + 1} ({SERVERS[i]}): {percent}%")

print(f"\nBest Fitness Score: {round(best_fitness, 3)}")