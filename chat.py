import re
from agent import AutomationAgent


class ChatAgent:
    def __init__(self):
        self.agent = AutomationAgent()
        self.running = True

    def parse_command(self, user_input):
        text = user_input.lower().strip()

        if text in ["خروج", "exit", "quit", "قفل", "agmaa"]:
            self.running = False
            return "مع السلامة!"

        if text in ["help", "مساعدة", "لو عايز تعرف الاوامر", "اوامر"]:
            return self.get_help()

        if any(w in text for w in ["سكرين شوت", "screenshot", "صورة الشاشة", "shat"]):
            return self.agent.screenshot()

        if any(w in text for w in ["موقع الماوس", "mouse position", "وين الماوس", "فين الماوس"]):
            return self.agent.get_mouse_position()

        if any(w in text for w in ["حجم الشاشة", "screen size", "size"]):
            return self.agent.get_screen_size()

        if any(w in text for w in ["الكليبورد", "clipboard", "copied"]):
            return self.agent.get_clipboard()

        pos_match = re.search(r"(?:اضغط|click|ضغط|دوس)\s*(?:على\s*)?\(?(\d+)\s*[,،]\s*(\d+)\)?", text)
        if pos_match:
            x, y = int(pos_match.group(1)), int(pos_match.group(2))
            return self.agent.click(x, y)

        if any(w in text for w in ["اضغط", "click", "دوس", "ضغط"]):
            return self.agent.click()

        dbl_match = re.search(r"(?:اضغط مرتين|double click|دوس مرتين)\s*(?:على\s*)?\(?(\d+)\s*[,،]\s*(\d+)\)?", text)
        if dbl_match:
            x, y = int(dbl_match.group(1)), int(dbl_match.group(2))
            return self.agent.double_click(x, y)

        if any(w in text for w in ["اضغط مرتين", "double click", "دوس مرتين"]):
            return self.agent.double_click()

        right_match = re.search(r"(?:كليك يمين|right click|يمين)\s*(?:على\s*)?\(?(\d+)\s*[,،]\s*(\d+)\)?", text)
        if right_match:
            x, y = int(right_match.group(1)), int(right_match.group(2))
            return self.agent.right_click(x, y)

        if any(w in text for w in ["كليك يمين", "right click", "يمين"]):
            return self.agent.right_click()

        if any(w in text for w in ["فتح", "open", "شغل", "run", "ابدأ", "start"]):
            app = self.extract_app_name(text)
            if app:
                return self.agent.open_app(app)
            return "اكتب اسم التطبيق اللي عايز تفتحه"

        if any(w in text for w in ["رابط", "url", "link", "موقع", "site", "page", "صفحة"]):
            url = self.extract_url(text)
            if url:
                return self.agent.open_url(url)
            return "اكتب الرابط اللي عايز تفتحه"

        if any(w in text for w in ["اغلق", "close", "قفل", "اوقف"]):
            return self.agent.close_window()

        if any(w in text for w in ["صغّر", "minimize", "تصغير", "unmaximize"]):
            return self.agent.minimize_window()

        if any(w in text for w in ["كبّر", "maximize", "تكبير", "maximum"]):
            return self.agent.maximize_window()

        if any(w in text for w in ["تبديل", "switch", "window", "نافذة"]):
            return self.agent.switch_window()

        if any(w in text for w in ["اكتب", "type", "كاتب", "write", "send", "ابعت"]):
            text_to_type = self.extract_text(text)
            if text_to_type:
                return self.agent.type_arabic(text_to_type)
            return "اكتب النص اللي عايز تكتبه"

        if any(w in text for w in ["kopieer", "انسخ", "copy", "نسخ"]):
            text_to_copy = self.extract_text(text)
            if text_to_copy:
                return self.agent.set_clipboard(text_to_copy)
            return "اكتب النص اللي عايز تنسخه"

        if any(w in text for w in ["لصق", "paste", "粘贴"]):
            return self.agent.paste_from_clipboard()

        if any(w in text for w in ["scroll", "تمرير", "اسكرول"]):
            amount = -5
            num_match = re.search(r"(-?\d+)", text)
            if num_match:
                amount = int(num_match.group(1))
            return self.agent.scroll(amount)

        if any(w in text for w in ["انتظر", "wait", "استنى", "ثانية", "second"]):
            seconds = 1
            num_match = re.search(r"(\d+)", text)
            if num_match:
                seconds = int(num_match.group(1))
            return self.agent.wait(seconds)

        if any(w in text for w in [" أمر", " command", "shell", "terminal", "terminal"]):
            cmd = self.extract_command(text)
            if cmd:
                return self.agent.execute_command(cmd)
            return "اكتب الأمر اللي عايز تنفيذه"

        if any(w in text for w in ["mov", "حرك", "ارسم", "روح", "go to"]):
            match = re.search(r"(\d+)\s*[,،]\s*(\d+)", text)
            if match:
                x, y = int(match.group(1)), int(match.group(2))
                return self.agent.move_mouse(x, y)
            return "اكتب الإحداثيات (x, y)"

        if any(w in text for w in ["hotkey", "keyboard shortcut", "option", "اختصار"]):
            keys = self.extract_keys(text)
            if keys:
                return self.agent.hotkey(*keys)
            return "اكتب الاختصار (مثلا ctrl+c)"

        return self.smart_response(text)

    def extract_app_name(self, text):
        apps = {
            "متصفح": "chrome",
            "جوجل": "chrome",
            "chrome": "chrome",
            "فايرفوكس": "firefox",
            "firefox": "firefox",
            "ترمinal": "gnome-terminal",
            "terminal": "gnome-terminal",
            "VERNOMAL": "gnome-terminal",
            "نوت باد": "gedit",
            "notepad": "gedit",
            "محرر": "gedit",
            "المجلد": "nautilus",
            "files": "nautilus",
            "الحاسبة": "gnome-calculator",
            "calculator": "gnome-calculator",
            "الإعدادات": "gnome-control-center",
            "settings": "gnome-control-center",
            "vscode": "code",
            "كود": "code",
            "code": "code",
        }
        for key, value in apps.items():
            if key in text:
                return value
        words = text.split()
        for w in words:
            if w not in ["افتح", "open", "شغل", "run", "ابدأ", "start", "التطبيق", "the", "app"]:
                return w
        return None

    def extract_url(self, text):
        url_match = re.search(r"(https?://\S+|www\.\S+)", text)
        if url_match:
            return url_match.group(1)
        words = text.split()
        for i, w in enumerate(words):
            if "." in w and len(w) > 3:
                return w
        return None

    def extract_text(self, text):
        patterns = [
            r'(?:اكتب|type|كاتب|write|send|ابعت|انسخ|copy|نسخ)\s*[:\s]*(.+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def extract_command(self, text):
        match = re.search(r'(?:command|امر|shell|terminal)\s*[:\s]*(.+)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def extract_keys(self, text):
        match = re.search(r'(?:hotkey|اختصار|option)\s*[:\s]*(.+)', text, re.IGNORECASE)
        if match:
            keys_str = match.group(1).strip()
            keys = [k.strip() for k in re.split(r'\+|و|\s*,\s*', keys_str)]
            return keys
        return None

    def smart_response(self, text):
        if any(w in text for w in ["ازيك", "عامل ايه", "hi", "hello", "اهلا", "مرحبا"]):
            return "أهلاً وسهلاً! أنا بوت الأوتوميشن، اكتبلي عايز تعمل ايه"

        if any(w in text for w in ["مين انت", "who are you", "تعريف", "introduce"]):
            return "أنا بوت أوتوميشن بيتحكم في جهازك! اكتبلي عايز تعمل ايه وساعديك"

        if "?" in text or "؟" in text:
            return "لو عايز تعرف الاوامر اكتب 'مساعدة' أو 'help'"

        return "مش فاهم الأمر، اكتب 'مساعدة' عشان تعرف الاوامر المتاحة"

    def get_help(self):
        help_text = """
╔══════════════════════════════════════════════════════╗
║           🤖 بوت الأوتوميشن - قائمة المساعدة         ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🖱️  التحكم بالماوس:                                 ║
║  • اضغط / click - ضغط على الموقع الحالي              ║
║  • اضغط (100, 200) / click 100,200 - ضغط على نقطة   ║
║  • اضغط مرتين / double click - ضغط مزدوج            ║
║  • كليك يمين / right click - ضغط بالزرار اليمين      ║
║  • حرك (100, 200) - تحريك الماوس                    ║
║  • سحب (0,0) إلى (100,100) - سحب من وإلى          ║
║                                                      ║
║  ⌨️  الكتابة والكيبورد:                               ║
║  • اكتب [نص] / type [text] - كتابة نص بالإنجليزي    ║
║  • اكتب [نص عربي] - كتابة نص بالعربي                ║
║  • اختصار ctrl+c / hotkey ctrl+c - اختصار لوحة مفاتيح║
║  • scroll 5 / تمرير 5 - تمرير                       ║
║                                                      ║
║  📱 التطبيقات والنوافذ:                               ║
║  • افتح [اسم التطبيق] / open [app]                  ║
║  • افتح رابط [url] - فتح رابط                       ║
║  • اغلق / close - إغلاق النافذة                     ║
║  • كبّر / maximize - تكبير النافذة                   ║
║  • صغّر / minimize - تصغير النافذة                   ║
║  • تبديل / switch - تبديل النافذة                    ║
║                                                      ║
║  📸 مساعدة:                                          ║
║  • سكرين شوت / screenshot - أخذ صورة للشاشة         ║
║  • موقع الماوس / mouse position - معرفة الموقع      ║
║  • حجم الشاشة / screen size - معرفة الحجم           ║
║  • انسخ [نص] / copy [text] - نسخ نص                 ║
║  • لصق / paste - لصق من الكليبورد                   ║
║                                                      ║
║  ⚙️  أوامر متقدمة:                                   ║
║  • command [أمر] - تنفيذ أمر في الترمينال             ║
║  • انتظر [ثانية] / wait [s] - انتظار                ║
║  • مساعدة / help - عرض هذه القائمة                  ║
║  • خروج / exit - إغلاق البوت                        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""
        return help_text
