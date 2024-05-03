import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QVBoxLayout, QLayout
from PyQt5.QtWidgets import QApplication

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Científica")
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                font-size: 18px;
                padding: 5px;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                font-size: 18px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #d3d3d3;
            }
            QPushButton:pressed {
                background-color: #c6c6c6;
            }
        """)

        self.layout: QLayout = QVBoxLayout()   
        self.setLayout(self.layout)

        # Pantalla de la calculadora
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.layout.addWidget(self.result_display)

        # Crear botones para dígitos y operadores
        buttons_layout = QVBoxLayout()
        self.layout.addLayout(buttons_layout)

        buttons = [
            ("7", "8", "9", "/", "C"),
            ("4", "5", "6", "*", "⌫"),
            ("1", "2", "3", "-", "("),
            ("0", ".", "=", "+", ")"),
            ("sin", "cos", "tan", "sqrt", "^"),
            ("log", "ln", "exp", "pi", "e")
        ]

        for row in buttons:
            row_layout = QHBoxLayout()
            for text in row:
                button = QPushButton(text)
                if text.isdigit() or text in "+-*/.()":
                    button.clicked.connect(lambda _, text=text: self.append_to_display(text))
                elif text == "=":
                    button.clicked.connect(self.show_result)
                elif text == "⌫":
                    button.clicked.connect(self.backspace)
                elif text == "C":
                    button.clicked.connect(self.clear_display)
                elif text in {"sin", "cos", "tan", "sqrt", "^", "log", "ln", "exp", "pi", "e"}:
                    button.clicked.connect(lambda _, text=text: self.insert_special(text))
                row_layout.addWidget(button)
            buttons_layout.addLayout(row_layout)

    def append_to_display(self, text):
        current_text = self.result_display.text()
        if text == "=":
            self.show_result()
        elif text == "C":
            self.result_display.clear()
        elif text == "←":  # Botón para borrar un solo caracter
            self.result_display.backspace()
        elif text == "^":  # Operador de potencia
            self.result_display.setText(current_text + "^")
        else:
            new_text = current_text + text
            self.result_display.setText(new_text)


    def backspace(self):
        current_text = self.result_display.text()
        new_text = current_text[:-1]
        self.result_display.setText(new_text)

    def clear_display(self):
        self.result_display.clear()

    def show_result(self):
        current_text = self.result_display.text()
        try:
            # Evaluar la expresión usando la función eval() de Python
            result = eval(current_text, {"__builtins__": None}, {"sin": math.sin, "cos": math.cos, "tan": math.tan, "sqrt": math.sqrt, "log": math.log10, "ln": math.log, "exp": math.exp, "pi": math.pi, "e": math.e})
            self.result_display.setText(str(result))
        except Exception as e:
            self.result_display.setText("Error")

    def insert_special(self, text):
        current_text = self.result_display.text()
        if text == "sin":
            self.result_display.setText(current_text + "sin(")
        elif text == "cos":
            self.result_display.setText(current_text + "cos(")
        elif text == "tan":
            self.result_display.setText(current_text + "tan(")
        elif text == "sqrt":
            self.result_display.setText(current_text + "sqrt(")
        elif text == "^":
            self.result_display.setText(current_text + "**")
        elif text == "log":
            self.result_display.setText(current_text + "log10(")
        elif text == "ln":
            self.result_display.setText(current_text + "log(")
        elif text == "exp":
            self.result_display.setText(current_text + "exp(")
        elif text == "pi":
            self.result_display.setText(current_text + "3.141592653589793")
        elif text == "e":
            self.result_display.setText(current_text + "2.718281828459045")
