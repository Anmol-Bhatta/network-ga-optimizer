# utils.py (optional helper functions)

def scale_to_percent(values):
    total = sum(values)
    return [round((v / total) * 100, 2) if total else 0 for v in values]


def log_traffic_result(server_urls, distribution):
    print("\nFinal Traffic Split:")
    for i, percent in enumerate(scale_to_percent(distribution)):
        print(f"  {server_urls[i]} → {percent}%")