# Arranque del sistema operativo personalizado
# Este código simula el arranque de un sistema operativo personalizado con una barra de progreso y la posibilidad de acceder a la BIOS.
# El arranque se interrumpe con la tecla 'G' y se reinicia con la tecla 'R'.

import tkinter as tk
import tkinter.ttk as ttk
import threading
import time
from Bios import mostrar_bios

def main():
    root = tk.Tk()
    root.title("Sistema Operativo Personalizado")
    root.geometry("800x600")
    root.configure(bg="black")
    root.resizable(False, False)

    loading_label = tk.Label(root, text="Iniciando Sistema Operativo...", font=("Arial", 20), fg="white", bg="black")
    loading_label.pack(pady=20)

    progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
    progress_bar.pack(pady=10)
    progress_bar["maximum"] = 100

    style = ttk.Style()
    style.theme_use("classic")
    style.configure("TProgressbar", foreground="green", background="black")


    info_label = tk.Label(root, text="Presiona G para acceder a la BIOS.", font=("Arial", 12), fg="white", bg="black")
    info_label.pack(pady=10)

    # Bandera para indicar si la carga fue interrumpida
    carga_interrumpida = threading.Event()

    # Bandera para indicar si la carga fue reiniciada
    carga_reiniciada = threading.Event()

    # Función para simular la carga
    def cargar():
        nonlocal carga_interrumpida, carga_reiniciada
        for i in range(101):
            if carga_interrumpida.is_set():
                if carga_reiniciada.is_set():
                    carga_reiniciada.clear()  # Restablecer la señal de carga reiniciada
                    i = 0  # Reiniciar el contador de progreso
                    info_label.config(text="Carga reiniciada. Presiona G para acceder a la BIOS.")
                    carga_interrumpida.clear()  # Reiniciar la carga interrumpida
                else:
                    break  # Salir del bucle sin reiniciar la carga
            loading_label.config(text=f"Cargando GarciaOS..... {i}%")
            progress_bar["value"] = i
            root.update()
            time.sleep(0.05)  # Simulación de carga
        else:
            if not carga_interrumpida.is_set():  # Si la carga no fue interrumpida
                info_label.config(text="Carga completa. Presiona G para acceder a la BIOS.")
            else:
                info_label.config(text="Carga interrumpida. Presiona G para continuar o reiniciar.")

    # Iniciar la carga en un hilo separado
    carga_thread = threading.Thread(target=cargar)
    carga_thread.start()

    # Función para interrumpir la carga
    def interrumpir_carga(event):
        carga_interrumpida.set()
        mostrar_bios(root, carga_reiniciada)  # Pasar carga_reiniciada a la función mostrar_bios

    # Enlazar la función interrumpir_carga con la tecla 'G'
    root.bind("g", interrumpir_carga)

    # Función para reiniciar la carga
    def reiniciar_carga(event):
        carga_reiniciada.set()
        info_label.config(text="Reiniciando la carga...")
        root.update()

    # Enlazar la función reiniciar_carga con la tecla 'R'
    root.bind("r", reiniciar_carga)

    root.mainloop()

if __name__ == "__main__":
    main()
