import tkinter as tk
import customtkinter as ctk
from CTkListbox import CTkListbox
from calculator import calculate, calculate_scientific
from history import save_history, load_history

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("500x600")
        self.root.resizable(True, True)

        # режим переключения
        self.mode = "standard"

        # кнопки режима
        mode_frame = ctk.CTkFrame(root, fg_color="transparent")
        mode_frame.grid(row=0, column=0, columnspan=4, pady=5)

        ctk.CTkButton(
            mode_frame, text="Standard", width=100,
            command=lambda: self.switch_mode("standard")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            mode_frame, text="Scientific", width=100,
            command=lambda: self.switch_mode("scientific")
        ).pack(side="left", padx=5)

        # поле ввода
        self.entry = ctk.CTkEntry(
            root, font=("Arial", 24),
            width=460, height=70,
            corner_radius=10, justify="right"
        )
        self.entry.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # фрейм для кнопок
        self.buttons_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.buttons_frame.grid(row=2, column=0, columnspan=4)

        # history и clear
        self.bottom_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.bottom_frame.grid(row=3, column=0, columnspan=4, pady=5)

        ctk.CTkButton(
            self.bottom_frame, text="History", width=220,
            command=self.show_history
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            self.bottom_frame, text="Clear", width=220,
            fg_color="#D32F2F", hover_color="#E53935",
            command=self.clear
        ).pack(side="left", padx=4)

        # история
        self.history_box = CTkListbox(
            root, width=400, height=80,
            corner_radius=12, border_width=2,
            fg_color="#1e1e1e", text_color="white",
            hover_color="#2a2a2a"
        )
        self.history_box.grid(row=4, column=0, columnspan=4, pady=10, padx=10)
        self.history_box.bind("<<ListboxSelect>>", self.on_select)

        # строим стандартные кнопки
        self.build_standard()

    def build_standard(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        self.root.geometry("500x650")

        buttons = [
            'CE', '±', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            'π', '0', '.', '='
        ]

        row, col = 0, 0
        for btn in buttons:
            if btn == '=':
                color, hover = "#FF9500", "#FFB143"
            elif btn in '+-*/':
                color, hover = "#505050", "#686868"
            elif btn in ['CE', '±', '%', 'π']:
                color, hover = "#2A2A2A", "#3A3A3A"  # тёмные спец кнопки
            else:
                color, hover = "#333333", "#4A4A4A"

            ctk.CTkButton(
                self.buttons_frame,
                text=btn, width=110, height=60,
                corner_radius=8,
                fg_color=color, hover_color=hover,
                font=("Arial", 18),
                command=lambda b=btn: self.click(b)
            ).grid(row=row, column=col, padx=4, pady=4)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def build_scientific(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        self.root.geometry("500x750")

        sci_buttons = [
            ("√", "sqrt"), ("log", "log"), ("ln", "ln"), ("x!", "fact"),
            ("sin", "sin"), ("cos", "cos"), ("tan", "tan"), ("x²", "x2"),
            ("x³", "x3"), ("xʸ", "xy"), ("1/x", "1/x"), ("e", "e"),
        ]

        for i, (label, op) in enumerate(sci_buttons):
            ctk.CTkButton(
                self.buttons_frame,
                text=label, width=110, height=45,
                corner_radius=8,
                fg_color="#1E5080", hover_color="#2A6FA8",
                font=("Arial", 14),
                command=lambda o=op: self.sci_click(o)
            ).grid(row=i // 4, column=i % 4, padx=4, pady=4)

        # цифры под научными
        buttons = [
            'CE', '±', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            'π', '0', '.', '='
        ]
        row, col = 3, 0
        for btn in buttons:
            if btn == '=':
                color, hover = "#FF9500", "#FFB143"
            elif btn in '+-*/':
                color, hover = "#505050", "#686868"
            elif btn in ['CE', '±', '%', 'π']:
                color, hover = "#2A2A2A", "#3A3A3A"
            else:
                color, hover = "#333333", "#4A4A4A"

            ctk.CTkButton(
                self.buttons_frame,
                text=btn, width=110, height=55,
                corner_radius=8,
                fg_color=color, hover_color=hover,
                font=("Arial", 18),
                command=lambda b=btn: self.click(b)
            ).grid(row=row, column=col, padx=4, pady=4)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def switch_mode(self, mode):
        self.mode = mode
        if mode == "scientific":
            self.build_scientific()
        else:
            self.build_standard()

    def click(self, btn):
        if btn == '=':
            expr = self.entry.get()
            result = calculate(expr)
            save_history(expr, result)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result))
            self.show_history()

        elif btn == 'CE':
            # удаляет последний символ
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current[:-1])

        elif btn == '±':
            # меняет знак числа
            current = self.entry.get()
            try:
                value = float(current)
                value = -value
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(value))
            except:
                pass

        elif btn == '%':
            # делит на 100
            current = self.entry.get()
            try:
                value = float(current) / 100
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(value))
            except:
                pass

        elif btn == 'π':
            import math
            self.entry.insert(tk.END, str(math.pi))

        else:
            self.entry.insert(tk.END, btn)

    def sci_click(self, operation):
        from calculator import calculate_scientific
        value = self.entry.get()

        if operation == "xy":
            # пользователь вводит основание, добавляем **
            self.entry.insert(tk.END, "**")
            return

        if operation == "e":
            import math
            self.entry.insert(tk.END, str(math.e))
            return

        result = calculate_scientific(operation, value)
        save_history(f"{operation}({value})", result)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(result))

    def clear(self):
        self.entry.delete(0, tk.END)

    def show_history(self):
        self.history_box.delete(0, "end")
        for item in load_history():
            self.history_box.insert(tk.END, item)

    def on_select(self, event):
        selected = self.history_box.get()
        if selected:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected.split('=')[0].strip())


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = CalculatorApp(root)
    root.mainloop()