import tkinter as tk
import tkinter.ttk as ttk
import threading
import time
from Bios import mostrar_bios
import sys
import os
from PIL import Image, ImageDraw

# Función para obtener la ruta del recurso, teniendo en cuenta el empaquetado con PyInstaller
def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Función para redondear imágenes
def round_image(image_path, corner_radius):
    img = Image.open(image_path).convert("RGBA")
    img = img.resize((400, 400))  # Cambiar el tamaño de la imagen
    circle = Image.new('L', (corner_radius * 2, corner_radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, corner_radius * 2, corner_radius * 2), fill=255)
    alpha = Image.new('L', img.size, 0)
    w, h = img.size
    alpha.paste(circle.crop((0, 0, corner_radius, corner_radius)), (0, 0))
    alpha.paste(circle.crop((0, corner_radius, corner_radius, corner_radius * 2)), (0, h - corner_radius))
    alpha.paste(circle.crop((corner_radius, 0, corner_radius * 2, corner_radius)), (w - corner_radius, 0))
    alpha.paste(circle.crop((corner_radius, corner_radius, corner_radius * 2, corner_radius * 2)), (w - corner_radius, h - corner_radius))
    img.putalpha(alpha)
    return img

# Función principal de la simulación de arranque del sistema operativo personalizado
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

    carga_interrumpida = threading.Event()
    carga_reiniciada = threading.Event()

    def cargar():
        nonlocal carga_interrumpida, carga_reiniciada
        for i in range(101):
            if carga_interrumpida.is_set():
                if carga_reiniciada.is_set():
                    carga_reiniciada.clear()
                    i = 0
                    info_label.config(text="Carga reiniciada. Presiona G para acceder a la BIOS.")
                    carga_interrumpida.clear()
                else:
                    break
            loading_label.config(text=f"Cargando GarciaOS... {i}%")
            progress_bar["value"] = i
            root.update()
            time.sleep(0.05)
        else:
            if not carga_interrumpida.is_set():
                info_label.config(text="Carga completa. Presiona G para acceder a la BIOS.")
                time.sleep(1)
                root.destroy()
                sys.exit()

    carga_thread = threading.Thread(target=cargar)
    carga_thread.start()

    def interrumpir_carga(event):
        carga_interrumpida.set()
        mostrar_bios(root, carga_reiniciada)

    root.bind("g", interrumpir_carga)

    def reiniciar_carga(event):
        carga_reiniciada.set()
        info_label.config(text="Reiniciando la carga...")
        root.update()

    root.bind("r", reiniciar_carga)

    root.mainloop()

# Punto de entrada principal del programa
if __name__ == "__main__":
    main()
