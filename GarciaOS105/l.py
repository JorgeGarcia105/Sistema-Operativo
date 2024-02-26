import tkinter as tk

class LoginInterface:
    def __init__(self, master):
        self.master = master

        self.users = {
            "Jorge": "jorge",
            "user": "user"
        }

        # Ocupar toda la pantalla  
        window_width = self.master.winfo_screenwidth()
        window_height = self.master.winfo_screenheight()

        # Crear un lienzo (Canvas) que cubra toda la ventana
        self.canvas = tk.Canvas(self.master, width=window_width, height=window_height, bg="blue")
        self.canvas.pack()

        # Agregar la imagen de fondo
        self.background_image = tk.PhotoImage(file="./GarciaOS105/images/login.png")
        # Ajustar la imagen a la pantalla
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Crear un marco para los elementos de login con forma redondeada 
        self.login_frame = tk.Frame(self.master, bg="blue", bd=5)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=350)

        # Elementos de login de usuario
        # Etiqueta para el usuario
        self.username_image = tk.PhotoImage(file="./GarciaOS105/images/loginboton.png")
        self.username_label = tk.Label(self.login_frame, text="Usuario", bg="blue" , font=("Arial", 12)) #cambiar el color de la letra
        self.username_label.pack()
        self.username = tk.Entry(self.login_frame)
        self.username.pack(pady=5)
        
        # mover etiqueta usarname 
        self.username_label.place(x=20, y=20)

        # Etiqueta para la contraseña
        self.password_label = tk.Label(self.login_frame, text="Contraseña")
        self.password_label.pack()
        self.password = tk.Entry(self.login_frame, show="*")
        self.password.pack(pady=5)

        # mover etiqueta contraseña
        self.password_label.place(x=100, y=125)
        
        self.login_button = tk.Button(self.login_frame, text="Iniciar sesión", bg="gray", fg="white", font=("Helvetica", 16), width=20, height=2, command=self.validate_login)
        self.login_button.pack(pady=5)
        self.login_button.pack()

        #mover boton de inicio de sesion
        self.login_button.place(x=80, y=250)

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

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    login_interface = LoginInterface(root)
    root.mainloop()
