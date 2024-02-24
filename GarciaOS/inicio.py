import tkinter as tk

class BIOSInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Iniciando Sistemas Operativos GarciaOS")
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

        # Destruir widgets de carga de BIOS
        self.label.pack_forget()
        self.progress_label.pack_forget()
        self.progress_bar.pack_forget()

        # Crear widgets de inicio de sesión
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
        if username == "admin" and password == "admin":
            self.label.config(text=f"Bienvenido {username}")
        else:
            self.label.config(text="Usuario o contraseña incorrectos")

def main():
    root = tk.Tk()
    BIOSInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
