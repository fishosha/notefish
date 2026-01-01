import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font, colorchooser
import os
import json

class Notefish:
    def __init__(self, root):
        self.root = root
        self.root.title("Notefish - Modern Text Editor")
        self.root.geometry("1200x700")
        self.root.minsize(900, 500)
        
        # Современная цветовая схема
        self.colors = {
            "primary": "#667eea",
            "primary_light": "#8e9ffa", 
            "secondary": "#764ba2",
            "bg_light": "#f8fafc",
            "bg_dark": "#1e293b",
            "sidebar": "#334155",
            "text_light": "#f1f5f9",
            "text_dark": "#0f172a",
            "accent": "#06b6d4",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
        
        # Настройка основного фона
        self.root.configure(bg=self.colors["bg_light"])
        
        # Текущий файл
        self.current_file = None
        self.saved = True
        
        # Настройки
        self.current_font = "Segoe UI"
        self.current_font_size = 12
        self.current_theme = "light"
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.setup_ui()
        
        # Загрузка настроек
        self.load_settings()
        
        # Центрирование окна
        self.center_window()
        
        # Обновление статистики
        self.update_stats()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Стиль для кнопок
        style.configure("Primary.TButton",
                       padding=10,
                       relief="flat",
                       font=("Segoe UI", 10, "bold"),
                       background=self.colors["primary"],
                       foreground="white")
        
        style.map("Primary.TButton",
                 background=[('active', self.colors["primary_light"])])
        
        style.configure("Success.TButton",
                       padding=10,
                       relief="flat",
                       font=("Segoe UI", 10, "bold"),
                       background=self.colors["success"],
                       foreground="white")
        
        # Стиль для фреймов
        style.configure("Card.TFrame",
                       background="white",
                       relief="flat",
                       borderwidth=2)
        
        # Стиль для комбобоксов
        style.configure("Modern.TCombobox",
                       fieldbackground="white",
                       background="white")
    
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        # Основной контейнер
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Сетка
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Боковая панель
        self.setup_sidebar(main_container)
        
        # Панель инструментов
        self.setup_toolbar(main_container)
        
        # Основная текстовая область
        self.setup_text_area(main_container)
        
        # Статус бар
        self.setup_statusbar(main_container)
        
        # Привязка горячих клавиш
        self.bind_shortcuts()
        
    def setup_sidebar(self, parent):
        """Создание боковой панели"""
        # Фрейм боковой панели
        sidebar_frame = tk.Frame(parent, bg=self.colors["sidebar"], 
                                width=220)
        sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=(0, 10))
        sidebar_frame.grid_propagate(False)
        
        # Заголовок
        title_label = tk.Label(sidebar_frame, text="NOTEFISH",
                              bg=self.colors["sidebar"],
                              fg="white",
                              font=("Segoe UI", 18, "bold"))
        title_label.pack(pady=(20, 5))
        
        subtitle_label = tk.Label(sidebar_frame, text="Modern Text Editor",
                                 bg=self.colors["sidebar"],
                                 fg=self.colors["primary_light"],
                                 font=("Segoe UI", 9))
        subtitle_label.pack(pady=(0, 20))
        
        # Разделитель
        separator = ttk.Separator(sidebar_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        # Кнопки файловых операций
        buttons = [
            ("📄 Новый файл", self.new_file, self.colors["primary"]),
            ("📂 Открыть файл", self.open_file, self.colors["secondary"]),
            ("💾 Сохранить", self.save_file, self.colors["success"]),
            ("💾 Сохранить как", self.save_as_file, self.colors["warning"]),
            ("🔍 Найти текст", self.find_text, self.colors["accent"]),
            ("🎨 Цвет текста", self.choose_color, "#8b5cf6"),
            ("🌙 Тема", self.toggle_theme, "#64748b")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(sidebar_frame, text=text, command=command,
                           bg=color, fg="white", font=("Segoe UI", 10),
                           relief="flat", padx=15, pady=8,
                           activebackground=color,
                           activeforeground="white")
            btn.pack(fill=tk.X, padx=20, pady=5)
            self.add_hover_effect(btn, color)
        
        # Разделитель
        separator2 = ttk.Separator(sidebar_frame, orient=tk.HORIZONTAL)
        separator2.pack(fill=tk.X, padx=20, pady=20)
        
        # Информация о файле
        info_frame = tk.Frame(sidebar_frame, bg=self.colors["sidebar"])
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.file_info_label = tk.Label(info_frame,
                                       text="Новый файл",
                                       bg=self.colors["sidebar"],
                                       fg="white",
                                       font=("Segoe UI", 10, "bold"))
        self.file_info_label.pack(anchor="w", pady=(0, 10))
        
        self.stats_label = tk.Label(info_frame,
                                   text="Символов: 0\nСтрок: 0",
                                   bg=self.colors["sidebar"],
                                   fg=self.colors["text_light"],
                                   font=("Segoe UI", 9),
                                   justify=tk.LEFT)
        self.stats_label.pack(anchor="w")
    
    def add_hover_effect(self, button, color):
        """Добавляет эффект наведения на кнопку"""
        def on_enter(e):
            button['bg'] = self.lighten_color(color, 10)
        
        def on_leave(e):
            button['bg'] = color
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def lighten_color(self, color, percent):
        """Осветляет цвет на указанный процент"""
        color = color.lstrip('#')
        r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
        
        r = min(255, r + int(r * percent / 100))
        g = min(255, g + int(g * percent / 100))
        b = min(255, b + int(b * percent / 100))
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def setup_toolbar(self, parent):
        """Создание панели инструментов"""
        toolbar_frame = tk.Frame(parent, bg="white", height=50)
        toolbar_frame.grid(row=0, column=1, sticky="ew", pady=(0, 10))
        toolbar_frame.grid_propagate(False)
        
        # Контейнер для кнопок форматирования
        format_frame = tk.Frame(toolbar_frame, bg="white")
        format_frame.pack(side=tk.LEFT, padx=15)
        
        # Кнопки форматирования
        format_buttons = [
            ("✂️", "Вырезать", self.cut_text),
            ("📋", "Копировать", self.copy_text),
            ("📝", "Вставить", self.paste_text),
            ("↶", "Отменить", lambda: self.text_area.edit_undo()),
            ("↷", "Повторить", lambda: self.text_area.edit_redo()),
            ("B", "Жирный", self.toggle_bold),
            ("I", "Курсив", self.toggle_italic),
            ("U", "Подчеркнутый", self.toggle_underline)
        ]
        
        for i, (icon, tooltip, command) in enumerate(format_buttons):
            btn = tk.Button(format_frame, text=icon, command=command,
                           bg="white", fg=self.colors["text_dark"],
                           font=("Segoe UI", 10),
                           relief="flat", width=3)
            btn.grid(row=0, column=i, padx=2)
            self.add_tooltip(btn, tooltip)
            self.add_hover_effect(btn, "white")
        
        # Контейнер для настроек
        settings_frame = tk.Frame(toolbar_frame, bg="white")
        settings_frame.pack(side=tk.RIGHT, padx=15)
        
        # Выбор шрифта
        tk.Label(settings_frame, text="Шрифт:", bg="white",
                font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.font_var = tk.StringVar(value=self.current_font)
        font_combo = ttk.Combobox(settings_frame, textvariable=self.font_var,
                                 values=["Segoe UI", "Arial", "Consolas", 
                                         "Courier New", "Verdana", "Georgia",
                                         "Times New Roman", "Monaco"],
                                 width=15, state="readonly")
        font_combo.pack(side=tk.LEFT, padx=(0, 15))
        font_combo.bind("<<ComboboxSelected>>", self.change_font)
        
        # Размер шрифта
        tk.Label(settings_frame, text="Размер:", bg="white",
                font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.size_var = tk.StringVar(value=str(self.current_font_size))
        size_combo = ttk.Combobox(settings_frame, textvariable=self.size_var,
                                 values=["8", "10", "12", "14", "16", "18", "20", "24"],
                                 width=5, state="readonly")
        size_combo.pack(side=tk.LEFT)
        size_combo.bind("<<ComboboxSelected>>", self.change_font_size)
    
    def add_tooltip(self, widget, text):
        """Добавляет всплывающую подсказку"""
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, bg="yellow", relief="solid", borderwidth=1)
            label.pack()
            
            widget.tooltip = tooltip
            widget.tooltip_label = label
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def setup_text_area(self, parent):
        """Создание текстовой области"""
        # Фрейм для текстовой области с тенью
        text_frame = tk.Frame(parent, bg="white", relief="flat")
        text_frame.grid(row=1, column=1, sticky="nsew", pady=(0, 10))
        
        # Добавляем тень
        text_frame.config(highlightbackground="#e2e8f0", highlightcolor="#e2e8f0", highlightthickness=1)
        
        # Создание текстового редактора
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=(self.current_font, self.current_font_size),
            undo=True,
            maxundo=-1,
            bg="white",
            fg=self.colors["text_dark"],
            insertbackground=self.colors["primary"],
            selectbackground=self.colors["primary_light"],
            relief="flat",
            padx=15,
            pady=15,
            borderwidth=0
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Привязка событий
        self.text_area.bind("<<Modified>>", self.on_text_modified)
        self.text_area.bind("<KeyRelease>", self.update_stats_and_cursor)
        self.text_area.bind("<ButtonRelease>", self.update_cursor_position)
    
    def setup_statusbar(self, parent):
        """Создание статусной строки"""
        status_frame = tk.Frame(parent, bg=self.colors["sidebar"], height=30)
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        status_frame.grid_propagate(False)
        
        # Информация о файле слева
        self.file_label = tk.Label(status_frame,
                                  text="Новый файл",
                                  bg=self.colors["sidebar"],
                                  fg="white",
                                  font=("Segoe UI", 9))
        self.file_label.pack(side=tk.LEFT, padx=15)
        
        # Позиция курсора по центру
        self.cursor_label = tk.Label(status_frame,
                                    text="Строка: 1, Колонка: 1",
                                    bg=self.colors["sidebar"],
                                    fg=self.colors["text_light"],
                                    font=("Segoe UI", 9))
        self.cursor_label.pack(side=tk.LEFT, padx=15)
        
        # Кодировка справа
        encoding_label = tk.Label(status_frame,
                                 text="UTF-8",
                                 bg=self.colors["sidebar"],
                                 fg=self.colors["text_light"],
                                 font=("Segoe UI", 9))
        encoding_label.pack(side=tk.RIGHT, padx=15)
        
        # Статистика символов
        self.char_count_label = tk.Label(status_frame,
                                        text="Символов: 0",
                                        bg=self.colors["sidebar"],
                                        fg=self.colors["text_light"],
                                        font=("Segoe UI", 9))
        self.char_count_label.pack(side=tk.RIGHT, padx=15)
    
    def bind_shortcuts(self):
        """Привязка горячих клавиш"""
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_as_file())
        self.root.bind("<Control-f>", lambda e: self.find_text())
        self.root.bind("<Control-x>", lambda e: self.cut_text())
        self.root.bind("<Control-c>", lambda e: self.copy_text())
        self.root.bind("<Control-v>", lambda e: self.paste_text())
        self.root.bind("<Control-z>", lambda e: self.text_area.edit_undo())
        self.root.bind("<Control-y>", lambda e: self.text_area.edit_redo())
        self.root.bind("<Control-b>", lambda e: self.toggle_bold())
        self.root.bind("<Control-i>", lambda e: self.toggle_italic())
        self.root.bind("<Control-u>", lambda e: self.toggle_underline())
    
    def new_file(self, event=None):
        """Создание нового файла"""
        if not self.saved:
            response = messagebox.askyesnocancel("Notefish", 
                                                "Сохранить изменения в текущем файле?")
            if response is None:
                return
            elif response:
                if not self.save_file():
                    return
        
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.saved = True
        self.file_label.config(text="Новый файл")
        self.file_info_label.config(text="Новый файл")
        self.root.title("Notefish - Новый файл")
        self.update_stats()
    
    def open_file(self, event=None):
        """Открытие файла"""
        if not self.saved:
            response = messagebox.askyesnocancel("Notefish",
                                                "Сохранить изменения в текущем файле?")
            if response is None:
                return
            elif response:
                if not self.save_file():
                    return
        
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*"),
                ("Python файлы", "*.py"),
                ("HTML файлы", "*.html;*.htm"),
                ("CSS файлы", "*.css"),
                ("JavaScript файлы", "*.js"),
                ("Markdown файлы", "*.md")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                
                self.current_file = file_path
                self.saved = True
                filename = os.path.basename(file_path)
                self.file_label.config(text=f"Файл: {filename}")
                self.file_info_label.config(text=f"Файл: {filename}")
                self.root.title(f"Notefish - {filename}")
                self.update_stats()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    def save_file(self, event=None):
        """Сохранение файла"""
        if self.current_file is None:
            return self.save_as_file()
        
        try:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(content)
            
            self.saved = True
            filename = os.path.basename(self.current_file)
            self.file_label.config(text=f"Файл: {filename} ✓")
            self.file_info_label.config(text=f"Файл: {filename} ✓")
            messagebox.showinfo("Сохранение", f"Файл '{filename}' успешно сохранен!")
            return True
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
            return False
    
    def save_as_file(self, event=None):
        """Сохранение файла как"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*"),
                ("Python файлы", "*.py"),
                ("HTML файлы", "*.html;*.htm"),
                ("CSS файлы", "*.css"),
                ("JavaScript файлы", "*.js"),
                ("Markdown файлы", "*.md")
            ]
        )
        
        if file_path:
            self.current_file = file_path
            return self.save_file()
        return False
    
    def find_text(self):
        """Поиск текста"""
        # Создание диалогового окна поиска
        find_window = tk.Toplevel(self.root)
        find_window.title("Найти текст")
        find_window.geometry("400x180")
        find_window.resizable(False, False)
        find_window.configure(bg="white")
        
        # Центрирование
        find_window.transient(self.root)
        find_window.grab_set()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 90
        find_window.geometry(f"+{x}+{y}")
        
        # Поле ввода
        tk.Label(find_window, text="Введите текст для поиска:", 
                bg="white", font=("Segoe UI", 10)).pack(pady=(20, 5))
        
        find_entry = tk.Entry(find_window, font=("Segoe UI", 10),
                             bg="#f8fafc", relief="flat", width=40)
        find_entry.pack(pady=5, padx=20, ipady=5)
        find_entry.focus()
        
        # Фрейм для кнопок
        button_frame = tk.Frame(find_window, bg="white")
        button_frame.pack(pady=15)
        
        def do_find():
            text = find_entry.get()
            if text:
                # Удаляем предыдущее выделение
                self.text_area.tag_remove("found", 1.0, tk.END)
                
                # Ищем текст
                start_pos = "1.0"
                found = False
                
                while True:
                    start_pos = self.text_area.search(text, start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    
                    end_pos = f"{start_pos}+{len(text)}c"
                    self.text_area.tag_add("found", start_pos, end_pos)
                    start_pos = end_pos
                    found = True
                
                # Настраиваем стиль найденного текста
                self.text_area.tag_config("found", background="yellow", foreground="black")
                
                if found:
                    self.text_area.see("found.first")
                    find_window.destroy()
                else:
                    messagebox.showinfo("Поиск", "Текст не найден.")
        
        # Кнопка Найти
        find_btn = tk.Button(button_frame, text="Найти", command=do_find,
                            bg=self.colors["primary"], fg="white",
                            font=("Segoe UI", 10), relief="flat",
                            padx=20, pady=5)
        find_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка Отмена
        cancel_btn = tk.Button(button_frame, text="Отмена", 
                              command=find_window.destroy,
                              bg=self.colors["sidebar"], fg="white",
                              font=("Segoe UI", 10), relief="flat",
                              padx=20, pady=5)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def cut_text(self):
        """Вырезать текст"""
        self.text_area.event_generate("<<Cut>>")
    
    def copy_text(self):
        """Копировать текст"""
        self.text_area.event_generate("<<Copy>>")
    
    def paste_text(self):
        """Вставить текст"""
        self.text_area.event_generate("<<Paste>>")
    
    def toggle_bold(self):
        """Включить/выключить жирный текст"""
        current_font = font.Font(font=self.text_area.cget("font"))
        new_weight = "bold" if current_font.actual()["weight"] != "bold" else "normal"
        
        try:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
            self.text_area.tag_config("bold", font=(self.current_font, self.current_font_size, new_weight))
        except:
            pass
    
    def toggle_italic(self):
        """Включить/выключить курсив"""
        current_font = font.Font(font=self.text_area.cget("font"))
        new_slant = "italic" if current_font.actual()["slant"] != "italic" else "roman"
        
        try:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
            self.text_area.tag_config("italic", font=(self.current_font, self.current_font_size, current_font.actual()["weight"], new_slant))
        except:
            pass
    
    def toggle_underline(self):
        """Включить/выключить подчеркивание"""
        current_font = font.Font(font=self.text_area.cget("font"))
        new_underline = not current_font.actual()["underline"]
        
        try:
            self.text_area.tag_add("underline", "sel.first", "sel.last")
            self.text_area.tag_config("underline", underline=new_underline)
        except:
            pass
    
    def choose_color(self):
        """Выбор цвета текста"""
        color = colorchooser.askcolor(title="Выберите цвет текста",
                                     initialcolor=self.colors["text_dark"])
        if color[1]:
            try:
                self.text_area.tag_add("colored", "sel.first", "sel.last")
                self.text_area.tag_config("colored", foreground=color[1])
            except:
                # Если ничего не выделено, устанавливаем цвет для будущего текста
                pass
    
    def change_font(self, event=None):
        """Изменение шрифта"""
        self.current_font = self.font_var.get()
        self.text_area.config(font=(self.current_font, self.current_font_size))
    
    def change_font_size(self, event=None):
        """Изменение размера шрифта"""
        self.current_font_size = int(self.size_var.get())
        self.text_area.config(font=(self.current_font, self.current_font_size))
    
    def toggle_theme(self):
        """Переключение темы"""
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.colors = {
                "primary": "#4c51bf",
                "primary_light": "#667eea",
                "secondary": "#7f00ff",
                "bg_light": "#1e293b",
                "bg_dark": "#0f172a",
                "sidebar": "#334155",
                "text_light": "#f1f5f9",
                "text_dark": "#cbd5e1",
                "accent": "#06b6d4",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444"
            }
        else:
            self.current_theme = "light"
            self.colors = {
                "primary": "#667eea",
                "primary_light": "#8e9ffa",
                "secondary": "#764ba2",
                "bg_light": "#f8fafc",
                "bg_dark": "#1e293b",
                "sidebar": "#334155",
                "text_light": "#f1f5f9",
                "text_dark": "#0f172a",
                "accent": "#06b6d4",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444"
            }
        
        self.update_theme()
    
    def update_theme(self):
        """Обновление темы интерфейса"""
        # Основное окно
        self.root.configure(bg=self.colors["bg_light"])
        
        # Обновляем все виджеты
        for widget in self.root.winfo_children():
            self.update_widget_colors(widget)
    
    def update_widget_colors(self, widget):
        """Рекурсивно обновляет цвета виджетов"""
        widget_type = widget.winfo_class()
        
        if widget_type == "Frame" and hasattr(widget, 'cget'):
            try:
                if widget.cget("bg") == "white" or widget.cget("bg") == "#f8fafc":
                    widget.configure(bg=self.colors["bg_light"])
                elif widget.cget("bg") == "#334155" or "sidebar" in str(widget):
                    widget.configure(bg=self.colors["sidebar"])
            except:
                pass
        
        elif widget_type == "Label":
            try:
                if widget.cget("bg") == "white" or widget.cget("bg") == "#f8fafc":
                    widget.configure(bg=self.colors["bg_light"], fg=self.colors["text_dark"])
                elif widget.cget("bg") == "#334155":
                    widget.configure(bg=self.colors["sidebar"], fg=self.colors["text_light"])
            except:
                pass
        
        elif widget_type == "Button":
            try:
                # Сохраняем цвет кнопки, если он не стандартный
                current_bg = widget.cget("bg")
                if current_bg not in ["#667eea", "#764ba2", "#10b981", "#f59e0b", 
                                     "#06b6d4", "#8b5cf6", "#64748b", "#4c51bf"]:
                    widget.configure(bg=current_bg)
            except:
                pass
        
        # Рекурсивно обходим дочерние виджеты
        for child in widget.winfo_children():
            self.update_widget_colors(child)
    
    def update_stats_and_cursor(self, event=None):
        """Обновление статистики и позиции курсора"""
        self.update_stats()
        self.update_cursor_position()
    
    def update_stats(self, event=None):
        """Обновление статистики"""
        content = self.text_area.get(1.0, tk.END)
        char_count = len(content) - 1  # Минус символ новой строки в конце
        lines = content.split('\n')
        line_count = len(lines) - 1 if lines[-1] == '' else len(lines)
        
        stats_text = f"Символов: {char_count}\nСтрок: {line_count}"
        self.stats_label.config(text=stats_text)
        self.char_count_label.config(text=f"Символов: {char_count}")
    
    def update_cursor_position(self, event=None):
        """Обновление позиции курсора"""
        cursor_pos = self.text_area.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.cursor_label.config(text=f"Строка: {line}, Колонка: {int(col)+1}")
    
    def on_text_modified(self, event=None):
        """Обработка изменения текста"""
        self.text_area.edit_modified(False)
        
        if self.current_file:
            filename = os.path.basename(self.current_file)
            self.file_label.config(text=f"Файл: {filename} *")
            self.file_info_label.config(text=f"Файл: {filename} *")
            self.root.title(f"Notefish - {filename} *")
        else:
            self.file_label.config(text="Новый файл *")
            self.file_info_label.config(text="Новый файл *")
            self.root.title("Notefish - Новый файл *")
        
        self.saved = False
        self.update_stats()
    
    def load_settings(self):
        """Загрузка настроек"""
        try:
            if os.path.exists("notefish_settings.json"):
                with open("notefish_settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                
                self.current_theme = settings.get("theme", "light")
                self.current_font = settings.get("font", "Segoe UI")
                self.current_font_size = settings.get("font_size", 12)
                
                # Применяем тему
                if self.current_theme == "dark":
                    self.toggle_theme()
                
                # Применяем шрифт
                self.font_var.set(self.current_font)
                self.size_var.set(str(self.current_font_size))
                self.text_area.config(font=(self.current_font, self.current_font_size))
                
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
    
    def save_settings(self):
        """Сохранение настроек"""
        settings = {
            "theme": self.current_theme,
            "font": self.current_font,
            "font_size": self.current_font_size
        }
        
        try:
            with open("notefish_settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def center_window(self):
        """Центрирование окна"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def on_closing(self):
        """Обработка закрытия окна"""
        if not self.saved:
            response = messagebox.askyesnocancel("Notefish", 
                                                "Сохранить изменения перед выходом?")
            if response is None:
                return
            elif response:
                if not self.save_file():
                    return
        
        self.save_settings()
        self.root.destroy()

def main():
    """Основная функция запуска приложения"""
    try:
        root = tk.Tk()
        
        # Устанавливаем иконку
        try:
            root.iconbitmap(default='notefish.ico')
        except:
            # Если нет файла иконки, используем стандартную
            pass
        
        app = Notefish(root)
        
        # Обработчик закрытия окна
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Запуск главного цикла
        root.mainloop()
        
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        messagebox.showerror("Ошибка", f"Не удалось запустить приложение:\n{str(e)}")

if __name__ == "__main__":
    main()