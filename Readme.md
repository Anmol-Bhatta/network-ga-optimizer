Tech Stack

- Python 3.13
- Flask (for simulated servers)
- PyGAD (for genetic optimization)
- Docker & Docker Compose
- YAML for config

---

## Setup Instructions

### Prerequisites
- Docker Desktop installed and running
- Git installed

---

##Step-by-Step Setup

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/network-ga-optimizer.git
cd network-ga-optimizer
```

### 2. Start Docker Containers
This will start 3 server containers + the optimizer controller:
```bash
docker compose up --build
```
Or to run in background:
```bash
docker compose up -d
```

### 3. (Optional) Re-run the GA Optimizer Manually
```bash
docker compose run optimizer
```

### 4. View Logs
```bash
docker logs ga-controller
```

---

Configuration
Edit `config.yaml` to adjust:
- Number of generations
- Traffic allocation weights (latency, throughput, etc.)
- Mutation rate


---

## 📁 Project Structure
```
network-ga-project/
├── ga_controller/
│   ├── main.py
│   ├── ga_runner.py
│   ├── fitness_evaluator.py
│   ├── server_client.py
│   ├── config.yaml
│   ├── Dockerfile
│   └── requirements.txt
├── simulated_server/
│   ├── server-app.py
│   └── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## Using GRAFANA
To see the metrics in Grafana. Here's what to do:
Open Grafana in your browser: http://localhost:3000
Login with:
Username: admin
Password: admin
Add Prometheus as a data source:
Click on the gear icon (⚙️) in the left sidebar
Select "Data sources"
Click "Add data source"
Select "Prometheus"
Set the URL to: http://prometheus:9090
Click "Save & Test"
Import the dashboard:
Click on the "+" icon in the left sidebar
Select "Import"
Click "Upload JSON file"
Select the grafana/dashboard.json file
Click "Import"
The dashboard will show:
Traffic Load: Shows the current traffic load on each server
Request Latency: Shows the average latency of requests in milliseconds
Throughput: Shows the current throughput in Mbps
Error Count: Shows the number of errors on each server

Next plan:
- [In Review] Add Prometheus & Grafana for observability
- [ ] Log best GA results to CSV
- [ ] Add REST API trigger for GA runs
- [ ] Compare with round-robin baseline
