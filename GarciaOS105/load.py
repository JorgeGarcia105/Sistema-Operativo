import tkinter as tk
from login import LoginInterface

class BIOSInterface:
    # Clase que representa la interfaz de la BIOS
    def __init__(self, master):
        self.master = master

        self.progress_label = tk.Label(self.master, text="", font=("Courier", 10))
        self.progress_label.pack()

        self.progress_bar = tk.Canvas(self.master, width=300, height=20, bg="white", borderwidth=1, relief="solid")
        self.progress_bar.pack(pady=10)

        self.progress = 0

        self.load_bios()
    # Método que simula la carga de la BIOS
    def load_bios(self):
        self.update_progress("Cargando GarciaOS", self.progress)
        self.progress += 1
        if self.progress <= 10:
            self.master.after(1000, self.load_bios)
        elif self.progress == 11:
            self.progress_label.config(text="GarciaOS cargado al 100%")
            self.master.after(2000, self.load_login)

    # Método que actualiza el progreso de la carga
    def update_progress(self, message, progress):
        self.progress_bar.delete("progress")
        x = (progress / 10) * 300
        self.progress_bar.create_rectangle(0, 0, x, 20, fill="blue", outline="", tag="progress")
        self.progress_label.config(text=f"{message} al {progress*10}%")
        self.master.update_idletasks()

    # Método que carga la interfaz de login
    def load_login(self):
        self.progress_label.pack_forget()
        self.progress_bar.pack_forget()
        LoginInterface(self.master)
