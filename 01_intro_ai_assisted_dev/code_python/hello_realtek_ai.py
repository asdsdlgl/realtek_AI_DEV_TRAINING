"""
這個檔案在上課時，會由 ChatGPT/OpenWebUI 根據 hello_realtek_manual.py 改寫而來。
上課前可以先故意留白或只放註解。
"""

def greet(name: str) -> str:
    """
    產生問候訊息。

    參數
    ----
    name : str
        使用者輸入的名稱。若為空字串，預設使用 "Engineer"。

    回傳值
    ------
    str
        完整的問候語，例如 "Hello, Engineer from Realtek!"。
    """
    # 若 name 為空（例如使用者直接按下 Enter），就使用預設值
    name = name.strip() or "Engineer"
    return f"Hello, {name} from Realtek!"


def main() -> None:
    """
    主程式入口：讀取使用者輸入並印出問候訊息。
    """
    user_name = input("請輸入你的名字：")
    greeting = greet(user_name)
    print(greeting)


if __name__ == "__main__":
    main()