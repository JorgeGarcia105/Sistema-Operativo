#creacion de interfaz de usuario de nuestro sistema operativo
import tkinter as tk
import os
import shutil
import time

# Definir la ventana principal
root = tk.Tk()
root.title("Sistema Operativo")

# Agregar widgets (botones, etiquetas, etc.) a la ventana
# Crear un widget de etiqueta
label = tk.Label(root, text="Bienvenido al sistema operativo")
label.pack()

# Crear un widget de botón
button = tk.Button(root, text="Crear carpeta", command=lambda: os.mkdir("Carpeta"))
button.pack()

# Crear un widget de botón
button = tk.Button(root, text="Eliminar carpeta", command=lambda: os.rmdir("Carpeta"))
button.pack()

# Crear un widget de botón
button = tk.Button(root, text="Copiar archivo", command=lambda: shutil.copy("archivo.txt", "archivo_copia.txt"))
button.pack()

# Crear un widget de botón
button = tk.Button(root, text="Mover archivo", command=lambda: shutil.move("archivo.txt", "Carpeta/archivo.txt"))
button.pack()

# Crear un widget de botón
button = tk.Button(root, text="Renombrar archivo", command=lambda: os.rename("archivo.txt", "archivo_nuevo.txt"))
button.pack()

# Crear un widget de botón
button = tk.Button(root, text="Eliminar archivo", command=lambda: os.remove("archivo.txt"))
button.pack()

# Crear un widget de botón
button = tk.Button(root, text="Mostrar contenido", command=lambda: os.listdir("."))
button.pack()

# Crear un widget de botón
button = tk.Button(root, text="Mostrar fecha y hora", command=lambda: time.ctime())
button.pack()

# Definir funciones para manejar eventos

# Iniciar el bucle principal de la interfaz de usuario
root.mainloop()

