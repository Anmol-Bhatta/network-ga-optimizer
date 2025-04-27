from ga_runner import run_ga
from fitness_evaluator import normalize_distribution, evaluate_solution
import yaml
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import time
import requests
import numpy as np

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

# --- Weighted Round Robin Comparison ---
# Use weights from config to split traffic proportionally
weighted_rr_weights = config.get("weighted_rr_weights", [1]*len(SERVERS))
total_weight = sum(weighted_rr_weights)
weighted_rr = [w / total_weight for w in weighted_rr_weights]
weighted_rr_fitness = evaluate_solution(weighted_rr)
print(f"Weighted Round Robin Fitness Score: {round(weighted_rr_fitness, 3)}")

# --- Per-Server Metrics Comparison ---
def get_metrics_for_allocation(allocation):
    metrics = []
    for i, weight in enumerate(allocation):
        traffic = weight * 100
        result = evaluate_solution([weight if j == i else 0 for j in range(len(SERVERS))])
        metrics.append(result)
    return metrics

# Helper to get per-server metrics for a given allocation
def get_server_metrics(allocation):
    metrics = []
    for i, weight in enumerate(allocation):
        traffic = weight * 100
        response = requests.post(SERVERS[i], json={"traffic_load": traffic}, timeout=2)
        if response.status_code == 200:
            metrics.append(response.json())
        else:
            metrics.append({"throughput_mbps": 0, "latency_ms": 1000, "error_rate": 1})
    return metrics

# Get per-server metrics for each method
methods = {
    "GA": normalized_best,
    "Round Robin": [1 / len(SERVERS)] * len(SERVERS),
    "Weighted RR": weighted_rr
}
per_server_metrics = {k: get_server_metrics(v) for k, v in methods.items()}

# Plot per-server metrics (throughput, latency, error rate)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
metrics_names = ["throughput_mbps", "latency_ms", "error_rate"]
metrics_labels = ["Throughput (Mbps)", "Latency (ms)", "Error Rate"]
bar_width = 0.2
x = np.arange(len(SERVERS))

for idx, (metric, label) in enumerate(zip(metrics_names, metrics_labels)):
    for i, (method, metrics_list) in enumerate(per_server_metrics.items()):
        values = [m.get(metric, 0) for m in metrics_list]
        axes[idx].bar(x + i * bar_width, values, bar_width, label=method)
    axes[idx].set_xticks(x + bar_width)
    axes[idx].set_xticklabels([f"Server {i+1}" for i in x])
    axes[idx].set_title(label)
    axes[idx].legend()
    axes[idx].grid(True)

plt.tight_layout()
per_server_plot_path = os.path.join(os.path.dirname(__file__), "per_server_metrics.png")
plt.savefig(per_server_plot_path)
print(f"Saved per-server metrics plot as {per_server_plot_path}")

# --- Visualization ---
labels = [f"Server {i+1}" for i in range(len(SERVERS))]
ga_percents = [round(r * 100, 2) for r in normalized_best]
rr_percents = [100/len(SERVERS)] * len(SERVERS)
weighted_rr_percents = [round(w * 100, 2) for w in weighted_rr]

x = range(len(SERVERS))
width = 0.25
fig, ax = plt.subplots()
rects1 = ax.bar([i - width for i in x], ga_percents, width, label='GA Allocation')
rects2 = ax.bar([i for i in x], rr_percents, width, label='Round Robin')
rects3 = ax.bar([i + width for i in x], weighted_rr_percents, width, label='Weighted RR')

ax.set_ylabel('Traffic Allocation (%)')
ax.set_title('Traffic Allocation: GA vs RR vs Weighted RR')
ax.set_xticks(list(x))
ax.set_xticklabels(labels)
ax.legend()

# Annotate bars
for rect in rects1 + rects2 + rects3:
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