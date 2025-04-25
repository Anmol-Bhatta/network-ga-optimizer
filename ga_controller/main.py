from ga_runner import run_ga
from fitness_evaluator import normalize_distribution, evaluate_solution
import yaml
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import time

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

# --- Fitness Over Generations Plot ---
gen = list(range(1, len(ga_instance.best_fitness_per_gen) + 1))
plt.figure()
plt.plot(gen, ga_instance.best_fitness_per_gen, marker='o', label='Best Fitness')
plt.xlabel('Generation')
plt.ylabel('Best Fitness Score')
plt.title('GA Best Fitness Score Over Generations')
plt.grid(True)
plt.legend()
plt.tight_layout()
fitness_plot_path = os.path.join(os.path.dirname(__file__), "fitness_over_generations.png")
plt.savefig(fitness_plot_path)
print(f"Saved plot as {fitness_plot_path}")

# --- Round Robin Comparison ---
# For N servers, round robin is equal split
round_robin = [1 / len(SERVERS)] * len(SERVERS)
round_robin_fitness = evaluate_solution(round_robin)
print(f"Round Robin Fitness Score: {round(round_robin_fitness, 3)}")

# --- Visualization ---
labels = [f"Server {i+1}" for i in range(len(SERVERS))]
ga_percents = [round(r * 100, 2) for r in normalized_best]
rr_percents = [100/len(SERVERS)] * len(SERVERS)

x = range(len(SERVERS))
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar([i - width/2 for i in x], ga_percents, width, label='GA Allocation')
rects2 = ax.bar([i + width/2 for i in x], rr_percents, width, label='Round Robin')

ax.set_ylabel('Traffic Allocation (%)')
ax.set_title('Traffic Allocation: GA vs Round Robin')
ax.set_xticks(list(x))
ax.set_xticklabels(labels)
ax.legend()

# Annotate bars
for rect in rects1 + rects2:
    height = rect.get_height()
    ax.annotate(f'{height:.1f}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

plt.tight_layout()
plot_path = os.path.join(os.path.dirname(__file__), "ga_vs_round_robin.png")
plt.savefig(plot_path)
print(f"Saved plot as {plot_path}")
time.sleep(60)
# plt.show()  # Disabled for Docker