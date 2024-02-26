import tkinter as tk

class LoginInterface:
    def __init__(self, master):
        self.master = master

        self.users = {
            "Jorge": "jorge",
            "user": "user"
        }

        #ocupar todo la pantalla  
        window_width = self.master.winfo_screenwidth()
        window_height = self.master.winfo_screenheight()

        # Crear un lienzo (Canvas) que cubra toda la ventana
        self.canvas = tk.Canvas(self.master, width=window_width, height=window_height, bg="white")
        self.canvas.pack()

        # Agregar la imagen de fondo
        self.background_image = tk.PhotoImage(file="./GarciaOS105/images/login.png")
        #ajustar la imagen a la pantalla
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Crear un marco para los elementos de login
        self.login_frame = tk.Frame(self.master, bg="white")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Elementos de login de usuario
        self.username_label = tk.Label(self.login_frame, text="Usuario")
        self.username_label.pack()
        self.username = tk.Entry(self.login_frame)
        self.username.pack(pady=5)

        self.password_label = tk.Label(self.login_frame, text="Contraseña")
        self.password_label.pack()
        self.password = tk.Entry(self.login_frame, show="*")
        self.password.pack(pady=5)

        self.login_button = tk.Button(self.login_frame, text="Iniciar sesión", command=self.validate_login)
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


