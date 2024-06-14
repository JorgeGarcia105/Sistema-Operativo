import sys
import os
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from PyQt5.QtWidgets import QApplication
from login import ProfileSelectionWindow
from Arranque.load import BIOSInterface 
from Arranque.Bios import mostrar_bios

def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def round_image(image_path, corner_radius):
    img = Image.open(image_path).convert("RGBA")
    img = img.resize((400, 400))  # Cambiar el tamaño de la imagen
    circle = Image.new('L', (corner_radius * 2, corner_radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, corner_radius * 2, corner_radius * 2), fill=300)
    alpha = Image.new('L', img.size, 300)
    w, h = img.size
    alpha.paste(circle.crop((0, 0, corner_radius, corner_radius)), (0, 0))
    alpha.paste(circle.crop((0, corner_radius, corner_radius, corner_radius * 2)), (0, h - corner_radius))
    alpha.paste(circle.crop((corner_radius, 0, corner_radius * 2, corner_radius)), (w - corner_radius, 0))
    alpha.paste(circle.crop((corner_radius, corner_radius, corner_radius * 2, corner_radius * 2)), (w - corner_radius, h - corner_radius))
    img.putalpha(alpha)
    return img

def start_garciaos():
    root = tk.Tk()
    root.title("Sistema Operativo Personalizado")
    
    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular el tamaño de la ventana ajustado a la pantalla sin la barra de tareas
    window_width = screen_width - 50
    window_height = screen_height - 100  # Ajustar según sea necesario

    root.geometry(f"{window_width}x{window_height}+50+50")  # +50+50 para ajustar la posición de la ventana
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

    # Función para simular la carga
    def cargar(i=0):
        if i <= 100:
            loading_label.config(text=f"Cargando GarciaOS... {i}%")
            progress_bar["value"] = i
            i += 1
            root.after(50, cargar, i)  # Llamar recursivamente después de 50 ms
        else:
            info_label.config(text="Carga completa. Presiona G para acceder a la BIOS.")

    # Iniciar la carga
    cargar()

    # Función para interrumpir la carga
    def interrumpir_carga(event):
        info_label.config(text="Carga interrumpida. Presiona R para reiniciar.")
        root.update()  # Actualizar la interfaz gráfica

    # Enlazar la función interrumpir_carga con la tecla 'G'
    root.bind("g", interrumpir_carga)

    # Función para reiniciar la carga
    def reiniciar_carga(event):
        info_label.config(text="Reiniciando la carga...")
        root.update()  # Actualizar la interfaz gráfica
        cargar()  # Llamar la función de carga nuevamente

    # Enlazar la función reiniciar_carga con la tecla 'R'
    root.bind("r", reiniciar_carga)

    root.mainloop()

# Función para iniciar la interfaz de GarciaOS
def start_garciaos_interface():
    root = tk.Tk()
    root.title("Iniciando Sistemas Operativos GarciaOS")
    root.geometry("800x600")

    # Crear un marco negro alrededor de la imagen de fondo
    background_frame = tk.Frame(root, bg="black")
    background_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Redondear la imagen de fondo
    rounded_image = round_image("./Recursos/images/arranque.png", 100)  # Ajustar el radio según tu preferencia

    # Convertir la imagen redondeada para su uso en tkinter
    rounded_image_tk = ImageTk.PhotoImage(rounded_image)

    # Crear imagen de fondo dentro del marco negro
    background_label = tk.Label(background_frame, image=rounded_image_tk)
    background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Crear etiqueta de bienvenida
    label = tk.Label(root, text="Bienvenido a GarciaOS", font=("Courier", 14), fg="black", bg="white")
    label.pack(pady=200)
   
    BIOSInterface(root)

    root.mainloop()

# Función principal que maneja la selección de perfiles en PyQt5
def profiles():
    with open(resource_path('./Recursos/json/profiles.json'), 'r') as jsonfile:
        profiles = json.load(jsonfile)

    app = QApplication(sys.argv)
    profile_window = ProfileSelectionWindow(profiles)

    profile_window.show()
    sys.exit(app.exec_())

# Punto de entrada principal del programa
if __name__ == "__main__":
    start_garciaos()  # Ejecutar primero la simulación de carga del sistema operativo
    start_garciaos_interface()  # Luego mostrar la interfaz de GarciaOS
    profiles()  # Finalmente, mostrar la ventana de selección de perfiles en PyQt5
