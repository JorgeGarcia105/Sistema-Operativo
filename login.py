import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QDialog
from PyQt5.QtGui import QPixmap, QFont, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QCursor
from PyQt5.QtWidgets import QApplication
from registro import RegisterWindow
import mysql.connector
from BaseDatos.database import connect_to_database, close_connection, ejecutar_consulta
import tempfile

# Clase de la ventana de selección de perfil
# Clase de la ventana de selección de perfil
class ProfileSelectionWindow(QDialog):
    def __init__(self, profiles):
        super().__init__()
        self.profiles = profiles
        self.initial_background_image = "./Recursos/images/fondo.png"  # Guardar la imagen de fondo inicial
        self.initial_profiles = profiles.copy()  # Guardar los perfiles iniciales

        # Configurar la ventana principal
        self.setWindowTitle("Selección de Perfil")
        self.set_background_image()

        # Configurar el diseño de la ventana principal
        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        screen_geometry = QApplication.desktop().availableGeometry()  # type: ignore
        if screen_geometry.isValid():
            self.setGeometry(screen_geometry)

        self.populate_profile_widgets()
        self.create_profile_button()

    def restore_initial_state(self):
        self.set_background_image(self.initial_background_image)
        self.profiles = self.initial_profiles.copy()

        for i in reversed(range(self.main_layout.count())):
            widget_item = self.main_layout.itemAt(i)
            if widget_item:
                widget = widget_item.widget()
                if widget:
                    widget.deleteLater()

        self.populate_profile_widgets()

    def populate_profile_widgets(self):
        for profile_name, profile_data in self.profiles.items():
            profile_widget = ProfileWidget(profile_name, profile_data['image'], self, profile_data['username'], profile_data['password'])
            self.main_layout.addWidget(profile_widget)

    def create_profile_button(self):
        create_button = QPushButton("Crear Nuevo Perfil")
        create_button.clicked.connect(self.crear_registro)
        self.main_layout.addWidget(create_button)

    def crear_registro(self):
        registro_window = RegisterWindow()
        registro_window.register()

    def open_login_window(self, profile_name, username, password):
        self.restore_initial_state()
        self.login_widget = LoginWidget(profile_name, self.profiles[profile_name]['image'], username, password, self)

        for i in reversed(range(self.main_layout.count())):
            widget_item = self.main_layout.itemAt(i)
            if widget_item:
                widget = widget_item.widget()
                if widget:
                    widget.setVisible(False)

        self.main_layout.addWidget(self.login_widget)

    def set_background_image(self, image_path=None):
        if image_path is None:
            image_path = self.initial_background_image
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(image_path)))
        self.setPalette(palette)

class LoginWidget(QWidget):
    def __init__(self, profile_name, profile_image, username, password, parent_window):
        super().__init__()

        self.profile_name = profile_name
        self.profile_image = profile_image
        self.expected_username = username
        self.expected_password = password
        self.parent_window = parent_window

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 10, 20, 10)

        self.image_label = QLabel()
        pixmap = QPixmap(self.profile_image)
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_label = QLabel(profile_name)
        self.name_label.setFont(QFont("Arial", 14))

        username_layout = QVBoxLayout()
        self.username_label = QLabel("Nombre de Usuario:")
        self.username_entry = QLineEdit()
        self.username_entry.setText(self.expected_username)
        self.username_entry.setMaximumWidth(200)
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_entry)

        password_layout = QVBoxLayout()
        self.password_label = QLabel("Contraseña:")
        self.password_entry = QLineEdit()
        self.password_entry.setText(self.expected_password)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setMaximumWidth(200)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_entry)

        username_h_layout = QHBoxLayout()
        username_h_layout.addStretch()
        username_h_layout.addLayout(username_layout)
        username_h_layout.addStretch()

        password_h_layout = QHBoxLayout()
        password_h_layout.addStretch()
        password_h_layout.addLayout(password_layout)
        password_h_layout.addStretch()

        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.login)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #FF5733;
                color: white;
                border: 2px solid #FF5733;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
            QPushButton:pressed {
                background-color: #FF4500;
            }
        """)
        self.btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.btn_back = QPushButton("Regresar")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #006699;
            }
            QPushButton:pressed {
                background-color: #005577;
            }
        """)
        self.btn_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 14px;")

        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(username_h_layout)
        layout.addLayout(password_h_layout)
        layout.addWidget(self.btn_login, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    # Función para iniciar sesión
    def login(self):
       def login(self):
        # Obtener el nombre de usuario y la contraseña ingresados
        entered_username = self.username_entry.text()
        entered_password = self.password_entry.text()

        if entered_username == "" or entered_password == "":
            self.error_label.setText("Por favor, complete todos los campos.")
            return

        # Conectar a la base de datos
        conexion = connect_to_database()

        try:
            # Consulta SQL para buscar el usuario en la base de datos
            sql = "SELECT * FROM perfiles WHERE nombre_usuario = %s"
            cursor = ejecutar_consulta(conexion, sql, (entered_username,))
            result = cursor.fetchone()

            if result:
                if entered_password == result[4]:  # type: ignore # El índice 4 corresponde al campo de la contraseña en la tabla
                    QMessageBox.information(self, "Inicio de Sesión", f"Inicio de sesión exitoso. ¡Bienvenido, {entered_username}!")
                    self.parent_window.close()
                else:
                    self.error_label.setText("Error de inicio de sesión. Contraseña incorrecta.")
            else:
                self.error_label.setText("Error de inicio de sesión. Usuario no encontrado.")
        finally:
            close_connection(conexion)

    def go_back(self):
        self.close()
        self.parent_window.restore_initial_state()
        self.parent_window.show()

class ProfileWidget(QWidget):
    def __init__(self, profile_name, profile_image, parent, username, password):
        super().__init__()
        self.profile_name = profile_name
        self.profile_image = profile_image
        self.parent = parent
        self.username = username
        self.password = password

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)

        self.image_label = QLabel()
        pixmap = QPixmap(self.profile_image)
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_label = QLabel(profile_name)
        self.name_label.setFont(QFont("Arial", 14))
        self.name_label.setStyleSheet("color: white")

        self.btn_select = QPushButton("Seleccionar")
        self.btn_select.clicked.connect(self.select_profile)
        self.btn_select.setStyleSheet("QPushButton { background-color: #008CBA; color: white; border: none; padding: 10px; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #006699; }")

        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_select, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def select_profile(self):
        self.parent.open_login_window(self.profile_name, self.username, self.password)
        self.parent.set_background_image(self.parent.profiles[self.profile_name]['imagen_fondo'])

# Función principal para ejecutar la aplicación
def main():
    try:
        conexion = connect_to_database()
        profiles = obtener_perfiles_de_usuario(conexion)

        app = QApplication(sys.argv)
        profile_window = ProfileSelectionWindow(profiles)
        profile_window.show()
        sys.exit(app.exec_())

    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        QMessageBox.critical(None, "Error", "Error al conectar a la base de datos. Por favor, inténtalo de nuevo más tarde.")
    finally:
        if 'conexion' in locals():
            conexion.close()

def obtener_perfiles_de_usuario(conexion):
    cursor = conexion.cursor()
    sql = "SELECT * FROM perfiles"
    cursor.execute(sql)
    profiles = {}

    for profile_data in cursor.fetchall():
        profile_name = profile_data[1]
        profile_image_name = profile_data[2] 
        pofile_image_fondo = profile_data[5]
        profile_image_path = f"./Recursos/images/{profile_image_name}.png"  
        profile_image_fondo = f"./Recursos/images/{pofile_image_fondo}.png"
        if os.path.exists(profile_image_path):
            profiles[profile_name] = {
                'image': profile_image_path,
                'username': profile_data[3], 
                'password': profile_data[4], 
                'imagen_fondo': profile_image_fondo,
            }
        else:
            print(f"La imagen {profile_image_path} no existe.")
    return profiles

def save_image(image_data, image_path):
    with open(image_path, 'wb') as file:
        file.write(image_data)

def save_temp_image(image_data):
    # Verificar que los datos de la imagen están en formato binario
    if not isinstance(image_data, bytes):
        raise TypeError("a bytes-like object is required, not 'str'")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(image_data)
        return temp_file.name

if __name__ == "__main__":
    main()

