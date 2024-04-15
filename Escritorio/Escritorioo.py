import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from Aplicaciones.calculadora import CalculatorApp
from Aplicaciones.BlockNotas import EditorTextoApp
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

class MiApp1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App 1")
        self.setGeometry(100, 100, 400, 300)
        self.setCentralWidget(QLabel("Contenido de la App 1"))

class MiApp4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App 4")
        self.setGeometry(100, 100, 400, 300)
        self.setCentralWidget(QLabel("Contenido de la App 4"))

class MiApp5(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App 5")
        self.setGeometry(100, 100, 400, 300)
        self.setCentralWidget(QLabel("Contenido de la App 5"))

class Escritorio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Escritorio Simulado")
        self.setGeometry(100, 100, 800, 500)

        # Configurar el fondo del escritorio
        self.fondo_escritorio = QLabel(self)
        pixmap = QPixmap("./Recursos/images/fondo.png")  # Ruta de la imagen de fondo
        self.fondo_escritorio.setPixmap(pixmap)
        self.fondo_escritorio.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Crear íconos de aplicaciones en la barra de tareas con barra centrada
        


        self.barra_tareas = QWidget()
        layout_barra_tareas = QHBoxLayout(self.barra_tareas)
        layout_barra_tareas.setSpacing(10)
        layout_barra_tareas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_barra_tareas.setContentsMargins(20, 0, 20, 0)
        btn_app1 = QPushButton("App 1", self)
        btn_app1.clicked.connect(self.abrir_app1)
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

        btn_app4 = QPushButton("App 4", self)
        btn_app4.clicked.connect(self.abrir_app4)
        layout_barra_tareas.addWidget(btn_app4)

        btn_app5 = QPushButton("App 5", self)
        btn_app5.clicked.connect(self.abrir_app5)
        layout_barra_tareas.addWidget(btn_app5)

        # Configurar el reloj
        self.reloj = QLabel("", self)
        self.reloj.setStyleSheet("font-size: 20px;")
        self.actualizar_reloj()
        layout_barra_tareas.addWidget(self.reloj)

        # Añadir el fondo del escritorio y la barra de tareas al layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.fondo_escritorio)
        layout.addWidget(self.barra_tareas)

        # Crear el widget central y asignar el layout
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

    def abrir_app1(self):
        self.app1 = MiApp1()
        self.app1.show()

    def abrir_app2(self):
        self.app2 = EditorTextoApp()
        self.app2.show()

    def abrir_app3(self):
        self.calculadora_app = CalculatorApp()
        self.calculadora_app.show()

    def abrir_app4(self):
        self.app4 = MiApp4()
        self.app4.show()

    def abrir_app5(self):
        self.app5 = MiApp5()
        self.app5.show()

def main():
    app = QApplication(sys.argv)
    escritorio = Escritorio()
    escritorio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
