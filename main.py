import json
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from login import ProfileSelectionWindow
from Escritorio import Escritorio

def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def profiles():
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

def escritorio():
    app = QApplication(sys.argv)
    window = Escritorio()
    window.setWindowTitle("Escritorio")
    window.setGeometry(100, 100, 800, 500)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    profiles()
