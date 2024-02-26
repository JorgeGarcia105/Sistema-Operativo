from json import load
import tkinter as tk

class BIOSInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistemas Operativos GarciaOS")
        self.master.geometry("500x400")

        self.label = tk.Label(self.master, text="Bienvenido a GarciaOS", font=("Courier", 14))
        self.label.pack(pady=20)

        self.progress_label = tk.Label(self.master, text="", font=("Courier", 10))
        self.progress_label.pack()

        self.progress_bar = tk.Canvas(self.master, width=300, height=20, bg="white", borderwidth=1, relief="solid")
        self.progress_bar.pack(pady=10)

        self.progress = 0
        self.load_bios()


    def load_bios(self):
        self.update_progress("Cargando GarciaOS", self.progress)
        self.progress += 1
        if self.progress <= 10:
            self.master.after(1000, self.load_bios)
        elif self.progress == 11:
            self.progress_label.config(text="GarciaOS cargado al 100%")
            self.master.after(2000, self.login)  # Llama a la función login después de cargar el BIOS


    def update_progress(self, message, progress):
        self.progress_bar.delete("progress")
        x = (progress / 10) * 300
        self.progress_bar.create_rectangle(0, 0, x, 20, fill="blue", outline="", tag="progress")
        self.progress_label.config(text=f"{message} al {progress*10}%")
        self.master.update_idletasks()

    def login(self):
        self.label.config(text="Iniciando sesión en GarciaOS")

        # Creación de la ventana de login del usuario
        self.login_window = tk.Toplevel(self.master)
        self.login_window.title("Iniciar sesión")
        self.login_window.geometry("300x200")
        self.login_window.transient(self.master)
        self.login_window.grab_set()

        # Creación de usuario y contraseña
        self.users = {
            "admin": "admin",
            "user": "user"
        }
        self.username_label = tk.Label(self.login_window, text="Usuario")
        self.username_label.pack()
        self.username = tk.Entry(self.login_window)
        self.username.pack(pady=5)
        self.password_label = tk.Label(self.login_window, text="Contraseña")
        self.password_label.pack()
        self.password = tk.Entry(self.login_window, show="*")
        self.password.pack(pady=5)
        self.login_button = tk.Button(self.login_window, text="Iniciar sesión", command=self.validate_login)
        self.login_button.pack(pady=5)

    def validate_login(self):
        username = self.username.get()
        password = self.password.get()
        if username in self.users:
            if self.users[username] == password:
                self.label.config(text=f"Bienvenido {username}")
                self.master.after(2000, self.login_window.destroy)
            else:
                self.label.config(text="Contraseña incorrecta")
                self.master.after(2000, self.label.config(text="Iniciando sesión en GarciaOS"))
        else:
            self.label.config(text="Usuario no encontrado")
            self.master.after(2000, self.label.config(text="Iniciando sesión en GarciaOS"))

def main():
    root = tk.Tk()
    BIOSInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()