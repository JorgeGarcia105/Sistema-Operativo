import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class GarciaOSApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text='Bienvenido a GarciaOS', font_size=32, color=(1, 1, 1, 1))
        layout.add_widget(label)

        button1 = Button(text='Iniciar sesión', font_size=20, background_color=(0.1, 0.4, 0.8, 1))
        button1.bind(on_press=self.login)
        layout.add_widget(button1)

        button2 = Button(text='Registrarse', font_size=20, background_color=(0.1, 0.8, 0.4, 1))
        button2.bind(on_press=self.register)
        layout.add_widget(button2)

        button3 = Button(text='Salir', font_size=20, background_color=(0.8, 0.1, 0.1, 1))
        button3.bind(on_press=self.exit)
        layout.add_widget(button3)

        return layout

    def login(self, instance):
        print("Iniciar sesión")

    def register(self, instance):
        print("Registrarse")

    def exit(self, instance):
        print("Salir")
        App.get_running_app().stop()

app = GarciaOSApp()
app.run()
