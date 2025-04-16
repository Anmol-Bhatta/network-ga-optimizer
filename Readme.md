# Network Traffic Optimizer with Genetic Algorithm

This project simulates server-side traffic handling and applies a **Genetic Algorithm (GA)** to optimize traffic distribution across multiple Flask-based simulated servers. The system uses **Prometheus** for metric scraping and **Grafana** for monitoring and visualization.

---

## Components

### 1. `simulated_server/`
- A Flask app that simulates traffic processing on each server
- Exposes Prometheus metrics like:
  - `latency_ms`
  - `throughput_mbps`
  - `error_rate`
  - `avg_load`
  - `load_variance`

### 2. `ga_controller/`
- Genetic Algorithm optimizer that:
  - Sends load based on evolving weights
  - Evaluates response times, throughput, and error metrics
  - Finds optimal traffic split across servers

### 3. `load_driver/`
- Sends test traffic (simulated clients) to endpoints
- Works in coordination with the optimizer

### 4. `prometheus/`
- Prometheus config to scrape all servers at `/metrics`

### 5. `grafana/`
- Pre-provisioned dashboard to visualize:
  - Real-time `latency_ms`, `error_rate`, `throughput_mbps`, `traffic_load`

---

## How it Works
1. Each server simulates traffic response behavior.
2. Optimizer runs GA to find best traffic allocation percentages.
3. Load Driver mimics client requests using that allocation.
4. Prometheus scrapes metrics every 5s.
5. Grafana auto-loads dashboard to show panel data for all metrics.

---

## Metrics Breakdown
| Metric              | Description                                |
|---------------------|--------------------------------------------|
| `latency_ms`        | Current simulated request latency          |
| `throughput_mbps`   | Simulated server throughput                |
| `error_rate`        | Probability of overload/error response     |
| `avg_load`          | Average load based on recent requests      |
| `load_variance`     | Variance of load for stability tracking    |

---

## 🚀 Run the System
```bash
# From root directory
$ docker compose up --build
```

- Grafana: [http://localhost:3000](http://localhost:3000) (admin/admin)
- Prometheus: [http://localhost:9090](http://localhost:9090)

---

##Folder Structure
```
├── simulated_server/     # Flask servers with Prometheus metrics
├── ga_controller/        # GA optimizer logic
├── load_driver/          # Automated traffic simulator
├── prometheus/           # prometheus.yml config
├── grafana/              # dashboard.json and provisioning files
└── docker-compose.yml    # Orchestrates the setup
```

---

## 🔧 Next Steps
- [ ] Add alerts in Prometheus + Grafana
- [ ] Improve GA fitness function (multi-objective)
- [ ] Persist GA best configs
- [ ] Export metrics to CSV
- [ ] Deploy to Kubernetes

---


