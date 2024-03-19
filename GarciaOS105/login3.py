import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt

# Parte 1: Clases de la ventana de selección de perfil y la ventana de inicio de sesión

class LoginWindow(QWidget):
    def __init__(self, profile_name, profile_image, username, password):
        super().__init__()

        self.setWindowTitle("Inicio de Sesión")

        self.profile_name = profile_name
        self.profile_image = profile_image
        self.expected_username = username
        self.expected_password = password

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)

        self.image_label = QLabel()
        pixmap = QPixmap(self.profile_image)
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel(profile_name)
        self.name_label.setFont(QFont("Arial", 16))

        self.username_label = QLabel("Nombre de Usuario:")
        self.username_entry = QLineEdit()
        self.username_entry.setText(self.expected_username)
        self.password_label = QLabel("Contraseña:")
        self.password_entry = QLineEdit()
        self.password_entry.setText(self.expected_password)
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.login)
        self.btn_login.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; padding: 10px; font-size: 16px; }"
                                      "QPushButton:hover { background-color: #45a049; }")

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 14px;")

        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.error_label, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def login(self):
        entered_username = self.username_entry.text()
        entered_password = self.password_entry.text()

        if entered_username == "" or entered_password == "":
            self.error_label.setText("Por favor, complete todos los campos.")
            return

        if entered_username == self.expected_username and entered_password == self.expected_password:
            QMessageBox.information(self, "Inicio de Sesión", f"Inicio de sesión exitoso. ¡Bienvenido, {entered_username}!")
        else:
            self.error_label.setText("Error de inicio de sesión. Nombre de usuario o contraseña incorrectos.")

class ProfileWidget(QWidget):
    def __init__(self, profile_name, profile_image, callback):
        super().__init__()
        self.profile_name = profile_name
        self.profile_image = profile_image
        self.callback = callback

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)

        self.image_label = QLabel()
        pixmap = QPixmap(self.profile_image)
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel(profile_name)
        self.name_label.setFont(QFont("Arial", 14))

        self.btn_select = QPushButton("Seleccionar")
        self.btn_select.clicked.connect(self.select_profile)
        self.btn_select.setStyleSheet("QPushButton { background-color: #008CBA; color: white; border: none; padding: 10px; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #006699; }")

        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_select, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def select_profile(self):
        self.callback(self.profile_name)

class ProfileSelectionWindow(QWidget):
    def __init__(self, profiles):
        super().__init__()
        self.profiles = profiles

        self.setWindowTitle("Selección de Perfil")
        self.setGeometry(100, 100, 800, 600)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        for profile_name, profile_data in self.profiles.items():
            profile_widget = ProfileWidget(profile_name, profile_data['image'], self.open_login_window)
            layout.addWidget(profile_widget)

        self.setLayout(layout)

    def open_login_window(self, profile_name):
        profile_data = self.profiles[profile_name]
        self.login_window = LoginWindow(profile_name, profile_data['image'], profile_data['username'], profile_data['password'])
        self.login_window.show()

# Parte 2: Cargar perfiles desde un archivo JSON y ejecutar la aplicación

if __name__ == "__main__":
    with open("./GarciaOS105/profiles.json", "r") as file:
        profiles = json.load(file)

    app = QApplication(sys.argv)
    profile_window = ProfileSelectionWindow(profiles)
    profile_window.show()
    sys.exit(app.exec_())
