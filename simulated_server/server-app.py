from flask import Flask, request, jsonify
import time
import random
import statistics
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.exposition import MetricsHandler

app = Flask(__name__)

# Prometheus metrics
request_latency = Histogram('request_latency_seconds', 'Request latency in seconds')
traffic_load = Gauge('traffic_load', 'Current traffic load')
throughput = Gauge('throughput_mbps', 'Current throughput in Mbps')
error_counter = Counter('error_total', 'Total number of errors')
avg_load = Gauge('average_load', 'Average load over time')

# Maintain load history
load_history = []
MAX_HISTORY = 10

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route("/serve", methods=["POST"])
def serve():
    try:
        traffic = float(request.json.get("traffic_load", 0))
    except (ValueError, TypeError):
        error_counter.inc()
        return jsonify({"error": "Invalid input"}), 400

    # Update Prometheus metrics
    traffic_load.set(traffic)
    
    # Track history and simulate overload behavior
    load_history.append(traffic)
    if len(load_history) > MAX_HISTORY:
        load_history.pop(0)
    current_avg_load = statistics.mean(load_history)
    avg_load.set(current_avg_load)

    # Simulate response behavior
    base_latency = random.uniform(0.1, 0.4)  # base latency in seconds
    degradation = 1 + (current_avg_load / 100)       # higher load → higher latency
    latency = base_latency * degradation
    
    # Record latency in Prometheus
    request_latency.observe(latency)
    time.sleep(latency)

    # Throughput drops as load increases
    current_throughput = max(0.1, 100 - traffic * random.uniform(0.5, 1.5))
    throughput.set(current_throughput)

    # Simulate error rate
    error_rate = 0.0
    if traffic > 80:
        if random.random() < 0.3:
            error_rate = 1.0
            error_counter.inc()
            return jsonify({"error": "Overloaded", "error_rate": error_rate}), 500

    return jsonify({
        "latency_ms": round(latency * 1000, 2),
        "throughput_mbps": round(current_throughput, 2),
        "error_rate": error_rate,
        "handled_traffic": traffic,
        "avg_load": round(current_avg_load, 2)
    })

@app.route("/status")
def status():
    simulated_latency = round(random.uniform(100, 400), 2)
    return jsonify({
        "status": "ok",
        "avg_load": round(statistics.mean(load_history), 2) if load_history else 0,
        "simulated_latency_estimate_ms": simulated_latency,
        "load_history": load_history[-5:]  # last 5 loads
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
