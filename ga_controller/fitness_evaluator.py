import statistics
import yaml
from server_client import send_traffic

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SERVERS = config["servers"]
WEIGHTS = config["weights"]


def normalize_distribution(distribution):
    total = sum(distribution)
    return [x / total for x in distribution] if total > 0 else [1 / len(distribution)] * len(distribution)


def evaluate_solution(solution):
    traffic_distribution = normalize_distribution(solution)

    latencies = []
    throughputs = []
    error_rates = []

    for i, weight in enumerate(traffic_distribution):
        traffic = weight * 100
        print(f"  → Sending {traffic:.2f}% to {SERVERS[i]}")
        metrics = send_traffic(SERVERS[i], traffic)
        print(f"     ← Received: {metrics}")

        latencies.append(metrics.get("latency_ms", 1000))
        throughputs.append(metrics.get("throughput_mbps", 0))
        error_rates.append(metrics.get("error_rate", 1))

    avg_latency = sum(latencies) / len(latencies)
    avg_throughput = sum(throughputs) / len(throughputs)
    avg_error = sum(error_rates) / len(error_rates)
    load_variance = statistics.stdev(traffic_distribution) if len(traffic_distribution) > 1 else 0

    # Weighted fitness function (moderate penalties for error and variance)
    score = (
        (avg_throughput * WEIGHTS["throughput"]) -
        (avg_latency * WEIGHTS["latency"]) -
        (avg_error * 20 * WEIGHTS["error_rate"]) -
        (load_variance * 10 * WEIGHTS["load_variance"])
    )
    print(f"Raw fitness score: {score}")
    return score