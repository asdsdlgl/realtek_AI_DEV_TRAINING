"""
scheduled_log_alert_manual.py

最初版：
- 讀取 alert_config.yaml
- 讀取 log 檔
- 做幾個簡單的「異常條件」檢查
- 有異常就寄 email

之後會用 AI 重構成：
- 規則化的 alert engine
- 支援 schedule / 多種 alert 類型
"""

from pathlib import Path
import yaml
from statistics import median
from typing import Dict, Any

from email_utils import send_email


CONFIG_PATH = Path(__file__).parent / "alert_config.yaml"


def load_config() -> Dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_log_lines(log_file: Path):
    if not log_file.exists():
        print(f"[ERROR] log file not found: {log_file}")
        return []
    with log_file.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def analyze_log(lines):
    """非常陽春的異常偵測，只為了示範，之後會交給 AI 強化。"""
    error_count = 0
    http_5xx = 0
    gpu_oom = 0
    wifi_disconnect = 0
    asr_latencies = []

    for line in lines:
        if " ERROR " in line:
            error_count += 1
        if " NetService " in line and ("http_500" in line or "http_503" in line or "http_504" in line):
            http_5xx += 1
        if "AIInference" in line and "gpu_oom" in line:
            gpu_oom += 1
        if "NetService" in line and "wifi_disconnected" in line:
            wifi_disconnect += 1
        if "AIInference" in line and "model=asr-small-v1" in line and "latency_ms=" in line:
            # 只抓 asr-small-v1 的 latency_ms
            parts = line.split("latency_ms=")
            if len(parts) > 1:
                right = parts[1]
                num = ""
                for ch in right:
                    if ch.isdigit():
                        num += ch
                    else:
                        break
                if num:
                    asr_latencies.append(int(num))

    asr_p95 = None
    if asr_latencies:
        # 簡單估 p95：排序後取 95% 位置
        asr_latencies_sorted = sorted(asr_latencies)
        idx = max(0, int(len(asr_latencies_sorted) * 0.95) - 1)
        asr_p95 = asr_latencies_sorted[idx]

    return {
        "error_count": error_count,
        "http_5xx": http_5xx,
        "gpu_oom": gpu_oom,
        "wifi_disconnect": wifi_disconnect,
        "asr_p95": asr_p95,
        "asr_samples": len(asr_latencies),
    }


def check_abnormal(summary: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any]:
    """根據 alert_config.yaml 的門檻判斷是否異常。"""
    alerts_cfg = cfg.get("alerts", {})
    triggered = {}

    ecfg = alerts_cfg.get("error_count", {})
    if ecfg.get("enabled") and summary["error_count"] >= ecfg.get("min_errors", 1):
        triggered["error_count"] = summary["error_count"]

    hcfg = alerts_cfg.get("http_5xx", {})
    if hcfg.get("enabled") and summary["http_5xx"] >= hcfg.get("min_5xx", 1):
        triggered["http_5xx"] = summary["http_5xx"]

    gcfg = alerts_cfg.get("gpu_oom", {})
    if gcfg.get("enabled") and summary["gpu_oom"] >= gcfg.get("min_events", 1):
        triggered["gpu_oom"] = summary["gpu_oom"]

    wcfg = alerts_cfg.get("wifi_disconnect", {})
    if wcfg.get("enabled") and summary["wifi_disconnect"] >= wcfg.get("min_events", 1):
        triggered["wifi_disconnect"] = summary["wifi_disconnect"]

    acfg = alerts_cfg.get("asr_latency_p95", {})
    if acfg.get("enabled") and summary["asr_p95"] is not None:
        if summary["asr_p95"] > acfg.get("max_p95_ms", 200):
            triggered["asr_p95"] = summary["asr_p95"]

    return triggered


def build_email_body(summary: Dict[str, Any], triggered: Dict[str, Any]) -> str:
    """設定 Email 通知內容（第 5 點）。"""
    lines = []
    lines.append("瑞昱行動 AI 服務日常 log 健康檢查結果：")
    lines.append("")
    lines.append("【整體指標】")
    lines.append(f"- ERROR 行數：{summary['error_count']}")
    lines.append(f"- HTTP 5xx 次數（500/503/504）：{summary['http_5xx']}")
    lines.append(f"- GPU OOM 次數：{summary['gpu_oom']}")
    lines.append(f"- WiFi 斷線次數：{summary['wifi_disconnect']}")
    if summary["asr_p95"] is not None:
        lines.append(
            f"- asr-small-v1 延遲 P95：{summary['asr_p95']} ms（樣本數 {summary['asr_samples']}）"
        )
    else:
        lines.append("- asr-small-v1：本次無有效 latency 資料")

    lines.append("")
    if triggered:
        lines.append("【觸發告警的條件】")
        for k, v in triggered.items():
            lines.append(f"- {k}: {v}")
    else:
        lines.append("【目前未觸發任何告警條件】")

    lines.append("")
    lines.append("建議後續處理：")
    lines.append("- 請登入監控平台確認是否有對應的 spike 或異常 pattern")
    lines.append("- 若 GPU OOM / 5xx 過多，可考慮暫時降載或擴充資源")
    lines.append("- 如需調整門檻，請修改 alert_config.yaml 後重新部署")

    return "\n".join(lines)


def main():
    cfg = load_config()
    log_path = Path(cfg["log"]["file"])
    lines = load_log_lines(log_path)
    if not lines:
        return

    summary = analyze_log(lines)
    print("[INFO] summary:", summary)
    triggered = check_abnormal(summary, cfg)

    if not triggered:
        print("[INFO] no abnormal conditions triggered, no email sent.")
        return

    email_cfg = cfg["email"]
    subject = "[Log Alert] 瑞昱行動 AI 服務異常告警"
    body = build_email_body(summary, triggered)

    send_email(
        smtp_host=email_cfg["smtp_host"],
        smtp_port=email_cfg["smtp_port"],
        sender_email=email_cfg["sender"],
        sender_password_env=email_cfg["sender_password_env"],
        recipients=email_cfg["recipients"],
        subject=subject,
        body=body,
    )


if __name__ == "__main__":
    main()