import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        self.add_widget(Label(text='Inicio de Sesión', font_size=32))
        
        self.username_input = TextInput(hint_text='Nombre de Usuario', multiline=False)
        self.add_widget(self.username_input)

        self.password_input = TextInput(hint_text='Contraseña', multiline=False, password=True)
        self.add_widget(self.password_input)

        self.error_label = Label(text='', color=(1, 0, 0, 1))
        self.add_widget(self.error_label)

        self.login_button = Button(text='Iniciar Sesión', size_hint=(None, None), size=(200, 50), font_size=20)
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if username == 'usuario' and password == 'contraseña':
            self.error_label.text = 'Inicio de sesión exitoso'
            # Aquí podrías añadir la lógica para iniciar sesión en el sistema operativo
        else:
            self.error_label.text = 'Nombre de usuario o contraseña incorrectos'

class GarciaOSApp(App):
    def build(self):
        login_screen = LoginScreen()
        return login_screen

if __name__ == '__main__':
    GarciaOSApp().run()
