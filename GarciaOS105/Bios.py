import tkinter as tk

def mostrar_bios(root, carga_reiniciada):
    bios_window = tk.Tk()
    bios_window.title("BIOS - Sistema Operativo GarciaOS")
    bios_window.geometry("400x300")
    bios_window.configure(bg="black")

    bios_label = tk.Label(bios_window, text="¡BIOS del Sistema Operativo GarciaOS!", font=("Arial", 20), fg="white", bg="black")
    bios_label.pack(pady=20)

    def cerrar_bios():
        bios_window.destroy()
        if carga_reiniciada.is_set():
            carga_reiniciada.clear()  # Restablecer la señal de carga reiniciada
