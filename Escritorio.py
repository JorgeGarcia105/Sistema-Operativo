import time
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer
import pygame
import mysql.connector
from Aplicaciones.calculadora import CalculatorApp
from Aplicaciones.BlockNotas import EditorTextoApp
from Aplicaciones.ReproductorVideoAudio import VideoWindow as VideoApp
from Aplicaciones.Youtube import Youtube
from Aplicaciones.AministradorArchivos import Archivos
from Aplicaciones.Navegador import Navegador
from Aplicaciones.juego import ALTO, ANCHO, JuegoAhorcado 

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

# Conectar a la base de datos
def connect_to_database():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jorge1002671250',
            database='perfiles_usuarios'
        )
        return conexion
    except mysql.connector.Error as err:
        QMessageBox.critical(None, "Error de conexión", f"Error al conectar a la base de datos: {err}")
        return None

# Obtener archivos por perfil
def obtener_archivos_por_perfil(conexion, perfil_id):
    try:
        cursor = conexion.cursor()
        sql = "SELECT nombre_archivo FROM archivos WHERE perfil_id = %s"
        cursor.execute(sql, (perfil_id,))
        archivos = [archivo[0] for archivo in cursor.fetchall()]  # Obtener todos los nombres de archivos
        return archivos
    except mysql.connector.Error as err:
        QMessageBox.critical(None, "Error de consulta", f"Error al obtener archivos del perfil: {err}")
        return []

class Escritorio(QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

        self.setWindowTitle("Escritorio - {}".format(username))
        self.setObjectName("mainWindow")
        
        # Configurar el fondo del escritorio
        self.set_background_image()

        # Configurar el layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Ajustar la ventana para que ocupe toda la pantalla
        self.setGeometry(QDesktopWidget().availableGeometry())
        self.showMaximized()

        # Crear un nuevo QVBoxLayout para el layout de la parte superior izquierda
        layout_superior_izquierda = QVBoxLayout()

        # Agregar botón para la papelera
        btn_papelera = QPushButton(self)
        btn_papelera.setFixedSize(80, 80)
        pixmap_papelera = QPixmap("./Recursos/icon/papelera.png")
        btn_papelera.setIcon(QIcon(pixmap_papelera))
        btn_papelera.setIconSize(btn_papelera.size())
        btn_papelera.setStyleSheet(button_style)
        # Conectar el botón a la función correspondiente
        # btn_papelera.clicked.connect(self.abrir_Papelera)
        layout_superior_izquierda.addWidget(btn_papelera)

        # Agregar botón para los archivos de usuario
        btn_archivos_usuario = QPushButton(self)
        btn_archivos_usuario.setFixedSize(80, 80)
        pixmap_archivos_usuario = QPixmap("./Recursos/icon/usuario.png")
        btn_archivos_usuario.setIcon(QIcon(pixmap_archivos_usuario))
        btn_archivos_usuario.setIconSize(btn_archivos_usuario.size())
        btn_archivos_usuario.setStyleSheet(button_style)
        # Conectar el botón a la función correspondiente
        # btn_archivos_usuario.clicked.connect(self.abrir_ArchivosUsuario)
        layout_superior_izquierda.addWidget(btn_archivos_usuario)

        # Añadir el layout de la parte superior izquierda al layout principal
        layout.addLayout(layout_superior_izquierda)

        # Añadir la barra de tareas a un widget horizontal
        self.barra_tareas = QWidget()
        self.barra_tareas.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 10px;
        """)
        
        layout_barra_tareas = QHBoxLayout(self.barra_tareas)
        layout_barra_tareas.setSpacing(20)
        layout_barra_tareas.setContentsMargins(20, 10, 20, 10)

        layout_barra_tareas.addStretch()  # Espacio flexible a la izquierda

        # Botones para las aplicaciones
        btn_youtube = QPushButton(self)
        btn_youtube.setFixedSize(80, 80)
        pixmap_youtube = QPixmap("./Recursos/icon/youtube.png")
        btn_youtube.setIcon(QIcon(pixmap_youtube))
        btn_youtube.setIconSize(btn_youtube.size())
        btn_youtube.clicked.connect(self.abrir_Youtube)
        btn_youtube.setStyleSheet(button_style)
        layout_barra_tareas.addWidget(btn_youtube)

        btn_editorText = QPushButton(self)
        btn_editorText.setFixedSize(80, 80)
        pixmap_editorText = QPixmap("./Recursos/icon/portapapeles.png")
        btn_editorText.setIcon(QIcon(pixmap_editorText))
        btn_editorText.setIconSize(btn_editorText.size())
        btn_editorText.clicked.connect(self.abrir_Text)
        btn_editorText.setStyleSheet(button_style)
        layout_barra_tareas.addWidget(btn_editorText)

        btn_calculadora = QPushButton(self)
        btn_calculadora.setFixedSize(80, 80)
        pixmap_calculadora = QPixmap("./Recursos/icon/calculadora.png")
        btn_calculadora.setIcon(QIcon(pixmap_calculadora))
        btn_calculadora.setIconSize(btn_calculadora.size())
        btn_calculadora.clicked.connect(self.abrir_Calculadora)
        btn_calculadora.setStyleSheet(button_style)
        layout_barra_tareas.addWidget(btn_calculadora)

        btn_reproductor = QPushButton(self)
        btn_reproductor.setFixedSize(80, 80)
        pixmap_reproductor = QPixmap("./Recursos/icon/reproductor.png")
        btn_reproductor.setIcon(QIcon(pixmap_reproductor))
        btn_reproductor.setIconSize(btn_reproductor.size())
        btn_reproductor.clicked.connect(self.reproductor)
        btn_reproductor.setStyleSheet(button_style)
        layout_barra_tareas.addWidget(btn_reproductor)

        btn_explorador = QPushButton(self)
        btn_explorador.setFixedSize(80, 80)
        pixmap_explorador = QPixmap("./Recursos/icon/explorador.png")
        btn_explorador.setIcon(QIcon(pixmap_explorador))
        btn_explorador.setIconSize(btn_explorador.size())
        btn_explorador.clicked.connect(self.abrir_Explorador)
        btn_explorador.setStyleSheet(button_style)
        layout_barra_tareas.addWidget(btn_explorador)

        btn_navegador = QPushButton(self)
        btn_navegador.setFixedSize(80, 80)
        pixmap_navegador = QPixmap("./Recursos/icon/navegador.png")
        btn_navegador.setIcon(QIcon(pixmap_navegador))
        btn_navegador.setIconSize(btn_navegador.size())
        btn_navegador.clicked.connect(self.abrir_Navegador)
        btn_navegador.setStyleSheet(button_style)
        layout_barra_tareas.addWidget(btn_navegador)

        btn_juego = QPushButton(self)
        btn_juego.setFixedSize(80, 80)
        pixmap_juego = QPixmap("./Recursos/icon/juego.png")
        btn_juego.setIcon(QIcon(pixmap_juego))
        btn_juego.setIconSize(btn_juego.size())
        btn_juego.clicked.connect(self.abrir_Juego)
        btn_juego.setStyleSheet(button_style)
        layout_barra_tareas.addWidget(btn_juego)

        layout_barra_tareas.addStretch()  # Espacio flexible a la derecha

        self.reloj = QLabel("", self)
        self.reloj.setStyleSheet("font-size: 20px; color: #FFFFFF;")  # Color blanco para el reloj
        self.actualizar_reloj()
        layout_barra_tareas.addWidget(self.reloj, alignment=Qt.AlignmentFlag.AlignRight)  # Colocar el reloj en la parte inferior derecha

        layout.addWidget(self.barra_tareas)
        layout.setAlignment(self.barra_tareas, Qt.AlignmentFlag.AlignBottom)  # Colocar la barra de tareas en la parte inferior

        # Establecer el layout principal en la ventana
        widget_central = QWidget(self)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

        # Actualizar el reloj cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_reloj)
        self.timer.start(1000)

    def set_background_image(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jorge1002671250',
                database='perfiles_usuarios'
            )
            cursor = conexion.cursor()

            # Obtener la ruta de la imagen de fondo del usuario que ha iniciado sesión
            cursor.execute("SELECT imagen_fondo FROM perfiles WHERE nombre_usuario = %s", (self.username,))
            resultado = cursor.fetchone()

            if resultado and resultado[0]: # type: ignore
                fondo_imagen = resultado[0] # type: ignore
                print(f"Ruta de la imagen de fondo: {fondo_imagen}")  # Debugging: Verificar la ruta de la imagen

                pixmap = QPixmap(fondo_imagen)
                if not pixmap.isNull():
                    palette = QPalette()
                    palette.setBrush(QPalette.Background, QBrush(pixmap))
                    self.setPalette(palette)
                    print("Imagen de fondo cargada correctamente.")
                else:
                    print("La imagen de fondo no se pudo cargar.")
            else:
                print("No se encontró una imagen de fondo para este usuario.")

            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error MySQL: {err}")
        except Exception as ex:
            print(f"Error general: {ex}")


    def actualizar_reloj(self):
        hora_actual = time.strftime("%H:%M:%S")
        self.reloj.setText(hora_actual)

    def abrir_Youtube(self):
        self.sesion = Youtube()
        self.sesion.show()

    def abrir_Text(self):
        self.app2 = EditorTextoApp()
        self.app2.show()

    def abrir_Calculadora(self):
        self.calculadora_app = CalculatorApp()
        self.calculadora_app.show()

    def reproductor(self):
        self.video_app = VideoApp()
        self.video_app.show()

    def abrir_Explorador(self):
        self.explorador_app = Archivos(self.username, self.password)
        self.explorador_app.show()

    def abrir_Navegador(self):
        self.navegador_app = Navegador()
        self.navegador_app.show()

    def abrir_Juego(self):
        pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crear la pantalla de Pygame
        self.juego_app = JuegoAhorcado(pantalla)  # Pasar la pantalla como argumento
        self.juego_app.show()


