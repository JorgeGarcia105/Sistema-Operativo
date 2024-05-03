import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
from math import sin, cos, sqrt, radians
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtWidgets import QTreeView

def Escritorio(Qwiget):
    def __init__(self):
        self.setWindowTitle("GarciaOS")
        #crear barra de tareas volatil
class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reproductor de Audio")

        layout = QVBoxLayout(self)

        self.player = QMediaPlayer()

        self.play_button = QPushButton("Reproducir")
        self.play_button.clicked.connect(self.play_audio)
        layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pausar")
        self.pause_button.clicked.connect(self.pause_audio)
        layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Detener")
        self.stop_button.clicked.connect(self.stop_audio)
        layout.addWidget(self.stop_button)

        self.select_button = QPushButton("Seleccionar Audio")
        self.select_button.clicked.connect(self.select_audio)
        layout.addWidget(self.select_button)

        # Inicialmente, el archivo de audio está vacío
        self.audio_file = ""

    def play_audio(self):
        if self.audio_file:
            media = QMediaContent(QUrl.fromLocalFile(self.audio_file))
            self.player.setMedia(media)
            self.player.play()

    def pause_audio(self):
        if self.player.state() == QMediaPlayer.media.PlayingState:
            self.player.pause()

    def stop_audio(self):
        self.player.stop()

    def select_audio(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo de audio
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Archivos de audio (*.mp3 *.wav)")
        file_dialog.selectFile(self.audio_file)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.audio_file = selected_files[0]

class VideoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video App")

        # Configura el diseño vertical
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Crea un componente QWebEngineView para mostrar el video
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

        # Conecta la señal loadFinished al método on_load_finished
        self.webview.loadFinished.connect(self.on_load_finished)

        # Carga el video inicial al iniciar la aplicación
        self.load_video("https://www.youtube.com/watch?v=127rJwowaAc")

    def load_video(self, video_url):
        # Carga la URL del video en el componente QWebEngineView
        self.webview.load(QUrl(video_url))

    def on_load_finished(self):
        # Ajusta el tamaño de la ventana según las dimensiones del iframe del video
        script = """
            var iframe = document.querySelector("iframe");
            if (iframe) {
                iframe.onload = function() {
                    var width = iframe.clientWidth;
                    var height = iframe.clientHeight;
                    window.pywebview.api.setSize(width, height);
                };
            }
        """
        self.webview.page().runJavaScript(script)
class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Científica")
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                font-size: 18px;
                padding: 5px;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                font-size: 18px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #d3d3d3;
            }
            QPushButton:pressed {
                background-color: #c6c6c6;
            }
        """)

        self.layout = self.QVBoxLayout()
        self.setLayout(self.layout)

        # Pantalla de la calculadora
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.layout.addWidget(self.result_display)

        # Crear botones para dígitos y operadores
        buttons_layout = QVBoxLayout()
        self.layout.addLayout(buttons_layout)

        buttons = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("0", ".", "=", "+")
        ]

        for row in buttons:
            row_layout = QHBoxLayout()
            for text in row:
                button = QPushButton(text)
                button.clicked.connect(lambda _, text=text: self.append_to_display(text))
                row_layout.addWidget(button)
            buttons_layout.addLayout(row_layout)

        # Botones de funciones científicas
        scientific_buttons_layout = QHBoxLayout()
        self.layout.addLayout(scientific_buttons_layout)

        scientific_buttons = [
            ("C", "sqrt", "^", "sin"),
            ("cos", "tan", "(", ")")
        ]

        for row in scientific_buttons:
            row_layout = QHBoxLayout()
            for text in row:
                button = QPushButton(text)
                button.clicked.connect(lambda _, text=text: self.append_to_display(text))
                row_layout.addWidget(button)
            scientific_buttons_layout.addLayout(row_layout)

    def append_to_display(self, text):
        current_text = self.result_display.text()
        if text == "=":
            try:
                result = self.evaluate_expression(current_text)
                self.result_display.setText(str(result))
            except Exception as e:
                self.result_display.setText("Error")
        elif text == "C":
            self.result_display.clear()
        else:
            new_text = current_text + text
            self.result_display.setText(new_text)

    def evaluate_expression(self, expression):
        expression = expression.replace("^", "**")
        expression = expression.replace("sqrt", "sqrt(")
        expression = expression.replace("sin", "sin(radians(")
        expression = expression.replace("cos", "cos(radians(")
        expression = expression.replace("tan", "tan(radians(")
        expression = expression.replace(")", "))")
        return eval(expression)
    
class FileManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Explorador de Archivos")
        layout = QVBoxLayout(self)

        # Etiqueta para el título del explorador de archivos
        title_label = QLabel("Explorador de Archivos")
        layout.addWidget(title_label)

        # Modelo del sistema de archivos
        self.model = QFileSystemModel()
        self.model.setRootPath(os.path.expanduser("~"))  # Establecer el directorio raíz como el directorio de inicio del usuario

        # Vista del árbol para mostrar la estructura de archivos y directorios
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.path.expanduser("~")))  # Establecer el índice raíz como el directorio de inicio del usuario
        layout.addWidget(self.tree_view)

        # Conectar la señal de clic de la vista del árbol para mostrar el directorio seleccionado
        self.tree_view.clicked.connect(self.on_tree_view_clicked)

    def on_tree_view_clicked(self, index):
        # Obtener la ruta del archivo o directorio seleccionado
        file_path = self.model.filePath(index)
        print("Selected File/Directory:", file_path)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GarciaOS")

        # Crear acciones para las diferentes aplicaciones
        audio_action = QAction("Audio", self)
        audio_action.triggered.connect(self.switch_audio_app)

        video_action = QAction("Video", self)
        video_action.triggered.connect(self.switch_video_app)

        calculator_action = QAction("Calculadora", self)
        calculator_action.triggered.connect(self.switch_calculator_app)

        file_manager_action = QAction("Explorador de Archivos", self)
        file_manager_action.triggered.connect(self.switch_file_manager_app)

        # Crear barra de menu

        self.setCentralWidget(QLabel("Bienvenido a GarciaOS"))

    def switch_audio_app(self):
        self.setCentralWidget(AudioApp())

    def switch_video_app(self):
        self.setCentralWidget(VideoApp())

    def switch_calculator_app(self):
        self.setCentralWidget(CalculatorApp())

    def switch_file_manager_app(self):
        self.setCentralWidget(FileManagerApp())

def main():
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
