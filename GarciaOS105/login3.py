import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QCursor

# Clase de la ventana de selección de perfil
class ProfileSelectionWindow(QWidget):
    def __init__(self, profiles):
        super().__init__()
        self.profiles = profiles
        self.initial_background_image = "./GarciaOS105/images/fondo.png"  # Guardar la imagen de fondo inicial
        self.initial_profiles = profiles.copy()  # Guardar los perfiles iniciales

        # Configurar la ventana principal
        self.setWindowTitle("Selección de Perfil")
        self.setGeometry(100, 100, 800, 600)
        self.set_background_image()

        # Configurar el diseño de la ventana principal
        self.main_layout = QHBoxLayout()  # Renombrar self.layout a self.main_layout
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        self.populate_profile_widgets()

    # Restaurar el estado inicial de la ventana principal
    def restore_initial_state(self):
        self.set_background_image(self.initial_background_image)
        self.profiles = self.initial_profiles.copy()

        # Limpiar cualquier widget existente en la ventana principal
        for i in reversed(range(self.main_layout.count())):
            widget_item = self.main_layout.itemAt(i)
            if widget_item:
                widget = widget_item.widget()
                if widget:
                    widget.deleteLater()

        # Volver a poblar los widgets de perfil
        self.populate_profile_widgets()

    # Poblar los widgets de perfil en la ventana principal
    def populate_profile_widgets(self):
        for profile_name, profile_data in self.profiles.items():
            profile_widget = ProfileWidget(profile_name, profile_data['image'], self, profile_data['username'], profile_data['password'])
            self.main_layout.addWidget(profile_widget)

    # Abrir la ventana de inicio de sesión
    def open_login_window(self, profile_name, username, password):
        self.restore_initial_state()  # Restaurar el estado inicial antes de abrir la ventana de inicio de sesión
        self.login_widget = LoginWidget(profile_name, self.profiles[profile_name]['image'], username, password, self)
        
        # Ocultar todos los widgets existentes en la ventana principal
        for i in reversed(range(self.main_layout.count())):
            widget_item = self.main_layout.itemAt(i)
            if widget_item:
                widget = widget_item.widget()
                if widget:
                    widget.setVisible(False)

        # Agregar el widget de inicio de sesión a la ventana principal
        self.main_layout.addWidget(self.login_widget)

    # Establecer la imagen de fondo de la ventana principal
    def set_background_image(self, image_path=None):
        if image_path is None:
            image_path = self.initial_background_image
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(image_path)))
        self.setPalette(palette)

# Clase del widget de inicio de sesión
class LoginWidget(QWidget):
    # Inicializar el widget de inicio de sesión
    def __init__(self, profile_name, profile_image, username, password, parent_window):
        super().__init__()

        # Guardar los datos del perfil y la ventana principal
        self.profile_name = profile_name
        self.profile_image = profile_image
        self.expected_username = username
        self.expected_password = password
        self.parent_window = parent_window

        # Configurar el diseño del widget de inicio de sesión
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 10, 20, 10)

        # Crear los widgets de la interfaz de inicio de sesión
        self.image_label = QLabel()
        pixmap = QPixmap(self.profile_image)
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Crear la etiqueta del nombre del perfil
        self.name_label = QLabel(profile_name)
        self.name_label.setFont(QFont("Arial", 14))

        # Crear los campos de entrada de nombre de usuario y contraseña
        username_layout = QVBoxLayout()
        self.username_label = QLabel("Nombre de Usuario:")
        self.username_entry = QLineEdit()
        self.username_entry.setText(self.expected_username)
        self.username_entry.setMaximumWidth(200)
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_entry)

        # Crear los campos de entrada de contraseña
        password_layout = QVBoxLayout()
        self.password_label = QLabel("Contraseña:")
        self.password_entry = QLineEdit()
        self.password_entry.setText(self.expected_password)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setMaximumWidth(200)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_entry)

        # Crear los botones de inicio de sesión y regreso
        username_h_layout = QHBoxLayout()
        username_h_layout.addStretch()
        username_h_layout.addLayout(username_layout)
        username_h_layout.addStretch()

        password_h_layout = QHBoxLayout()
        password_h_layout.addStretch()
        password_h_layout.addLayout(password_layout)
        password_h_layout.addStretch()

        # Crear el botón de inicio de sesión
        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.login)
        self.btn_login.setStyleSheet("background-color: #FF5733; color: white; border: 2px solid #FF5733; border-radius: 5px; padding: 10px; font-size: 16px;")
        self.btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Crear el botón de regreso
        self.btn_back = QPushButton("Regresar")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setStyleSheet("background-color: #3498db; color: white; border: 2px solid #3498db; border-radius: 5px; padding: 10px; font-size: 16px;")
        self.btn_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


        # Crear la etiqueta de error
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 14px;")


        # Agregar los widgets al diseño del widget de inicio de sesión
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(username_h_layout)
        layout.addLayout(password_h_layout)
        layout.addWidget(self.btn_login, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Establecer el diseño del widget de inicio de sesión
        self.setLayout(layout)

    # Función para iniciar sesión
    def login(self):
        # Obtener el nombre de usuario y la contraseña ingresados
        entered_username = self.username_entry.text()
        entered_password = self.password_entry.text()

        # Verificar si el nombre de usuario y la contraseña están vacíos
        if entered_username == "" or entered_password == "":
            self.error_label.setText("Por favor, complete todos los campos.")
            return

        # Verificar si el nombre de usuario y la contraseña son correctos
        if entered_username == self.expected_username and entered_password == self.expected_password:
            QMessageBox.information(self, "Inicio de Sesión", f"Inicio de sesión exitoso. ¡Bienvenido, {entered_username}!")
        else:
            self.error_label.setText("Error de inicio de sesión. Nombre de usuario o contraseña incorrectos.")

    # Función para regresar a la ventana de selección de perfil
    def go_back(self):
        self.close()
        self.parent_window.restore_initial_state()
        self.parent_window.show()

# Clase del widget de perfil
class ProfileWidget(QWidget):
    # Inicializar el widget de perfil
    def __init__(self, profile_name, profile_image, parent, username, password):
        super().__init__()
        self.profile_name = profile_name
        self.profile_image = profile_image
        self.parent = parent
        self.username = username
        self.password = password

        # Configurar el diseño del widget de perfil
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)

        # Crear los widgets de la interfaz de perfil
        self.image_label = QLabel()
        pixmap = QPixmap(self.profile_image) 
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Crear la etiqueta del nombre del perfil
        self.name_label = QLabel(profile_name)
        self.name_label.setFont(QFont("Arial", 14))
        self.name_label.setStyleSheet("color: white") 

        # Crear el botón de selección de perfil
        self.btn_select = QPushButton("Seleccionar")
        self.btn_select.clicked.connect(self.select_profile)
        self.btn_select.setStyleSheet("QPushButton { background-color: #008CBA; color: white; border: none; padding: 10px; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #006699; }")

        # Agregar los widgets al diseño del widget de perfil
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_select, alignment=Qt.AlignmentFlag.AlignCenter)

        # Establecer el diseño del widget de perfil
        self.setLayout(layout)

    # Función para seleccionar el perfil
    def select_profile(self):
        self.parent.open_login_window(self.profile_name, self.username, self.password)
        self.parent.set_background_image(self.parent.profiles[self.profile_name]['background_image'])

# Función principal para ejecutar la aplicación
if __name__ == "__main__":
    # Cargar los perfiles de usuario desde el archivo JSON  
    def resource_path(relative_path):
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Cargar los perfiles de usuario desde el archivo JSON
    with open(resource_path('GarciaOS105/json/profiles.json'), 'r') as jsonfile:
        profiles = json.load(jsonfile)

    # Crear la aplicación y la ventana de selección de perfil
    app = QApplication(sys.argv)
    profile_window = ProfileSelectionWindow(profiles)
    profile_window.show()
    sys.exit(app.exec_())
