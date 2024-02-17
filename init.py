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

# Función para manejar el evento de hacer clic en el botón
def on_button_click():
    print("¡Hiciste clic en el botón!")

# Asociar la función con el evento de hacer clic en el botón
button.config(command=on_button_click)

#eventos de teclado
def on_key_press(event):
    print(f"Presionaste la tecla {event.char}")

root.bind("<Key>", on_key_press)

#eventos de mouse
def on_mouse_click(event):
    print(f"Hiciste clic en la posición {event.x}, {event.y}")

root.bind("<Button-1>", on_mouse_click)

#eventos de movimiento de mouse
def on_mouse_move(event):
    print(f"Te moviste a la posición {event.x}, {event.y}")

root.bind("<Motion>", on_mouse_move)

#eventos de cierre de ventana
def on_close_window():
    print("¡Hasta luego!")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close_window)

#Eventos de redimensionamiento de ventana
def on_resize(event):
    print(f"Ancho: {event.width}, Alto: {event.height}")

root.bind("<Configure>", on_resize)

#evento de busqueda
def on_find(event):
    print("Buscando...")

root.bind("<Control-f>", on_find)

#evento edicion de archivo
def on_edit(event):
    print("Editando...")
    print(event.keysym)

root.bind("<Control-e>", on_edit)

#evento de ayuda
def on_help(event):
    print("Ayuda...")

root.bind("<F1>", on_help)

#evento de guardar
def on_save(event):
    print("Guardando...")
    print(event.keysym)

root.bind("<Control-s>", on_save)

#evento de abrir
def on_open(event):
    print("Abriendo...")
    print(event.keysym)

root.bind("<Control-o>", on_open)

#evento de nuevo
def on_new(event):
    print("Nuevo...")
    print(event.keysym)

root.bind("<Control-n>", on_new)

#evento de imprimir
def on_print(event):
    print("Imprimiendo...")
    print(event.keysym)

root.bind("<Control-p>", on_print)


# Iniciar el bucle principal de la interfaz de usuario
root.mainloop()

