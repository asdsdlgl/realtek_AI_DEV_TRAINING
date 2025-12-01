from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Dict, List, Optional

LOG_FILE = Path("dataset/example_mobile_ai.log")

@dataclass
class LogEntry:
    timestamp: str
    level: str
    source: str
    fields: Dict[str, str]
    raw_message: str

def parse_line(line: str) -> Optional[LogEntry]:
    line = line.strip()
    if not line:
        return None
    
    parts = line.split()
    if len(parts) < 4:
        return None
    
    timestamp = f"{parts[0]} {parts[1]}"
    level = parts[2]
    source = parts[3]
    
    # 解析 key=value 範式
    fields: Dict[str, str] = {}
    for part in parts[4:]:
        if '=' not in part:
            continue
        key, value = part.split('=', 1)
        fields[key.strip()] = value.strip()
    
    # 剩下的部分當成 raw_message
    message_parts = [part for part in parts[4:] if '=' in part]
    raw_message = " ".join(message_parts)
    
    return LogEntry(timestamp, level, source, fields, raw_message)

def parse_file(path: Path) -> List[LogEntry]:
    log_entries = []
    if not path.exists():
        print(f"[ERROR] log file not found: {path}")
        return log_entries
    
    print(f"[INFO] reading log file: {path}")
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            entry = parse_line(line)
            if entry is not None:
                log_entries.append(entry)
    
    return log_entries

def output_as_json_lines(entries: List[LogEntry], output_path: Path):
    with output_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(asdict(entry)) + "\n")

if __name__ == "__main__":
    log_entries = parse_file(LOG_FILE)
    
    # 例子：輸出成 JSON lines
    json_output_path = Path("dataset/mobile_ai_logs.jsonl")
    output_as_json_lines(log_entries, json_output_path)