from calendar import c
import sys
import os
import json
from PyQt5.QtWidgets import QApplication
from user_manager import UserManager
from loginPrueba import LoginWidget, ProfileSelectionWindow
from Escritorio import Escritorio
# conectar la base de datos

# Función para obtener la ruta del recurso, teniendo en cuenta el empaquetado con PyInstaller
def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Función principal que maneja la selección de perfiles
def profiles():
    user_manager = UserManager('./Recursos/json/users.json')

    # Cargar los perfiles de usuario desde el archivo JSON
    with open(resource_path('./Recursos/json/profiles.json'), 'r') as jsonfile:
        profiles = json.load(jsonfile)

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
