import sys
from PyQt5.QtWidgets import QApplication
from login import ProfileSelectionWindow
from Escritorio import Escritorio
from BaseDatos.database import obtener_perfiles_de_usuario

# Función principal que maneja la selección de perfiles
def profiles():
    # Obtener los perfiles de usuario desde la base de datos
    profiles = obtener_perfiles_de_usuario()

    # Crear la aplicación y la ventana de selección de perfil
    app = QApplication(sys.argv)
    profile_window = ProfileSelectionWindow(profiles)

    # Conectar la señal destroyed de la ventana de perfiles a la función escritorio
    profile_window.destroyed.connect(escritorio)

    profile_window.show()

    sys.exit(app.exec_())

# Función para mostrar el escritorio
def escritorio():
    # Crear la aplicación y la ventana de escritorio
    app = QApplication(sys.argv)
    window = Escritorio()
    window.show()
    sys.exit(app.exec_())

# Punto de entrada principal del programa
if __name__ == "__main__":
    profiles()
