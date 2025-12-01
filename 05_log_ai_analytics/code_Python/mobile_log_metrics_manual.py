"""
mobile_log_metrics_manual.py

最出版：只做非常基本的統計，讓學員感受到：
- 如果要多加幾個指標會很累
- 適合交給 AI 來補強

目標：
- 計算 ERROR / WARN / INFO 行數
- 粗略抓出 AIInference model 的 latency_ms 數值平均
"""

from pathlib import Path

LOG_FILE = Path("../datasets/example_mobile_ai.log")


def main():
    if not LOG_FILE.exists():
        print(f"[ERROR] log file not found: {LOG_FILE}")
        return

    count_info = count_warn = count_error = 0
    asr_latencies = []

    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if " INFO " in line:
                count_info += 1
            if " WARN " in line:
                count_warn += 1
            if " ERROR " in line:
                count_error += 1

            if "AIInference" in line and "latency_ms=" in line:
                # 非常 naive 的取值方式
                parts = line.split("latency_ms=")
                if len(parts) > 1:
                    right = parts[1]
                    num_str = ""
                    for ch in right:
                        if ch.isdigit():
                            num_str += ch
                        else:
                            break
                    if num_str:
                        asr_latencies.append(int(num_str))

    print(f"[INFO] INFO count  = {count_info}")
    print(f"[INFO] WARN count  = {count_warn}")
    print(f"[INFO] ERROR count = {count_error}")

    if asr_latencies:
        avg = sum(asr_latencies) / len(asr_latencies)
        print(f"[INFO] AIInference latency count = {len(asr_latencies)}, avg = {avg:.2f} ms")
    else:
        print("[INFO] no AIInference latency found")


if __name__ == "__main__":
    main()