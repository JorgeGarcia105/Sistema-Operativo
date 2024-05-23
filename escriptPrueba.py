import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QDesktopWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QBrush

class Escritorio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Escritorio")

        # Ajustar la ventana para que ocupe toda la pantalla
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

        layout.addWidget(self.barra_tareas, 1, 0, 1, 2)  # Añadir la barra de tareas en la fila 1, columnas 0 y 1

        # Establecer el layout principal en la ventana
        widget_central = QWidget(self)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

        # barra de tareas negra y por encima de la imagen de fondo
        self.barra_tareas.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Background, Qt.GlobalColor.black)
        self.barra_tareas.setPalette(palette)

def main():
    app = QApplication(sys.argv)
    escritorio = Escritorio()
    escritorio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
