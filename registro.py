import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from BaseDatos.database import conectar_db, insertar_usuario, connect_to_database, ejecutar_consulta

class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Usuario")

        self.layout = QVBoxLayout()  # type: ignore

        self.username_label = QLabel("Nombre de Usuario:")
        self.username_entry = QLineEdit()

        self.password_label = QLabel("Contraseña:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Registrar")
        self.register_button.clicked.connect(self.register)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_entry)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_entry)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout) # type: ignore

    def register(self):
        nombre_usuario = self.username_entry.text()
        contrasena = self.password_entry.text()

        # Conectar a la base de datos
        conexion = connect_to_database()

        # Verificar si la conexión fue exitosa
        if conexion:
            print("Conexión exitosa a la base de datos.")

            # Verificar si el usuario ya existe
            usuario_existente = False
            try:
                cursor = ejecutar_consulta(conexion, "SELECT COUNT(*) FROM perfiles WHERE nombre_usuario = %s", (nombre_usuario,))
                result = cursor.fetchone()
                if result and result[0] > 0:  # type: ignore
                    usuario_existente = True
            except Exception as e:
                print(f"Error al verificar usuario existente: {e}")
                QMessageBox.warning(self, "Error", "Error al verificar usuario existente.")

            if usuario_existente:
                QMessageBox.warning(self, "Error", "El nombre de usuario ya está en uso.")
            else:
                # Insertar el usuario en la base de datos
                try:
                    insertar_usuario(conexion, nombre_usuario, '', nombre_usuario, contrasena, '')
                    QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente")
                    self.close()
                except Exception as e:
                    print(f"Error al insertar usuario: {e}")
                    QMessageBox.warning(self, "Error", "Error al insertar usuario en la base de datos.")

            # Cerrar la conexión
            conexion.close()
            print("Conexión cerrada.")
            
        else:
            QMessageBox.warning(self, "Error", "Error al conectar a la base de datos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    registro_window = RegisterWindow()
    registro_window.show()
    sys.exit(app.exec_())
