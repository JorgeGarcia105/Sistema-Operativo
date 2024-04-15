from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

class EditorTextoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor de texto - GarciaOS")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit()
        self.clear_button = QPushButton("Borrar todo")
        self.clear_button.clicked.connect(self.clear_text)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.clear_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def clear_text(self):
        self.text_edit.clear()