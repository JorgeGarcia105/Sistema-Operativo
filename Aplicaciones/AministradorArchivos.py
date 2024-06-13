import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
import mysql.connector

# Estilo para los botones de la barra de tareas
button_style = """
    QPushButton {
        background-color: #FFFFFF;
        color: #000000;
        border: none;
        padding: 10px;
        font-size: 14px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #E0E0E0;
    }
    QPushButton:pressed {
        background-color: #C0C0C0;
    }
"""

class Archivos(QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        self.username = username

        self.setWindowTitle(f"Escritorio - {username}")

        # Configurar el layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Crear QListWidget para mostrar archivos del usuario
        self.lista_archivos = QListWidget()
        layout.addWidget(self.lista_archivos)

        # Conectar botón de archivos de usuario a función correspondiente
        btn_archivos_usuario = QPushButton("Cargar Archivos")
        btn_archivos_usuario.setStyleSheet(button_style)
        btn_archivos_usuario.clicked.connect(self.cargar_archivos)
        layout.addWidget(btn_archivos_usuario)

        # Establecer el layout principal en la ventana
        widget_central = QWidget(self)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

        # Cargar archivos del usuario desde la base de datos al iniciar
        self.cargar_archivos()

    def cargar_archivos(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jorge1002671250',
                database='perfiles_usuarios'
            )
            cursor = conexion.cursor()

            # Obtener el id del usuario que ha iniciado sesión
            cursor.execute("SELECT id_perfil FROM perfiles WHERE nombre_usuario = %s", (self.username,))
            usuario = cursor.fetchone()

            if usuario:
                perfil_id = usuario[0] # type: ignore
                self.mostrar_archivos_por_perfil(conexion, perfil_id)
            else:
                print("Usuario no encontrado.")
            
            conexion.close()

        except mysql.connector.Error as err:
            print(f"Error al cargar archivos desde la base de datos: {err}")

    def mostrar_archivos_por_perfil(self, conexion, perfil_id):
        try:
            cursor = conexion.cursor()
            sql = "SELECT nombre_archivo, tipo_archivo, ubicacion_archivo FROM archivos WHERE id_perfil = %s"
            cursor.execute(sql, (perfil_id,))
            archivos = cursor.fetchall()  # obtener todos los archivos

            if archivos:
                self.lista_archivos.clear()  # Limpiar la lista antes de agregar nuevos elementos
                for archivo in archivos:
                    nombre_archivo, tipo_archivo, ubicacion_archivo = archivo
                    item = QListWidgetItem(f"Nombre: {nombre_archivo}, Tipo: {tipo_archivo}")
                    item.setData(Qt.UserRole, ubicacion_archivo)  # type: ignore # Almacenar la ubicación del archivo como data del item
                    self.lista_archivos.addItem(item)

                self.lista_archivos.itemDoubleClicked.connect(self.abrir_archivo)
            else:
                print("No se encontraron archivos para este perfil.")

        except mysql.connector.Error as err:
            print(f"Error al obtener archivos del perfil: {err}")

    def abrir_archivo(self, item):
        ubicacion_archivo = item.data(Qt.UserRole) # type: ignore
        QDesktopServices.openUrl(QUrl.fromLocalFile(ubicacion_archivo))

def main(username, password):
    app = QApplication(sys.argv)
    escritorio = Archivos(username, password)
    escritorio.show()
    sys.exit(app.exec_())
