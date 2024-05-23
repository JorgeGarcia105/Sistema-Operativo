from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class RegisterWindow(QWidget):
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.setWindowTitle("Registrar Usuario")

        self.layout: QVBoxLayout = QVBoxLayout()

        self.username_label = QLabel("Nombre de Usuario:")
        self.username_entry = QLineEdit()

        self.password_label = QLabel("Contraseña:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Registrar")
        self.register_button.clicked.connect(self.register)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_entry)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_entry)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        try:
            self.user_manager.create_user(username, password)
            QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente")
            self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
