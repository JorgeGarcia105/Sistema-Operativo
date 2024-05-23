from math import log
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QDesktopWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
from Aplicaciones.calculadora import CalculatorApp
from Aplicaciones.BlockNotas import EditorTextoApp
from Aplicaciones.ReproductorVideo import VideoApp
from PyQt5.QtCore import Qt, QTimer

class Escritorio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Escritorio")

        # Ajustar la ventana para que ocupe toda la pantalla si es posible
        desktop = QDesktopWidget()
        screen_geometry = desktop.availableGeometry(desktop.primaryScreen())
        if screen_geometry.isValid():
            self.setGeometry(screen_geometry)
        
        # Configurar el fondo del escritorio
        self.fondo_escritorio = QLabel(self)
        pixmap = QPixmap("./Recursos/images/fondo.png")  # Ruta de la imagen de fondo
        self.fondo_escritorio.setPixmap(pixmap)
        self.fondo_escritorio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Configurar el layout principal 
        layout = QGridLayout()
        layout.addWidget(self.fondo_escritorio, 0, 0, 1, 2)  # Añadir el fondo del escritorio en la fila 0, columnas 0 y 1
        

        # Añadir la barra de tareas a la cuadrícula
        self.barra_tareas = QWidget()
        layout_barra_tareas = QHBoxLayout(self.barra_tareas)
        layout_barra_tareas.setSpacing(10)
        layout_barra_tareas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_barra_tareas.setContentsMargins(20, 0, 20, 0)

        btn_app1 = QPushButton("App 1", self)
        btn_app1.clicked.connect(self.abrir_Video)
        layout_barra_tareas.addWidget(btn_app1)

        btn_app2 = QPushButton("App 2", self)
        btn_app2.clicked.connect(self.abrir_app2)
        layout_barra_tareas.addWidget(btn_app2)

        # Botón de la calculadora con imagen estática
        btn_app3 = QPushButton(self)
        btn_app3.setFixedSize(64, 64)
        pixmap_calculadora = QPixmap("./Recursos/icon/calculadora.png")
        btn_app3.setIcon(QIcon(pixmap_calculadora))
        btn_app3.setIconSize(btn_app3.size())
        btn_app3.clicked.connect(self.abrir_app3)
        layout_barra_tareas.addWidget(btn_app3)
        

        # Configurar el reloj
        self.reloj = QLabel("", self)
        self.reloj.setStyleSheet("font-size: 20px;")
        self.actualizar_reloj()
        layout_barra_tareas.addWidget(self.reloj)

        layout.addWidget(self.barra_tareas, 1, 0, 1, 2)  # Añadir la barra de tareas en la fila 1, columnas 0 y 1

        # Establecer el layout principal en la ventana
        widget_central = QWidget(self)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

        # Actualizar el reloj cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_reloj)
        self.timer.start(1000)

    def actualizar_reloj(self):
        hora_actual = time.strftime("%H:%M:%S")
        self.reloj.setText(hora_actual)

    def abrir_Video(self):
        self.sesion = VideoApp()
        self.sesion.show()

    def abrir_app2(self):
        self.app2 = EditorTextoApp()
        self.app2.show()

    def abrir_app3(self):
        self.calculadora_app = CalculatorApp()
        self.calculadora_app.show()

def main():
    app = QApplication(sys.argv)
    escritorio = Escritorio()
    escritorio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
