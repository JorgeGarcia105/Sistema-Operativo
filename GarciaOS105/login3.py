from ctypes import alignment
import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette

class ProfileSelectionWindow(QWidget):
    # Ventana para seleccionar un perfil de una lista
    def __init__(self, profiles):
        # Inicialización de la ventana
        super().__init__()
        self.profiles = profiles

        # Ruta de la imagen de fondo
        self.BACKGROUND_IMAGE_PATH = "./GarciaOS105/images/fondo.png"

        # Configuración de la ventana principal
        self.setWindowTitle("Selección de Perfil")
        self.setGeometry(100, 100, 800, 600)

        # Establecer la imagen de fondo
        self.set_background_image()

        # Diseño de la ventana principal
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Agregar widgets para cada perfil
        for profile_name, profile_data in self.profiles.items():
            profile_widget = ProfileWidget(profile_name, profile_data['image'], self, profile_data['username'], profile_data['password'])
            layout.addWidget(profile_widget)

        self.setLayout(layout)

    # Método para abrir los datos de inicio de sesión para el perfil seleccionado
    def open_login_window(self, profile_name, username, password):
        # Crear el widget de inicio de sesión
        self.login_widget = LoginWidget(profile_name, self.profiles[profile_name]['image'], username, password)
        
        # Obtener el layout actual o crear uno nuevo si no existe
        layout = self.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.setLayout(layout)
        
        # Agregar el widget de inicio de sesión al layout
        layout.addWidget(self.login_widget)
        
        # Ocultar los widgets de perfil existentes
        for i in range(layout.count()):
            widget_item = layout.itemAt(i)
            if widget_item and widget_item.widget() != self.login_widget:
                widget = widget_item.widget()
                if widget:
                    widget.setVisible(False)

    # Método para establecer la imagen de fondo
    def set_background_image(self, image_path=None):
        if image_path is None:
            image_path = self.BACKGROUND_IMAGE_PATH
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(image_path)))
        self.setPalette(palette)


class LoginWidget(QWidget):
    # Widget para mostrar los datos de inicio de sesión del perfil seleccionado
    def __init__(self, profile_name, profile_image, username, password):
        # Inicialización del widget
        super().__init__()

        # Configuración del widget
        self.profile_name = profile_name
        self.profile_image = profile_image
        self.expected_username = username
        self.expected_password = password

        # Diseño del widget
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 10, 20, 10)

        # Etiqueta de la imagen del perfil
        self.image_label = QLabel()
        pixmap = QPixmap(self.profile_image)
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Etiqueta del nombre del perfil
        self.name_label = QLabel(profile_name)
        self.name_label.setFont(QFont("Arial", 14))

        # Campo de entrada de nombre de usuario
        username_layout = QVBoxLayout()
        self.username_label = QLabel("Nombre de Usuario:")
        self.username_entry = QLineEdit()
        self.username_entry.setText(self.expected_username)
        self.username_entry.setMaximumWidth(200)  # Establecer una anchura máxima
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_entry)

        # Campo de entrada de contraseña
        password_layout = QVBoxLayout()
        self.password_label = QLabel("Contraseña:")
        self.password_entry = QLineEdit()
        self.password_entry.setText(self.expected_password)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setMaximumWidth(200)  # Establecer una anchura máxima
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_entry)

        # Alineación horizontal para centrar los campos de entrada
        username_h_layout = QHBoxLayout()
        username_h_layout.addStretch()
        username_h_layout.addLayout(username_layout)
        username_h_layout.addStretch()

        password_h_layout = QHBoxLayout()
        password_h_layout.addStretch()
        password_h_layout.addLayout(password_layout)
        password_h_layout.addStretch()

        # Botón de inicio de sesión
        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.login)
        self.btn_login.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; padding: 10px; font-size: 16px; }"
                                      "QPushButton:hover { background-color: #45a049; }")

        # Etiqueta de error
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 14px;")

        # Agregar widgets al diseño
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(username_h_layout)
        layout.addLayout(password_h_layout)
        layout.addWidget(self.btn_login, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    # Método para realizar el inicio de sesión
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
    # Widget para mostrar un perfil y permitir su selección
    def __init__(self, profile_name, profile_image, parent, username, password):
        # Inicialización del widget
        super().__init__()
        self.profile_name = profile_name
        self.profile_image = profile_image
        self.parent = parent
        self.username = username
        self.password = password

        # Diseño del widget de perfil
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)

        # Etiqueta de la imagen del perfil
        self.image_label = QLabel()
        pixmap = QPixmap(self.profile_image)
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation )) #SmoothTransformation
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Etiqueta del nombre del perfil
        self.name_label = QLabel(profile_name)
        self.name_label.setFont(QFont("Arial", 14))
        self.name_label.setStyleSheet("color: white") 

        # Botón de selección del perfil
        self.btn_select = QPushButton("Seleccionar")
        self.btn_select.clicked.connect(self.select_profile)
        self.btn_select.setStyleSheet("QPushButton { background-color: #008CBA; color: white; border: none; padding: 10px; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #006699; }")

        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_select, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    # Método llamado cuando se selecciona un perfil
    def select_profile(self):
        self.parent.open_login_window(self.profile_name, self.username, self.password)
        # Cambiar la imagen de fondo al seleccionar un perfil
        self.parent.set_background_image(self.parent.profiles[self.profile_name]['background_image'])
if __name__ == "__main__":
    # Directorio de imágenes
    IMAGES_DIR = "./GarciaOS105/images/"
    BACKGROUND_IMAGE_PATH = os.path.join(IMAGES_DIR, "fondo.png")

    # Cargar perfiles desde un archivo JSON y ejecutar la aplicación
    with open("./GarciaOS105/profiles.json", "r") as file:
        profiles = json.load(file)

    app = QApplication(sys.argv)
    profile_window = ProfileSelectionWindow(profiles)
    profile_window.show()
    sys.exit(app.exec_())