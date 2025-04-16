from flask import Flask, request, jsonify, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random
import statistics
import math

app = Flask(__name__)

# ----------------------
# Configurable Constants
# ----------------------
MAX_HISTORY = 10
TRAFFIC_CAP = 40  # Mbps limit per server
BASE_LATENCY = random.uniform(20, 40)  # ms baseline per container

# ----------------------
# Metrics
# ----------------------
latency_gauge = Gauge("latency_ms", "Simulated latency in milliseconds")
throughput_gauge = Gauge("throughput_mbps", "Simulated throughput in Mbps")
error_rate_gauge = Gauge("error_rate", "Error rate (0-1)")
load_gauge = Gauge("avg_load", "Average traffic load over recent requests")
load_variance_gauge = Gauge("load_variance", "Variance of recent traffic load")

# ----------------------
# Traffic load history
# ----------------------
load_history = []

# ----------------------
# Helper: Dynamic latency based on time
# ----------------------
def dynamic_latency(base_latency, current_traffic):
    t = time.time() % 60
    fluctuation = 10 * math.sin(t / 10)  # cyclical every ~minute
    overload_penalty = max(0, current_traffic - TRAFFIC_CAP) * 5  # 5ms penalty per unit overload
    return base_latency + fluctuation + overload_penalty

# ----------------------
# Helper: Dynamic throughput calculation
# ----------------------
def dynamic_throughput(load):
    base = min(load, TRAFFIC_CAP)
    noise = random.uniform(-2, 2)
    return base + noise

# ----------------------
# Serve endpoint
# ----------------------
@app.route("/serve", methods=["POST"])
def serve():
    try:
        traffic = float(request.json.get("traffic_load", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

    # Track traffic history
    load_history.append(traffic)
    if len(load_history) > MAX_HISTORY:
        load_history.pop(0)

    avg_load = statistics.mean(load_history)
    load_variance = statistics.variance(load_history) if len(load_history) > 1 else 0.0
    latency = dynamic_latency(BASE_LATENCY, traffic)
    throughput = dynamic_throughput(traffic)
    error_rate = min(1.0, max(0, (traffic - TRAFFIC_CAP) / 20))  # penalize overload

    # Update Prometheus gauges
    latency_gauge.set(latency)
    throughput_gauge.set(throughput)
    error_rate_gauge.set(error_rate)
    load_gauge.set(avg_load)
    load_variance_gauge.set(load_variance)

    return jsonify({
        "avg_load": round(avg_load, 2),
        "load_variance": round(load_variance, 2),
        "latency_ms": round(latency, 2),
        "throughput_mbps": round(throughput, 2),
        "error_rate": round(error_rate, 2),
        "handled_traffic": round(traffic, 2),
        "status": "ok"
    })

# ----------------------
# /metrics endpoint for Prometheus
# ----------------------
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
