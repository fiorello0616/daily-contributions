import os
import datetime
import random
import subprocess

# 這個腳本會在你的 GitHub Actions 環境中運行
# 所以我們讓它在當前目錄操作，而不是指定一個固定路徑
# REPO_PATH 設置為 "." 表示當前目錄
REPO_PATH = "." 

FILE_TO_MODIFY = "contribute_log.txt"

COMMIT_MESSAGES = [
    "自動提交：更新貢獻日誌",
    "每日例行公事：保持活躍",
    "讓 GitHub 貢獻保持綠色",
    "添加一些新的數據點",
    "今天的進度更新",
    "修復一些小問題"
]

def run_command(command, cwd=None):
    """執行 shell 命令並檢查是否成功"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            shell=True,
            text=True,
            capture_output=True
        )
        print(f"命令執行成功: {command}")
        if result.stdout:
            print("標準輸出:\n", result.stdout)
        if result.stderr:
            print("標準錯誤:\n", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令執行失敗: {command}")
        print(f"錯誤碼: {e.returncode}")
        print(f"標準輸出:\n", e.stdout)
        print(f"標準錯誤:\n", e.stderr)
        return False
    except Exception as e:
        print(f"執行命令時發生意外錯誤: {e}")
        return False

def daily_github_contributor():
    """執行每日 GitHub 貢獻流程"""
    # 確保在正確的目錄執行
    original_cwd = os.getcwd()
    os.chdir(REPO_PATH) 
    print(f"正在處理倉庫: {os.getcwd()}")

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"提交時間: {timestamp} - 隨機數: {random.randint(1, 1000)}\n"

    file_path = os.path.join(os.getcwd(), FILE_TO_MODIFY)
    try:
        with open(file_path, "a") as f:
            f.write(log_content)
        print(f"已將內容追加到文件: {FILE_TO_MODIFY}")
    except IOError as e:
        print(f"錯誤: 無法寫入文件 {FILE_TO_MODIFY}: {e}")
        os.chdir(original_cwd) # 返回原始目錄
        return

    # Git add
    if not run_command(["git", "add", FILE_TO_MODIFY], cwd=os.getcwd()):
        print("Git add 命令失敗，終止。")
        os.chdir(original_cwd)
        return

    # Git commit
    commit_message = random.choice(COMMIT_MESSAGES)
    if not run_command(["git", "commit", "-m", commit_message], cwd=os.getcwd()):
        print("Git commit 命令失敗，終止。")
        os.chdir(original_cwd)
        return

    # Git push
    # 注意: 在 GitHub Actions 中，origin/main 是預設且通常正確的
    if not run_command(["git", "push", "origin", "main"], cwd=os.getcwd()):
        print("Git push 命令失敗。請檢查 GitHub Actions 的日誌。")
        os.chdir(original_cwd)
        return

    print("腳本執行完畢。請檢查你的 GitHub 貢獻圖。")
    os.chdir(original_cwd) # 返回原始目錄

if _name_ == "_main_":
    daily_github_contributor()
