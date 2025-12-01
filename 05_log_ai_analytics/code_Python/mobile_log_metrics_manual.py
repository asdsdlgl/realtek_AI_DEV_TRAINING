"""
mobile_log_basic_manual.py

最出版：非常基本的 log 解析示範。

功能：
- 逐行讀取 example_mobile_ai.log
- 粗略切出 timestamp / level / source / message
- 將結果印出，不做進一步統計

之後會用 AI 改寫成：
- dataclass / 結構化 parser
- 可以輸出 JSON / CSV
"""

from pathlib import Path

LOG_FILE = Path("dataset/example_mobile_ai.log")


def parse_line_naive(line: str):
    line = line.strip()
    if not line:
        return None

    # 先用空白切開前幾欄 (timestamp level source)
    parts = line.split()
    if len(parts) < 4:
        return {"raw": line}

    timestamp = f"{parts[0]} {parts[1]}"
    level = parts[2]
    source = parts[3]
    # 後面全部當成 message
    message = " ".join(parts[4:])

    return {
        "timestamp": timestamp,
        "level": level,
        "source": source,
        "message": message,
    }


def main():
    if not LOG_FILE.exists():
        print(f"[ERROR] log file not found: {LOG_FILE}")
        return

    print(f"[INFO] reading log file: {LOG_FILE}")
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            entry = parse_line_naive(line)
            if entry is None:
                continue
            print(entry)


if __name__ == "__main__":
    main()