import customtkinter as ctk
from chat import ChatAgent
import threading
import time
from datetime import datetime


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AutomationDesktop:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 بوت الأوتوميشن")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.chat = ChatAgent()
        self.message_count = 0

        self.setup_ui()

    def setup_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0, fg_color="#1a1a2e")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        logo_label = ctk.CTkLabel(
            sidebar,
            text="🤖 الأوتوميشن",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#00d4ff",
        )
        logo_label.pack(pady=25, padx=10)

        buttons = [
            ("🖱️  اضغط", lambda: self.send_command("اضغط")),
            ("🖱️  اضغط مرتين", lambda: self.send_command("اضغط مرتين")),
            ("🖱️  كليك يمين", lambda: self.send_command("كليك يمين")),
            ("⌨️  اكتب نص", self.open_type_dialog),
            ("📱  افتح تطبيق", self.open_app_dialog),
            ("📸  سكرين شوت", lambda: self.send_command("سكرين شوت")),
            ("🔲  اغلق نافذة", lambda: self.send_command("اغلق")),
            ("🔼  كبّر نافذة", lambda: self.send_command("كبّر")),
            ("🔽  صغّر نافذة", lambda: self.send_command("صغّر")),
            ("🔄  تبديل نافذة", lambda: self.send_command("تبديل")),
            ("📍  موقع الماوس", lambda: self.send_command("موقع الماوس")),
            ("📐  حجم الشاشة", lambda: self.send_command("حجم الشاشة")),
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                height=38,
                corner_radius=8,
                font=ctk.CTkFont(size=13),
                fg_color="#16213e",
                hover_color="#0f3460",
                anchor="e",
            )
            btn.pack(pady=3, padx=10, fill="x")

        exit_btn = ctk.CTkButton(
            sidebar,
            text="❌  خروج",
            command=self.root.destroy,
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            fg_color="#e94560",
            hover_color="#c81e45",
        )
        exit_btn.pack(pady=15, padx=10, fill="x", side="bottom")

    def create_main_area(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="#0f0f23", corner_radius=0)
        main_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(main_frame, height=60, fg_color="#16213e", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="💬 شات الأوامر",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00d4ff",
        )
        title.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.status_label = ctk.CTkLabel(
            header,
            text="● جاهز",
            font=ctk.CTkFont(size=12),
            text_color="#00ff88",
        )
        self.status_label.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        self.chat_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color="#0a0a1a",
            scrollbar_fg_color="#1a1a2e",
            scrollbar_button_color="#0f3460",
            scrollbar_button_hover_color="#00d4ff",
        )
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.add_system_message("أهلاً وسهلاً! 👋\nأنا بوت الأوتوميشن، اكتبلي عايز تعمل ايه\nاكتب 'مساعدة' عشان تعرف كل الأوامر المتاحة")

        input_frame = ctk.CTkFrame(main_frame, height=70, fg_color="#16213e", corner_radius=0)
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="اكتب الأمر هنا... (مثال: افتح chrome)",
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=10,
            fg_color="#0a0a1a",
            border_color="#0f3460",
            text_color="#ffffff",
        )
        self.input_entry.grid(row=0, column=0, padx=15, pady=12, sticky="ew")
        self.input_entry.bind("<Return>", lambda event: self.send_input())

        send_btn = ctk.CTkButton(
            input_frame,
            text="إرسال ➤",
            command=self.send_input,
            width=100,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0f3460",
            hover_color="#00d4ff",
        )
        send_btn.grid(row=0, column=1, padx=(0, 15), pady=12)

    def add_message(self, text, is_user=False):
        self.message_count += 1

        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color="#1a1a2e" if is_user else "#16213e",
            corner_radius=12,
        )
        msg_frame.grid(row=self.message_count, column=0, pady=5, padx=10, sticky="ew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        if is_user:
            label = ctk.CTkLabel(
                msg_frame,
                text=f"🧑 أنت:\n{text}",
                font=ctk.CTkFont(size=13),
                text_color="#ffffff",
                justify="right",
                wraplength=500,
            )
            label.pack(padx=15, pady=10, anchor="e")
        else:
            label = ctk.CTkLabel(
                msg_frame,
                text=f"🤖 البوت:\n{text}",
                font=ctk.CTkFont(size=13),
                text_color="#00d4ff",
                justify="left",
                wraplength=500,
            )
            label.pack(padx=15, pady=10, anchor="w")

        self.chat_frame._parent_canvas.after(
            100,
            lambda: self.chat_frame._parent_canvas.yview_moveto(1.0),
        )

    def add_system_message(self, text):
        self.message_count += 1

        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color="#0f3460",
            corner_radius=12,
        )
        msg_frame.grid(row=self.message_count, column=0, pady=5, padx=30, sticky="ew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            msg_frame,
            text=text,
            font=ctk.CTkFont(size=13),
            text_color="#00ff88",
            justify="center",
            wraplength=500,
        )
        label.pack(padx=15, pady=10)

    def send_input(self):
        text = self.input_entry.get().strip()
        if text:
            self.input_entry.delete(0, "end")
            self.process_command(text)

    def send_command(self, command):
        self.process_command(command)

    def process_command(self, command):
        self.add_message(command, is_user=True)
        self.status_label.configure(text="● جاري التنفيذ...", text_color="#ffaa00")

        def run():
            try:
                response = self.chat.parse_command(command)
                self.root.after(0, lambda: self.add_message(response, is_user=False))
                self.root.after(0, lambda: self.status_label.configure(
                    text="● جاهز", text_color="#00ff88"
                ))
            except Exception as e:
                self.root.after(0, lambda: self.add_message(f"❌ خطأ: {str(e)}", is_user=False))
                self.root.after(0, lambda: self.status_label.configure(
                    text="● خطأ", text_color="#ff4444"
                ))

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def open_type_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("اكتب نص")
        dialog.geometry("400x200")
        dialog.configure(fg_color="#0f0f23")
        dialog.transient(self.root)
        dialog.grab_set()

        label = ctk.CTkLabel(
            dialog,
            text="اكتب النص اللي عايز تكتبه:",
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
        )
        label.pack(pady=(20, 10))

        entry = ctk.CTkEntry(
            dialog,
            placeholder_text="النص هنا...",
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#1a1a2e",
            border_color="#0f3460",
        )
        entry.pack(pady=10, padx=20, fill="x")
        entry.focus()

        def submit():
            text = entry.get().strip()
            if text:
                dialog.destroy()
                self.process_command(f"اكتب {text}")

        btn = ctk.CTkButton(
            dialog,
            text="كتابة ✓",
            command=submit,
            height=40,
            fg_color="#0f3460",
            hover_color="#00d4ff",
        )
        btn.pack(pady=15)
        entry.bind("<Return>", lambda e: submit())

    def open_app_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("فتح تطبيق")
        dialog.geometry("400x250")
        dialog.configure(fg_color="#0f0f23")
        dialog.transient(self.root)
        dialog.grab_set()

        label = ctk.CTkLabel(
            dialog,
            text="اكتب اسم التطبيق:",
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
        )
        label.pack(pady=(20, 10))

        entry = ctk.CTkEntry(
            dialog,
            placeholder_text="chrome, firefox, vscode...",
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#1a1a2e",
            border_color="#0f3460",
        )
        entry.pack(pady=10, padx=20, fill="x")
        entry.focus()

        apps_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        apps_frame.pack(pady=5)

        for app in ["chrome", "firefox", "vscode", "terminal", "files"]:
            btn = ctk.CTkButton(
                apps_frame,
                text=app,
                command=lambda a=app: (dialog.destroy(), self.process_command(f"افتح {a}")),
                width=70,
                height=30,
                font=ctk.CTkFont(size=11),
                fg_color="#16213e",
                hover_color="#0f3460",
            )
            btn.pack(side="left", padx=3)

        def submit():
            text = entry.get().strip()
            if text:
                dialog.destroy()
                self.process_command(f"افتح {text}")

        btn = ctk.CTkButton(
            dialog,
            text="فتح ✓",
            command=submit,
            height=40,
            fg_color="#0f3460",
            hover_color="#00d4ff",
        )
        btn.pack(pady=10)
        entry.bind("<Return>", lambda e: submit())

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AutomationDesktop()
    app.run()
