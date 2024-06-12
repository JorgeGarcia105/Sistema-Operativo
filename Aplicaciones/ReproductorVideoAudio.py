import sys
import vlc
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QMainWindow, QAction, QStatusBar)
from PyQt5.QtCore import Qt, QDir

class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt VLC Player")

        # Crear una instancia de VLC
        self.instance = vlc.Instance()
        self.mediaPlayer = self.instance.media_player_new() # type: ignore

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay)) # type: ignore
        self.playButton.clicked.connect(self.play_pause)

        self.positionSlider = QSlider(Qt.Horizontal) # type: ignore
        self.positionSlider.setRange(0, 100)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        openAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open media')
        openAction.triggered.connect(self.openFile)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')# type: ignore
        fileMenu.addAction(openAction)# type: ignore
        fileMenu.addAction(exitAction)# type: ignore

        wid = QWidget(self)
        self.setCentralWidget(wid)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        wid.setLayout(layout)

        # Configurar la barra de estado
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Configurar el widget de video
        self.videoFrame = QWidget(self)
        self.videoFrame.setStyleSheet("background-color: black;")
        layout.insertWidget(0, self.videoFrame)

        self.mediaPlayer.set_hwnd(self.videoFrame.winId())

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Media", QDir.homePath(), "Media Files (*.mp3 *.mp4 *.avi *.mkv *.wav)")# type: ignore

        if fileName != '':
            self.mediaPlayer.set_media(self.instance.media_new(fileName))# type: ignore
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play_pause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))# type: ignore
        else:
            self.mediaPlayer.play()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))# type: ignore

    def setPosition(self, position):
        self.mediaPlayer.set_position(position / 100.0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
