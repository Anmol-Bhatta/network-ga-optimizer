import requests
import yaml

# Load config.yaml once at startup
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SERVERS = config["servers"]
TIMEOUT = config["timeout"]


def send_traffic(server_url, traffic):
    """
    Sends a POST request with traffic to the given server URL.
    Returns a dictionary with performance metrics.
    """
    try:
        response = requests.post(
            server_url,
            json={"traffic_load": traffic},
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error_rate": 1.0}  # Server error or overload
    except requests.exceptions.RequestException:
        print(f"[ERROR] Failed to reach {server_url}: {e}")
    return {"error_rate": 1.0}
