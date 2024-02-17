# Importar la librería Kivy
import kivy

# Indicar la versión mínima de Kivy requerida
kivy.require('2.0.0')

# Importar la clase App
from kivy.app import App

# Importar el widget BoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# Crear una clase que herede de App
class GarciaOSApp(App):

    # Definir el método build
    def build(self):

        # Crear un widget de tipo BoxLayout con orientación vertical
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Agregar un Label al BoxLayout
        label = Label(text='Bienvenido a GarciaOS', font_size=32, color=(1, 1, 1, 1))
        layout.add_widget(label)

        # Agregar botones al BoxLayout
        login_button = Button(text='Iniciar sesión', font_size=24, background_color=(0, 0.5, 1, 1))
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

        register_button = Button(text='Registrarse', font_size=24, background_color=(0, 1, 0.5, 1))
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)

        exit_button = Button(text='Salir', font_size=24, background_color=(1, 0, 0, 1))
        exit_button.bind(on_press=self.exit)
        layout.add_widget(exit_button)

        # Devolver el widget raíz
        return layout

    # Métodos para manejar los eventos de los botones
    def login(self, instance):
        print("Iniciar sesión")

    def register(self, instance):
        print("Registrarse")

    def exit(self, instance):
        print("Salir")

# Crear una instancia de la clase
app = GarciaOSApp()

# Llamar al método run
app.run()
