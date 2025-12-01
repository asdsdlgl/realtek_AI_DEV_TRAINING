# 瑞昱 AI 助理編寫與優化 Python/Perl/Linux Script（實作）

本專案搭配 VSCode、ChatGPT / OpenWebUI 使用，作為 12 小時內訓課程的實作範例專案。

## 環境需求

- VSCode
- Python 3.10+
- Perl
- Bash / Linux Shell 環境（或 WSL）
- （選用）ChatGPT 或自建 OpenWebUI（gpt-oss:20b）

## 專案結構

- `01_intro_ai_assisted_dev/`  
  AI 輔助開發概論與語法差異、第一個 AI 生成範例程式。

- `02_script_automation/`  
  批次檔案處理、SMTP 寄信、自動化腳本。

- `03_optimization_debug/`  
  Debug、效能分析與重構（Refactoring）。

- `04_maintenance_git/`  
  Git 版本管理、AI 協助寫 commit message 與維護文件。

- `datasets/`：log / csv / 測試資料  
- `solutions/`：課後參考解答（AI 優化後版本）  
- `prompts_global/`：通用 Prompt 模板  
- `slides/`：課程簡報

## 如何使用

1. 在 VSCode 打開此資料夾。
2. 安裝建議的 Extensions（VSCode 會自動跳出）。
3. 依照老師指示，從 `01_intro_ai_assisted_dev/` 開始實作。
4. 在每個模組底下，`code_*` 資料夾放「最初版本」，`solutions/` 放「AI 優化後」結果。
5. `prompts/` 或 `prompts_global/` 中提供可直接複製貼上的範例提示詞。