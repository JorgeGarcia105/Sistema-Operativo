# Creacion de Ventana de navegador web

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Navegador(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Navegador")

        # Crear un widget de navegador web
        self.web_view = QWebEngineView()

        # Cargar una página web
        self.web_view.setUrl(QUrl("https://www.google.com"))

        # Crear un layout vertical para el widget de navegador web
        layout = QVBoxLayout(self)
        layout.addWidget(self.web_view)