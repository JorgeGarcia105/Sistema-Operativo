from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QMenu
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QIcon
import sys

class ExploradorArchivos(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Explorador de Archivos")
        self.setGeometry(300, 100, 800, 600)

        # Crear un modelo de sistema de archivos desde la ruta del proyecto D.
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # Crear un árbol de vista para mostrar el sistema de archivos
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree_view.setAnimated(False)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)

        # Configurar para expandir carpetas con doble clic
        self.tree_view.doubleClicked.connect(self.expand_folder)

        # Crear un layout vertical para el árbol de vista
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree_view)

    def expand_folder(self, index):
        if self.model.isDir(index):
            if self.tree_view.isExpanded(index):
                self.tree_view.collapse(index)
            else:
                self.tree_view.expand(index)
