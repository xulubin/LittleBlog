import time
import os
import shutil
import hashlib
import traceback
import win32clipboard
import win32con
import win32gui
import win32console
from datetime import datetime

# 配置参数
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download')
CHECK_INTERVAL = 5  # 检测间隔（秒）

# 隐藏控制台窗口
def hide_console():
    try:
        window = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(window, win32con.SW_HIDE)
    except Exception as e:
        print(f"隐藏控制台失败: {e}")


# 创建备份目录
os.makedirs(BACKUP_DIR, exist_ok=True)

# 日志记录函数
def log_error(message):
    with open('error.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()}: {message}\n")

# 获取剪贴板中的文件路径
def get_clipboard_files():
    for _ in range(3):  # 重试3次
        try:
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
                    return set(win32clipboard.GetClipboardData(win32clipboard.CF_HDROP))
            finally:
                win32clipboard.CloseClipboard()
            break  # 成功获取剪贴板内容，跳出循环
        except Exception as e:
            time.sleep(0.1)  # 短暂等待后重试
    else:
        log_error(f"剪贴板访问错误: {e}\n{traceback.format_exc()}")
    return set()

# 生成唯一文件名
def generate_filename(original_path):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ext = os.path.splitext(original_path)[1]
    counter = 1
    while True:
        new_name = f"{timestamp}-{counter}{ext}"
        new_path = os.path.join(BACKUP_DIR, new_name)
        if not os.path.exists(new_path):
            return new_path
        counter += 1

# 分块计算文件哈希
def get_file_hash(file_path, chunk_size=1024*1024):
    try:
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception:
        return None

# 备份文件
def backup_file(file_path, backed_up_hashes):
    try:
        if not os.path.isfile(file_path):
            return False

        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            return False

        file_hash = get_file_hash(file_path)
        if file_hash in backed_up_hashes:
            return False

        dest_path = generate_filename(file_path)
        shutil.copy2(file_path, dest_path)
        backed_up_hashes.add(file_hash)
        return True
    except Exception as e:
        log_error(f"备份文件 {file_path} 失败: {e}")
        return False

# 主监控循环
def monitor_clipboard():
    last_files = set()
    backed_up_hashes = set()

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            files = get_clipboard_files()

            # 检查是否有新增文件
            for file_path in files - last_files:
                backup_file(file_path, backed_up_hashes)

            last_files = files
    except Exception as e:
        log_error(f"监控错误: {e}")

if __name__ == "__main__":
    hide_console()
    monitor_clipboard()