import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

# Constantes
IMAGES_DIR = "./GarciaOS105/images/"
BACKGROUND_IMAGE_PATH = os.path.join(IMAGES_DIR, "fondo.png")
LOGO_IMAGE_PATH = os.path.join(IMAGES_DIR, "arranque.png")

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Logo
        self.logo_label = QLabel(self)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setScaledContents(True)

        # Establecer un tamaño máximo para el logotipo
        max_logo_width = 300
        max_logo_height = 300
        self.logo_label.setMaximumSize(max_logo_width, max_logo_height)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.login_function)

        # Selector de idioma
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Español", "Inglés"])

        # Botón de apagado/reinicio
        self.shutdown_button = QPushButton()
        self.shutdown_button.setIcon(QIcon(LOGO_IMAGE_PATH))

        # Diseño principal
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.logo_label, 0, 0, 1, 2)
        self.main_layout.addWidget(self.login_button, 1, 0)
        self.main_layout.addWidget(self.language_combo, 1, 1)
        self.main_layout.addWidget(self.shutdown_button, 2, 0, 1, 2)
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def set_logo(self, image_path):
        self.logo_label.setPixmap(QPixmap(image_path))

    def login_function(self):
        print("¡Inicio de sesión exitoso!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GarciaOS - Inicio de Sesión")
        self.setup_ui()

    def setup_ui(self):
        # Obtener resolución de pantalla
        screen_resolution = QApplication.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.setFixedSize(width, height)

        # Establecer imagen de fondo
        self.setStyleSheet(f"background-image: url({BACKGROUND_IMAGE_PATH});")
        # Expander imagen de fondo en todo la pantalla
        


        # Widget central
        self.login_widget = LoginWindow()
        self.login_widget.set_logo(LOGO_IMAGE_PATH)
        self.setCentralWidget(self.login_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
