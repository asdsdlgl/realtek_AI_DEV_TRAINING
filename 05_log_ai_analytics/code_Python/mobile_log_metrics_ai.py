"""
mobile_log_metrics_ai.py
功能：
- 逐行讀取 example_mobile_ai.log
- 解析並統計關鍵 metrics
- 印出結果，可選輸出 JSON / CSV
"""

from pathlib import Path
import json
import csv
from collections import defaultdict, Counter
from datetime import datetime

LOG_FILE = Path("dataset/example_mobile_ai.log")

def parse_line_naive(line: str):
    line = line.strip()
    if not line:
        return None
    parts = line.split()
    if len(parts) < 4:
        return {"raw": line}
    timestamp = f"{parts[0]} {parts[1]}"
    level = parts[2]
    source = parts[3]
    message = " ".join(parts[4:])
    return {
        "timestamp": timestamp,
        "level": level,
        "source": source,
        "message": message,
    }

def calculate_latencies(log_entries):
    latencies = defaultdict(list)
    
    for entry in log_entries:
        if 'ai_model_latency' in entry['message']:
            latency_ms = float(entry['message'].split('latency=')[1].split(',')[0])
            model_name = entry['source']
            latencies[model_name].append(latency_ms)
    
    return {model: {
                "avg_latency_ms": sum(lats) / len(lats),
                "p95_latency_ms": sorted(lats)[int(len(lats) * 0.95)]
              } for model, lats in latencies.items()}

def count_user_logins(log_entries):
    login_counts = defaultdict(lambda: {"success": 0, "failure": 0})
    
    for entry in log_entries:
        if 'user_login' in entry['message']:
            user_id = entry['message'].split('user=')[1].split(',')[0]
            result = entry['message'].split('result=')[1].split(',')[0]
            login_counts[user_id][result] += 1
    
    return {user: {
                "login_success_count": counts["success"],
                "login_failure_count": counts["failure"]
              } for user, counts in login_counts.items()}

def count_http_status(log_entries):
    status_counts = Counter()
    
    for entry in log_entries:
        if 'http_status' in entry['message']:
            status_code = int(entry['message'].split('status=')[1].split(',')[0])
            status_counts[status_code] += 1
    
    return {
        "http_2xx_count": status_counts[200],
        "http_4xx_count": sum(counts for code, counts in status_counts.items() if 400 <= code < 500),
        "http_5xx_count": sum(counts for code, counts in status_counts.items() if 500 <= code < 600)
    }

def count_network_events(log_entries):
    event_counts = Counter()
    
    for entry in log_entries:
        if 'network_event' in entry['message']:
            event_type = entry['message'].split('event=')[1].split(',')[0]
            event_counts[event_type] += 1
    
    return {
        "wifi_disconnected_count": event_counts["wifi_disconnected"],
        "tcp_reset_count": event_counts["tcp_reset"],
        "http_504_count": event_counts.get("http_504", 0),
        "http_503_count": event_counts.get("http_503", 0)
    }

def main():
    if not LOG_FILE.exists():
        print(f"[ERROR] log file not found: {LOG_FILE}")
        return
    
    print("[INFO] reading log file: ", LOG_FILE)
    with LOG_FILE.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    
    log_entries = [parse_line_naive(line) for line in lines if parse_line_naive(line)]
    
    latencies = calculate_latencies(log_entries)
    user_logins = count_user_logins(log_entries)
    http_statuses = count_http_status(log_entries)
    network_events = count_network_events(log_entries)
    
    print("\nLatencies:")
    for model, metrics in latencies.items():
        print(f"  {model}: avg_latency_ms={metrics['avg_latency_ms']:.2f}, p95_latency_ms={metrics['p95_latency_ms']:.2f}")
    
    print("\nUser Logins:")
    for user, counts in user_logins.items():
        print(f"  {user}: login_success_count={counts['login_success_count']}, login_failure_count={counts['login_failure_count']}")
    
    print("\nHTTP Statuses:")
    print(f"  http_2xx_count: {http_statuses['http_2xx_count']}")
    print(f"  http_4xx_count: {http_statuses['http_4xx_count']}")
    print(f"  http_5xx_count: {http_statuses['http_5xx_count']}")
    
    print("\nNetwork Events:")
    print(f"  wifi_disconnected_count: {network_events['wifi_disconnected_count']}")
    print(f"  tcp_reset_count: {network_events['tcp_reset_count']}")
    print(f"  http_504_count: {network_events['http_504_count']}")
    print(f"  http_503_count: {network_events['http_503_count']}")
    
    # Output to JSON
    metrics_dict = {
        "latencies": latencies,
        "user_logins": user_logins,
        "http_statuses": http_statuses,
        "network_events": network_events
    }
    print("\nMetrics JSON:")
    print(json.dumps(metrics_dict, indent=2))
    
    # Output to CSV
    with open("metrics.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["model", "avg_latency_ms", "p95_latency_ms"])
        for model, metrics in latencies.items():
            writer.writerow([model, metrics['avg_latency_ms'], metrics['p95_latency_ms']])
    
    with open("user_logins.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["user", "login_success_count", "login_failure_count"])
        for user, counts in user_logins.items():
            writer.writerow([user, counts['login_success_count'], counts['login_failure_count']])
    
    with open("http_statuses.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["status_code", "count"])
        writer.writerow([200, http_statuses["http_2xx_count"]])
        writer.writerow([400, http_statuses["http_4xx_count"]])
        writer.writerow([500, http_statuses["http_5xx_count"]])

    with open("network_events.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["event_type", "count"])
        writer.writerow(["wifi_disconnected", network_events["wifi_disconnected_count"]])
        writer.writerow(["tcp_reset", network_events["tcp_reset_count"]])
        writer.writerow(["http_504", network_events["http_504_count"]])
        writer.writerow(["http_503", network_events["http_503_count"]])

if __name__ == "__main__":
    main()