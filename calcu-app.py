import tkinter as tk
from tkinter import ttk

class PinkCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("380x580")
        self.root.configure(bg="#F9B4CE")  # Soft pink background
        self.root.resizable(False, False)

        self.expression = ""
        self.current_value = "0"

        # Configure Custom TTK Styles for Rounded Buttons
        self.style = ttk.Style()
        self.style.theme_use('default')

        # White/Light pink buttons (Numbers)
        self.style.configure(
            "Num.TButton",
            font=("Helvetica", 18),
            background="#FFF0F5",
            foreground="#E05A88",
            borderwidth=0,
            focusthickness=0,
            focuscolor='none'
        )
        self.style.map("Num.TButton", background=[("active", "#FFE4E1")])

        # Darker pink buttons (Top Row Functions & Operators)
        self.style.configure(
            "Op.TButton",
            font=("Helvetica", 18),
            background="#F693B6",
            foreground="#FFFFFF",
            borderwidth=0,
            focusthickness=0,
            focuscolor='none'
        )
        self.style.map("Op.TButton", background=[("active", "#E57EA3")])

        self.create_layouts()

    def create_layouts(self):
        # --- DISPLAY SCREEN ---
        display_frame = tk.Frame(self.root, bg="#F9B4CE")
        display_frame.pack(expand=True, fill="both", padx=20, pady=(20, 10))

        # Small text for history/expression
        self.history_label = tk.Label(
            display_frame, text="", anchor="e", font=("Helvetica", 12),
            bg="#F9B4CE", fg="#FFFFFF"
        )
        self.history_label.pack(fill="x", side="top")

        # Main large numbers display
        self.result_label = tk.Label(
            display_frame, text="0", anchor="e", font=("Helvetica", 36, "bold"),
            bg="#F9B4CE", fg="#FFFFFF"
        )
        self.result_label.pack(fill="x", side="top", pady=5)

        # --- BUTTONS FRAME ---
        buttons_frame = tk.Frame(self.root, bg="#F9B4CE")
        buttons_frame.pack(expand=True, fill="both", padx=15, pady=(0, 20))

        # Grid configuration for spacing
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1, pad=8)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1, pad=8)

        # Button Layout Grid
        buttons = [
            ('AC', 0, 0, 'Op.TButton'), ('+/-', 0, 1, 'Op.TButton'), ('%', 0, 2, 'Op.TButton'), ('⌫', 0, 3, 'Op.TButton'),
            ('7', 1, 0, 'Num.TButton'), ('8', 1, 1, 'Num.TButton'), ('9', 1, 2, 'Num.TButton'), ('÷', 1, 3, 'Op.TButton'),
            ('4', 2, 0, 'Num.TButton'), ('5', 2, 1, 'Num.TButton'), ('6', 2, 2, 'Num.TButton'), ('×', 2, 3, 'Op.TButton'),
            ('1', 3, 0, 'Num.TButton'), ('2', 3, 1, 'Num.TButton'), ('3', 3, 2, 'Num.TButton'), ('-', 3, 3, 'Op.TButton'),
            ('0', 4, 0, 'Num.TButton'), ('.', 4, 2, 'Num.TButton'),  ('+', 4, 3, 'Op.TButton')
        ]

        # Render all standard buttons
        for text, row, col, style in buttons:
            colspan = 2 if text == '0' else 1  # Make '0' button wider
            btn = ttk.Button(
                buttons_frame, text=text, style=style,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)

        # Bottom full-width Equal (=) button
        equal_btn = ttk.Button(
            buttons_frame, text="=", style='Op.TButton',
            command=lambda: self.on_button_click('=')
        )
        equal_btn.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=4, pady=10)
        buttons_frame.rowconfigure(5, weight=1, pad=8)

    def on_button_click(self, char):
        if char == 'AC':
            self.expression = ""
            self.current_value = "0"
            self.history_label.config(text="")
        elif char == '⌫':
            if len(self.current_value) > 1:
                self.current_value = self.current_value[:-1]
            else:
                self.current_value = "0"
        elif char in ['+', '-', '×', '÷', '%']:
            op_map = {'×': '*', '÷': '/'}
            actual_op = op_map.get(char, char)
            self.expression = f"{self.current_value} {actual_op} "
            self.history_label.config(text=f"{self.current_value} {char}")
            self.current_value = "0"
        elif char == '=':
            if self.expression:
                full_expr = self.expression + self.current_value
                try:
                    # Safeguard evaluation
                    result = eval(full_expr)
                    # Format float results gracefully
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                    self.history_label.config(text=f"{full_expr.replace('*', '×').replace('/', '÷')} =")
                    self.current_value = str(result)
                    self.expression = ""
                except Exception:
                    self.current_value = "Error"
        elif char == '+/-':
            if self.current_value != "0":
                if self.current_value.startswith("-"):
                    self.current_value = self.current_value[1:]
                else:
                    self.current_value = "-" + self.current_value
        else:  # Numbers and Decimals
            if self.current_value == "0" and char != ".":
                self.current_value = char
            else:
                if char == "." and "." in self.current_value:
                    pass  # Prevent multiple decimals
                else:
                    self.current_value += char

        self.result_label.config(text=self.current_value)

if __name__ == "__main__":
    root = tk.Tk()
    app = PinkCalculator(root)
    root.mainloop()