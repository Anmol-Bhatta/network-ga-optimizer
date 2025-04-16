import time
import random
import requests

servers = [
    "http://server-1:80/serve",
    "http://server-2:80/serve",
    "http://server-3:80/serve"
]

def send_load():
    while True:
        for server in servers:
            traffic = random.uniform(10, 80)  # Varying loads
            try:
                res = requests.post(server, json={"traffic_load": traffic}, timeout=2)
                if res.ok:
                    print(f"[OK] {server} <- {traffic:.2f}")
                else:
                    print(f"[ERR] {server} <- {traffic:.2f} ({res.status_code})")
            except Exception as e:
                print(f"[FAIL] {server}: {e}")
        time.sleep(5)

if __name__ == "__main__":
    send_load()
