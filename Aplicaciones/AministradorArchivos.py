import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
import mysql.connector
import os

# Aquí se define RUTA_BASE
RUTA_BASE = r"C:\Users\garci\OneDrive\Desktop\Uni\7 semestre\Sistemas Operativos\SistemaOperativo\Recursos\usuarios"

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

        # Diccionario para almacenar los ítems de lista por tipo de archivo
        self.lista_archivos_por_tipo = {
            'musica': QListWidget(),
            'videos': QListWidget(),
            'documentos': QListWidget(),
            'otros': QListWidget()
        }

        # Crear QListWidget para mostrar archivos del usuario por tipo
        for list_widget in self.lista_archivos_por_tipo.values():
            layout.addWidget(list_widget)

        # Botón para cargar archivos
        btn_cargar_archivos = QPushButton("Cargar Archivos")
        btn_cargar_archivos.setStyleSheet(button_style)
        btn_cargar_archivos.clicked.connect(self.cargar_archivos)
        layout.addWidget(btn_cargar_archivos)

        # Botón para agregar archivo
        btn_agregar_archivo = QPushButton("Agregar Archivo")
        btn_agregar_archivo.setStyleSheet(button_style)
        btn_agregar_archivo.clicked.connect(self.agregar_archivo)
        layout.addWidget(btn_agregar_archivo)

        # Botón para eliminar archivo
        btn_eliminar_archivo = QPushButton("Eliminar Archivo")
        btn_eliminar_archivo.setStyleSheet(button_style)
        btn_eliminar_archivo.clicked.connect(self.eliminar_archivo)
        layout.addWidget(btn_eliminar_archivo)

        # Establecer el layout principal en la ventana
        widget_central = QWidget(self)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

        # Cargar archivos del usuario desde la base de datos al iniciar
        self.cargar_archivos()

    def conectar_bd(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jorge1002671250',
                database='perfiles_usuarios'
            )
            return conexion
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return None

    def cargar_archivos(self):
        try:
            conexion = self.conectar_bd()
            if conexion:
                cursor = conexion.cursor()

                # Obtener el id del usuario que ha iniciado sesión
                cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (self.username,))
                usuario = cursor.fetchone()

                if usuario:
                    usuario_id = usuario[0]
                    self.mostrar_archivos_por_usuario(conexion, usuario_id)
                else:
                    print("Usuario no encontrado.")

                conexion.close()

        except mysql.connector.Error as err:
            print(f"Error al cargar archivos desde la base de datos: {err}")

    def mostrar_archivos_por_usuario(self, conexion, usuario_id):
        try:
            cursor = conexion.cursor(dictionary=True)

            # Obtener archivos asociados a las carpetas del usuario, agrupados por tipo
            sql = """
                SELECT nombre_archivo, ruta_archivo
                FROM archivos
                WHERE carpeta_id IN (
                    SELECT id
                    FROM carpetas
                    WHERE usuario_id = %s
                )
            """
            cursor.execute(sql, (usuario_id,))
            archivos = cursor.fetchall()

            if archivos:
                # Limpiar las listas antes de agregar nuevos elementos
                for list_widget in self.lista_archivos_por_tipo.values():
                    list_widget.clear()

                for archivo in archivos:
                    nombre_archivo = archivo['nombre_archivo']
                    ruta_archivo = archivo['ruta_archivo']

                    tipo_archivo = self.obtener_tipo_archivo(nombre_archivo)

                    # Añadir a la lista correspondiente según el tipo de archivo
                    if tipo_archivo in self.lista_archivos_por_tipo:
                        list_widget = self.lista_archivos_por_tipo[tipo_archivo]
                        item = QListWidgetItem(f"Nombre: {nombre_archivo}")
                        item.setData(Qt.UserRole, ruta_archivo)
                        list_widget.addItem(item)

                        list_widget.itemDoubleClicked.connect(self.abrir_archivo)

            else:
                print("No se encontraron archivos para este usuario.")

        except mysql.connector.Error as err:
            print(f"Error al obtener archivos del usuario: {err}")

    def obtener_tipo_archivo(self, nombre_archivo):
        # Función para determinar el tipo de archivo basado en su extensión
        extension = os.path.splitext(nombre_archivo)[1].lower()
        if extension in ('.mp3', '.wav', '.flac'):
            return 'musica'
        elif extension in ('.mp4', '.avi', '.mkv'):
            return 'videos'
        elif extension in ('.doc', '.docx', '.pdf'):
            return 'documentos'
        else:
            return 'otros'

    def agregar_archivo(self):
        try:
            file_dialog = QFileDialog()
            archivo_seleccionado, _ = file_dialog.getOpenFileName(self, "Seleccionar Archivo")
            
            if archivo_seleccionado:
                nombre_archivo = os.path.basename(archivo_seleccionado)
                tipo_archivo = self.obtener_tipo_archivo(nombre_archivo)
                ruta_archivo = os.path.relpath(archivo_seleccionado, RUTA_BASE)

                conexion = self.conectar_bd()
                if conexion:
                    cursor = conexion.cursor()

                    # Obtener el id de la carpeta predeterminada del usuario (ejemplo)
                    cursor.execute("SELECT id FROM carpetas WHERE nombre = 'videos' AND usuario_id = %s", (1,))
                    carpeta_id = cursor.fetchone()

                    if carpeta_id:
                        sql = "INSERT INTO archivos (nombre_archivo, ruta_archivo, carpeta_id) VALUES (%s, %s, %s)"
                        val = (nombre_archivo, ruta_archivo, carpeta_id[0])
                        cursor.execute(sql, val)
                        conexion.commit()
                        print("Archivo agregado correctamente.")

                        # Actualizar la lista de archivos después de agregar uno nuevo
                        self.mostrar_archivos_por_usuario(conexion, 1)
                    else:
                        print("Carpeta no encontrada para el usuario.")

                    conexion.close()

        except mysql.connector.Error as err:
            print(f"Error al agregar archivo a la base de datos: {err}")

    def eliminar_archivo(self):
        # Obtener el QListWidget activo
        list_widget = None
        for tipo, lw in self.lista_archivos_por_tipo.items():
            if lw.hasFocus():
                list_widget = lw
                break
        
        if list_widget is None:
            print("No se ha seleccionado ningún archivo para eliminar.")
            return

        # Obtener el item seleccionado
        selected_item = list_widget.currentItem()
        if not selected_item:
            print("No se ha seleccionado ningún archivo para eliminar.")
            return

        # Obtener datos del item (id_archivo, ruta_archivo)
        id_archivo, ruta_archivo = selected_item.data(Qt.UserRole)
        
        # Confirmar eliminación con el usuario
        confirmacion = QMessageBox.question(self, "Confirmar Eliminación",
                                            f"¿Estás seguro que deseas eliminar el archivo '{ruta_archivo}'?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmacion == QMessageBox.Yes:
            try:
                conexion = self.conectar_bd()
                if conexion:
                    cursor = conexion.cursor()

                    # Eliminar el archivo de la base de datos
                    sql = "DELETE FROM archivos WHERE id = %s"
                    cursor.execute(sql, (id_archivo,))
                    conexion.commit()

                    # Eliminar físicamente el archivo del sistema (opcional)
                    # if os.path.exists(ruta_archivo):
                    #     os.remove(ruta_archivo)

                    # Actualizar la lista de archivos después de eliminar
                    self.cargar_archivos()
                    
                    print(f"Archivo '{ruta_archivo}' eliminado correctamente.")

                else:
                    print("No se pudo conectar a la base de datos para eliminar el archivo.")

            except mysql.connector.Error as err:
                print(f"Error al eliminar el archivo: {err}")

            finally:
                if conexion:
                    conexion.close()

        else:
            print("Eliminación cancelada por el usuario.")

    def abrir_archivo(self, item):
        ruta_archivo_relativa = item.data(Qt.UserRole)
        ruta_completa = os.path.join(RUTA_BASE, ruta_archivo_relativa)
        if os.path.exists(ruta_completa):
            QDesktopServices.openUrl(QUrl.fromLocalFile(ruta_completa))
        else:
            print(f"Archivo no encontrado en la ruta: {ruta_completa}")

        def closeEvent(self, event):
            confirmación = QMessageBox.question(self, "Confirmar Salida",
                                                "¿Estás seguro que deseas salir?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmación == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


def main(username, password):
    app = QApplication(sys.argv)
    escritorio = Archivos(username, password)
    escritorio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Asumiendo que el nombre de usuario y contraseña se proporcionan al iniciar la aplicación
    username = "root"  # Reemplazar con tu nombre de usuario de MySQL
    password = "Jorge1002671250"  # Reemplazar con tu contraseña de MySQL

    main(username, password)
