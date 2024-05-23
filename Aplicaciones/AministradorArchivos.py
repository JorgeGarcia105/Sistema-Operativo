from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileSystemModel, QTreeView

class ExploradorArchivos(QWidget):
    def __init__(self):

        super().__init__()

        self.setWindowTitle("Explorador de Archivos")

        # Crear un modelo de sistema de archivos desde la ruta del proyecto D.
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # Crear un árbol de vista para mostrar el sistema de archivos
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.rootPath()))

        # Crear un layout vertical para el árbol de vista
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree_view)