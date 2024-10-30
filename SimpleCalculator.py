import tkinter as tk

LARGE_FONT_STYLE = ("Mono Sans", 40, "bold")
SMALL_FONT_STYLE = ("Mono Sans", 16)
DIGITS_FONT_STYLE = ("Mono Sans", 24, "bold")
DEFAULT_FONT_STYLE = ("Mono Sans", 20)

WHITE = "#FFFFFF"
ORANGE = "#F1770B"
BLACK = "#000000"
DARKER_GRAY = "#0A0A0A"
DARK_GRAY = "#212121"



class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(1, 1)
        self.window.title("Simple Calculator")

        self.final_expression = ""
        self.final_answer = ""
        self.display_frame = self.create_display_frame()

        self.full_label, self.label = self.create_display_labels()

        self.digits = {
            7:(1, 1), 8:(1, 2), 9:(1, 3),
            4:(2, 1), 5:(2, 2), 6:(2, 3),
            1:(3, 1), 2:(3, 2), 3:(3, 3),
            '.':(4, 1), 0:(4, 2)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        full_label = tk.Label(self.display_frame, text=self.final_expression, anchor=tk.E, bg=BLACK,
                               fg=WHITE, padx=24, font=SMALL_FONT_STYLE)
        full_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.final_answer, anchor=tk.E, bg=BLACK,
                         fg=WHITE, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return full_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=BLACK)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.final_answer += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=DARK_GRAY, fg=WHITE, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.final_answer += operator
        self.final_expression += self.final_answer
        self.final_answer = ""
        self.update_full_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=DARKER_GRAY, fg=WHITE, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.final_answer = ""
        self.final_expression = ""
        self.update_label()
        self.update_full_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=DARKER_GRAY, fg=WHITE, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.final_answer = str(eval(f"{self.final_answer}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=DARKER_GRAY, fg=WHITE, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.final_answer = str(eval(f"{self.final_answer}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=DARKER_GRAY, fg=WHITE, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.final_expression += self.final_answer
        self.update_full_label()
        try:
            self.final_answer = str(eval(self.final_expression))

            self.final_expression = ""
        except Exception as e:
            self.final_answer = "ERROR"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=ORANGE, fg=WHITE, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_full_label(self):
        expression = self.final_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.full_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.final_answer[:11])

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()