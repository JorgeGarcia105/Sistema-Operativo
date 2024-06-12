from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Youtube(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Youtube")

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

