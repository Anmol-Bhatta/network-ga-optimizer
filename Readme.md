Tech Stack

- Python 3.13
- Flask (for simulated servers)
- PyGAD (for genetic optimization)
- Docker & Docker Compose
- YAML for config

---

## 🛠️ Setup Instructions

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
