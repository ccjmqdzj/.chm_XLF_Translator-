import tkinter as tk
from tkinter import filedialog, messagebox
from pygtrans import Translate
from docts import Docts
import os
import platform


if platform.system() == 'Windows':
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


if platform.system() == 'Windows':
    FONT_FAMILY = ('Segoe UI', 'Microsoft YaHei UI', '微软雅黑', 'Arial', 'sans-serif')
elif platform.system() == 'Darwin':
    FONT_FAMILY = ('PingFang SC', 'Arial', 'sans-serif')
else:
    FONT_FAMILY = ('Arial', 'sans-serif')

class XLFTranslatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("XLF 自动翻译工具")
        master.geometry("540x390")
        master.resizable(True, True)

        
        self.themes = {
            'light': {
                'bg': '#f9f9fb', 'fg': '#222', 'entry_bg': '#f4f6fa', 'entry_fg': '#222',
                'btn_bg': '#4f8cff', 'btn_fg': '#fff', 'btn_hover': '#357ae8',
                'border': '#e0e0e0', 'hint_fg': '#888', 'frame': '#e0e0e0',
                'icon_bg': '#f9f9fb', 'icon_fg': '#222', 'icon_hover': '#e0e0e0',
            },
            'dark': {
                'bg': '#23272e', 'fg': '#f5f6fa', 'entry_bg': '#2d313a', 'entry_fg': '#f5f6fa',
                'btn_bg': '#3b82f6', 'btn_fg': '#fff', 'btn_hover': '#2563eb',
                'border': '#444950', 'hint_fg': '#aaa', 'frame': '#444950',
                'icon_bg': '#23272e', 'icon_fg': '#f5f6fa', 'icon_hover': '#444950',
            }
        }
        self.theme_cycle = ['system', 'light', 'dark']
        self.theme_mode = 'system'
        self._apply_theme(self._get_system_theme())

        
        self.theme_icon_btn = tk.Label(master, cursor="hand2", bg=self.icon_bg)
        self.theme_icon_btn.place(relx=1.0, x=-36, y=18, anchor="ne")
        self.theme_icon_btn.bind('<Button-1>', self._on_theme_icon_click)
        self.theme_icon_btn.bind('<Enter>', lambda e: self.theme_icon_btn.config(bg=self.icon_hover))
        self.theme_icon_btn.bind('<Leave>', lambda e: self.theme_icon_btn.config(bg=self.icon_bg))
        self._update_theme_icon()

        font_title = (FONT_FAMILY, 22, "bold")
        font_label = (FONT_FAMILY, 13, "bold")
        font_entry = (FONT_FAMILY, 13)
        font_btn = (FONT_FAMILY, 14, "bold")
        font_hint = (FONT_FAMILY, 11)
        font_icon = (FONT_FAMILY, 20, "bold")

        
        self.title_label = tk.Label(master, text="XLF 自动翻译工具", font=font_title, bg=self.bg, fg=self.fg)
        self.title_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=36, pady=(12, 10))
        
        self.sep = tk.Frame(master, bg=self.frame, height=1, width=420)
        self.sep.grid(row=2, column=0, columnspan=3, padx=36, pady=(0, 14), sticky="we")

        
        self.input_label = tk.Label(master, text="选择 XLF 文件", font=font_label, bg=self.bg, fg=self.fg)
        self.input_label.grid(row=3, column=0, sticky="w", padx=36, pady=7)
        self.input_entry = tk.Entry(master, width=32, font=font_entry, relief=tk.FLAT, bg=self.entry_bg, fg=self.entry_fg, highlightthickness=1, highlightbackground=self.border, highlightcolor=self.btn_bg)
        self.input_entry.grid(row=3, column=1, sticky="we", pady=7)
        self.browse_btn = tk.Button(master, text="浏览", font=font_btn, bg=self.btn_bg, fg=self.btn_fg, bd=0, command=self.browse_input, cursor="hand2", width=7, height=1, activebackground=self.btn_hover, activeforeground=self.btn_fg)
        self.browse_btn.grid(row=3, column=2, sticky="w", padx=(8,0), pady=7)
        self._add_hover(self.browse_btn, self.btn_bg, self.btn_hover)

        
        self.filter_label = tk.Label(master, text="过滤关键词", font=font_label, bg=self.bg, fg=self.fg)
        self.filter_label.grid(row=4, column=0, sticky="w", padx=36, pady=7)
        self.filter_entry = tk.Entry(master, width=32, font=font_entry, relief=tk.FLAT, bg=self.entry_bg, fg=self.entry_fg, highlightthickness=1, highlightbackground=self.border, highlightcolor=self.btn_bg)
        self.filter_entry.grid(row=4, column=1, columnspan=2, sticky="we", pady=7)
        self.filter_hint = tk.Label(master, text="用英文逗号分隔，如 TODO,不翻译", font=font_hint, fg=self.hint_fg, bg=self.bg)
        self.filter_hint.grid(row=5, column=1, columnspan=2, sticky="w", padx=(0,0))

        
        self.type_label = tk.Label(master, text="过滤类型", font=font_label, bg=self.bg, fg=self.fg)
        self.type_label.grid(row=6, column=0, sticky="w", padx=36, pady=7)
        self.type_entry = tk.Entry(master, width=32, font=font_entry, relief=tk.FLAT, bg=self.entry_bg, fg=self.entry_fg, highlightthickness=1, highlightbackground=self.border, highlightcolor=self.btn_bg)
        self.type_entry.grid(row=6, column=1, columnspan=2, sticky="we", pady=7)
        self.type_hint = tk.Label(master, text="如 code,page:3，英文逗号分隔，可选", font=font_hint, fg=self.hint_fg, bg=self.bg)
        self.type_hint.grid(row=7, column=1, columnspan=2, sticky="w", padx=(0,0))

        
        self.proxy_label = tk.Label(master, text="代理", font=font_label, bg=self.bg, fg=self.fg)
        self.proxy_label.grid(row=8, column=0, sticky="w", padx=36, pady=7)
        self.proxy_entry = tk.Entry(master, width=32, font=font_entry, relief=tk.FLAT, bg=self.entry_bg, fg=self.entry_fg, highlightthickness=1, highlightbackground=self.border, highlightcolor=self.btn_bg)
        self.proxy_entry.grid(row=8, column=1, columnspan=2, sticky="we", pady=7)
        self.proxy_hint = tk.Label(master, text="如 http://localhost:12334，可选", font=font_hint, fg=self.hint_fg, bg=self.bg)
        self.proxy_hint.grid(row=9, column=1, columnspan=2, sticky="w", padx=(0,0))

        
        self.translate_btn = tk.Button(master, text="一键翻译", font=font_btn, bg=self.btn_bg, fg=self.btn_fg, command=self.translate, cursor="hand2", height=2, width=18, bd=0, activebackground=self.btn_hover, activeforeground=self.btn_fg)
        self.translate_btn.grid(row=10, column=0, columnspan=3, sticky="we", padx=36, pady=(26, 0))
        self._add_hover(self.translate_btn, self.btn_bg, self.btn_hover)

        
        self.theme_icon_btn.config(font=font_icon)

        
        master.grid_rowconfigure(11, minsize=20)
        master.grid_columnconfigure(0, minsize=36)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, minsize=80)

    def _get_system_theme(self):
        if platform.system() == 'Windows':
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize') as key:
                    value = winreg.QueryValueEx(key, 'AppsUseLightTheme')[0]
                    return 'light' if value == 1 else 'dark'
            except Exception:
                return 'light'
        elif platform.system() == 'Darwin':
            try:
                import subprocess
                result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], capture_output=True, text=True)
                return 'dark' if 'Dark' in result.stdout else 'light'
            except Exception:
                return 'light'
        else:
            return 'light'

    def _apply_theme(self, theme_name):
        if theme_name == 'system':
            theme_name = self._get_system_theme()
        theme = self.themes[theme_name]
        self.bg = theme['bg']
        self.fg = theme['fg']
        self.entry_bg = theme['entry_bg']
        self.entry_fg = theme['entry_fg']
        self.btn_bg = theme['btn_bg']
        self.btn_fg = theme['btn_fg']
        self.btn_hover = theme['btn_hover']
        self.border = theme['border']
        self.hint_fg = theme['hint_fg']
        self.frame = theme['frame']
        self.icon_bg = theme['icon_bg']
        self.icon_fg = theme['icon_fg']
        self.icon_hover = theme['icon_hover']
        if hasattr(self, 'master'):
            self.master.configure(bg=self.bg)
        if hasattr(self, 'theme_icon_btn'):
            self.theme_icon_btn.config(bg=self.icon_bg, fg=self.icon_fg)
            self._update_theme_icon()

    def _on_theme_icon_click(self, event=None):
        idx = self.theme_cycle.index(self.theme_mode)
        self.theme_mode = self.theme_cycle[(idx + 1) % len(self.theme_cycle)]
        self._apply_theme(self.theme_mode)
        
        for widget in [self.title_label, self.input_label, self.filter_label, self.type_label, self.proxy_label]:
            widget.configure(bg=self.bg, fg=self.fg)
        for widget in [self.filter_hint, self.type_hint, self.proxy_hint]:
            widget.configure(bg=self.bg, fg=self.hint_fg)
        self.sep.configure(bg=self.frame)
        for entry in [self.input_entry, self.filter_entry, self.type_entry, self.proxy_entry]:
            entry.configure(bg=self.entry_bg, fg=self.entry_fg, highlightbackground=self.border, highlightcolor=self.btn_bg)
        for btn in [self.browse_btn, self.translate_btn]:
            btn.configure(bg=self.btn_bg, fg=self.btn_fg, activebackground=self.btn_hover, activeforeground=self.btn_fg)
        self.theme_icon_btn.config(bg=self.icon_bg, fg=self.icon_fg)
        self._update_theme_icon()

    def _update_theme_icon(self):
        
        if self.theme_mode == 'system':
            icon = '\u2699'  # ⚙️
            tip = '跟随系统'
        elif self.theme_mode == 'light':
            icon = '\u2600'  # ☀️
            tip = '浅色模式'
        else:
            icon = '\U0001F319'  # 🌙
            tip = '深色模式'
        self.theme_icon_btn.config(text=icon, fg=self.icon_fg)
        self.theme_icon_btn.tooltip = tip

    def _add_hover(self, widget, normal_bg, hover_bg):
        def on_enter(e): widget["bg"] = hover_bg
        def on_leave(e): widget["bg"] = normal_bg
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def browse_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("XLF 文件", "*.xlf")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

    def translate(self):
        xlf_path = self.input_entry.get().strip()
        filters = [f.strip() for f in self.filter_entry.get().split(",") if f.strip()]
        types = [t.strip() for t in self.type_entry.get().split(",") if t.strip()]
        proxy = self.proxy_entry.get().strip()

        if not xlf_path or not os.path.isfile(xlf_path):
            messagebox.showerror("错误", "请选择有效的 XLF 文件！")
            return

        try:
            self.translate_btn.config(state=tk.DISABLED, text="正在翻译...")
            self.master.update()
            
            if proxy:
                translator = Translate(proxies={'https': proxy})
            else:
                translator = Translate()

            doc = Docts(xlf_path, translator)

            
            for keyword in filters:
                doc.add_filter(lambda word, k=keyword: k in word)

            
            for t in types:
                if t.startswith("page:"):
                    page_num = t.split(":")[1]
                    doc.add_filter(lambda word, p=page_num: f"page {p}" in word)
                elif t == "code":
                    doc.add_filter(lambda word: word.strip().startswith("<code>") or word.strip().endswith("</code>"))

            
            translated_file_path = doc.save_words()
            messagebox.showinfo("完成", f"翻译完成，结果保存至:\n{translated_file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"翻译失败：{e}")
        finally:
            self.translate_btn.config(state=tk.NORMAL, text="一键翻译")

if __name__ == "__main__":
    root = tk.Tk()
    app = XLFTranslatorGUI(root)
    root.mainloop() 