"""
email_utils.py

寄信工具函式：
- 不寫死帳號/密碼在程式裡
- 從呼叫端傳入 subject / body
- 適合拿來做「log 告警通知」用途
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List


def send_email(
    smtp_host: str,
    smtp_port: int,
    sender_email: str,
    sender_password_env: str,
    recipients: List[str],
    subject: str,
    body: str,
) -> None:
    """寄送純文字 email。

    :param smtp_host: SMTP 主機，例如 smtp.gmail.com
    :param smtp_port: SMTP Port，例如 587
    :param sender_email: 寄件者 email
    :param sender_password_env: 儲存 App Password 的環境變數名稱
    :param recipients: 收件者 email list
    :param subject: 郵件標題
    :param body: 郵件內文（純文字）
    """
    password = os.environ.get(sender_password_env)
    if not password:
        print(f"[ERROR] env var {sender_password_env} not set, cannot send email.")
        return

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, recipients, msg.as_string())
        print("[INFO] Email sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")