import tkinter as tk

class LoginInterface:
    def __init__(self, master):
        self.master = master

        self.users = {
            "Jorge": "jorge",
            "user": "user"
        }

        self.username_label = tk.Label(self.master, text="Usuario")
        self.username_label.pack()
        self.username = tk.Entry(self.master)
        self.username.pack(pady=5)

        self.password_label = tk.Label(self.master, text="Contraseña")
        self.password_label.pack()
        self.password = tk.Entry(self.master, show="*")
        self.password.pack(pady=5)

        self.login_button = tk.Button(self.master, text="Iniciar sesión", command=self.validate_login)
        self.login_button.pack(pady=5)

    def validate_login(self):
        username = self.username.get()
        password = self.password.get()
        if username in self.users:
            if self.users[username] == password:
                print(f"Bienvenido {username}")
                self.master.destroy()
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario no encontrado")