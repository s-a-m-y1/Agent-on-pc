import pyautogui
import subprocess
import os
import time
import json
from datetime import datetime
from PIL import Image

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


class AutomationAgent:
    def __init__(self):
        self.screenshot_dir = os.path.join(os.path.expanduser("~"), "Agent_Screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def click(self, x=None, y=None, button="left", clicks=1):
        if x is not None and y is not None:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
            return f"تم الضغط على النقطة ({x}, {y})"
        else:
            pyautogui.click(button=button, clicks=clicks)
            pos = pyautogui.position()
            return f"تم الضغط على الموقع الحالي ({pos.x}, {pos.y})"

    def double_click(self, x=None, y=None):
        if x is not None and y is not None:
            pyautogui.doubleClick(x=x, y=y)
            return f"تم الضغط المزدوج على ({x}, {y})"
        else:
            pyautogui.doubleClick()
            pos = pyautogui.position()
            return f"تم الضغط المزدوج على الموقع الحالي ({pos.x}, {pos.y})"

    def right_click(self, x=None, y=None):
        if x is not None and y is not None:
            pyautogui.rightClick(x=x, y=y)
            return f"تم الضغط بالزرار اليمين على ({x}, {y})"
        else:
            pyautogui.rightClick()
            pos = pyautogui.position()
            return f"تم الضغط بالزرار اليمين على الموقع الحالي ({pos.x}, {pos.y})"

    def type_text(self, text, interval=0.05):
        pyautogui.typewrite(text, interval=interval)
        return f"تم الكتابة: {text}"

    def type_arabic(self, text):
        import pyperclip
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        return f"تم الكتابة بالعربي: {text}"

    def press_key(self, key):
        pyautogui.press(key)
        return f"تم الضغط على زرار: {key}"

    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        return f"تم الضغط على: {' + '.join(keys)}"

    def scroll(self, amount):
        pyautogui.scroll(amount)
        return f"تم التمرير {amount} مرات"

    def move_mouse(self, x, y, duration=0.5):
        pyautogui.moveTo(x, y, duration=duration)
        return f"تم تحريك الماوس إلى ({x}, {y})"

    def drag(self, x1, y1, x2, y2, duration=0.5):
        pyautogui.moveTo(x1, y1)
        pyautogui.drag(x2 - x1, y2 - y1, duration=duration)
        return f"تم السحب من ({x1}, {y1}) إلى ({x2}, {y2})"

    def screenshot(self, name=None):
        if name is None:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.screenshot_dir, name)
        img = pyautogui.screenshot()
        img.save(filepath)
        return f"تم أخذ سكرين شوت: {filepath}"

    def open_app(self, app_name):
        linux_apps = {
            "chrome": "google-chrome",
            "firefox": "firefox",
            "terminal": "gnome-terminal",
            "notepad": "gedit",
            "files": "nautilus",
            "calculator": "gnome-calculator",
            "settings": "gnome-control-center",
            "vscode": "code",
            "code": "code",
        }
        app_cmd = linux_apps.get(app_name.lower(), app_name)
        try:
            subprocess.Popen([app_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"تم فتح التطبيق: {app_name}"
        except FileNotFoundError:
            try:
                subprocess.Popen(
                    ["nohup", app_cmd, "&"],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return f"تم محاولة فتح التطبيق: {app_name}"
            except Exception as e:
                return f"مش قادر أفتح التطبيق {app_name}: {str(e)}"

    def open_url(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"تم فتح الرابط: {url}"

    def close_window(self):
        pyautogui.hotkey("alt", "f4")
        return "تم إغلاق النافذة الحالية"

    def minimize_window(self):
        pyautogui.hotkey("alt", "space")
        time.sleep(0.1)
        pyautogui.press("n")
        return "تم تصغير النافذة"

    def maximize_window(self):
        pyautogui.hotkey("alt", "space")
        time.sleep(0.1)
        pyautogui.press("x")
        return "تم تكبير النافذة"

    def switch_window(self):
        pyautogui.hotkey("alt", "tab")
        return "تم التبديل للنافذة التالية"

    def get_mouse_position(self):
        pos = pyautogui.position()
        return f"موقع الماوس الحالي: ({pos.x}, {pos.y})"

    def get_screen_size(self):
        size = pyautogui.size()
        return f"حجم الشاشة: {size.width}x{size.height}"

    def wait(self, seconds):
        time.sleep(seconds)
        return f"تم الانتظار {seconds} ثانية"

    def get_clipboard(self):
        import pyperclip
        text = pyperclip.paste()
        return f"المحتوى في الكليبورد: {text}"

    def set_clipboard(self, text):
        import pyperclip
        pyperclip.copy(text)
        return f"تم نسخ النص في الكليبورد: {text}"

    def paste_from_clipboard(self):
        pyautogui.hotkey("ctrl", "v")
        return "تم لصق المحتوى من الكليبورد"

    def execute_command(self, command):
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout if result.stdout else result.stderr
            return f"نتيجة الأمر:\n{output}"
        except subprocess.TimeoutExpired:
            return "الأمر أخد وقت أكتر من 30 ثانية"
        except Exception as e:
            return f"خطأ في تنفيذ الأمر: {str(e)}"

    def get_active_window(self):
        try:
            import subprocess
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                capture_output=True,
                text=True,
            )
            return f"النافذة الحالية: {result.stdout.strip()}"
        except Exception:
            return "مش قادر أعرف النافذة الحالية"
