import tkinter as tk
import time

class BIOSInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("BIOS Emulator")
        self.master.geometry("400x300")

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
            self.master.after(2000, self.login)

    def update_progress(self, message, progress):
        self.progress_bar.delete("progress")
        x = (progress / 10) * 300
        self.progress_bar.create_rectangle(0, 0, x, 20, fill="blue", outline="", tag="progress")
        self.progress_label.config(text=f"{message} al {progress*10}%")
        self.master.update_idletasks()

    def login(self):
        self.label.config(text="Iniciando sesión en GarciaOS")
        self.master.after(2000, self.welcome)

    def welcome(self):
        self.label.config(text="Bienvenido a GarciaOS")
        self.master.after(2000, self.thanks)

    def thanks(self):
        self.label.config(text="Gracias por usar GarciaOS")
        self.master.after(2000, self.master.destroy)

def main():
    root = tk.Tk()
    BIOSInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
