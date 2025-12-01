"""
最初版本：最簡單的 Hello Realtek Script

Day 1：學員感受「人寫最初版本 vs AI 改寫」的差異。
之後會請 ChatGPT/OpenWebUI 把這段程式改成
- 可重複使用的 function
- 加上參數與簡單錯誤處理
"""

def main():
    name = input("請輸入你的名字：")
    print(f"Hello, {name} from Realtek!")

if __name__ == "__main__":
    main()