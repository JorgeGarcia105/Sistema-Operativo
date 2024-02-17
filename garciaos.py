# Importar la librería Kivy
import kivy

# Indicar la versión mínima de Kivy requerida
kivy.require('2.0.0')

# Importar la clase App
from kivy.app import App

# Importar el widget BoxLayout
from kivy.uix.boxlayout import BoxLayout

# Crear una clase que herede de App
class GarciaOSApp(App):

    # Definir el método build
    def build(self):

        # Crear un widget de tipo BoxLayout
        layout = BoxLayout()

        # Devolver el widget raíz
        return layout

# Crear una instancia de la clase
app = GarciaOSApp()

# Llamar al método run
app.run()
