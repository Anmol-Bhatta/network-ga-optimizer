from flask import Flask, request, jsonify
import time
import random
import statistics

app = Flask(__name__)

# Maintain load history
load_history = []
MAX_HISTORY = 10

@app.route("/serve", methods=["POST"])
def serve():
    try:
        traffic = float(request.json.get("traffic_load", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

    # Track history and simulate overload behavior
    load_history.append(traffic)
    if len(load_history) > MAX_HISTORY:
        load_history.pop(0)
    avg_load = statistics.mean(load_history)

    # Simulate response behavior
    base_latency = random.uniform(0.1, 0.4)  # base latency in seconds
    degradation = 1 + (avg_load / 100)       # higher load → higher latency
    latency = base_latency * degradation
    time.sleep(latency)

    # Throughput drops as load increases
    throughput = max(0.1, 100 - traffic * random.uniform(0.5, 1.5))

    # Simulate error rate
    error_rate = 0.0
    if traffic > 80:
        if random.random() < 0.3:
            error_rate = 1.0
            return jsonify({"error": "Overloaded", "error_rate": error_rate}), 500

    return jsonify({
        "latency_ms": round(latency * 1000, 2),
        "throughput_mbps": round(throughput, 2),
        "error_rate": error_rate,
        "handled_traffic": traffic,
        "avg_load": round(avg_load, 2)
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
