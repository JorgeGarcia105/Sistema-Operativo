import os
import psutil
import tkinter as tk
from tkinter import messagebox

#creando inicio maquina para ejecutar sistema operativo
#creacion de mensaje maquina de inicio de sistem operativo lenguaje maquina










def crear_archivo(nombre_archivo):
    with open(nombre_archivo, "w") as archivo:
        archivo.write("Hola mundo!")
    messagebox.showinfo("Archivo creado", f"Se ha creado el archivo '{nombre_archivo}'.")

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            contenido = archivo.read()
            messagebox.showinfo("Contenido del archivo", contenido)
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no existe.")

def eliminar_archivo(nombre_archivo):
    try:
        os.remove(nombre_archivo)
        messagebox.showinfo("Archivo eliminado", f"Se ha eliminado el archivo '{nombre_archivo}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no existe.")

def listar_archivos(directorio):
    archivos = os.listdir(directorio)
    mensaje = "Archivos en el directorio:\n" + "\n".join(archivos)
    messagebox.showinfo("Archivos en el directorio", mensaje)

def mostrar_info_sistema():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    mensaje = f"CPU: {cpu_percent}%\nMemoria: {mem_percent}%"
    messagebox.showinfo("Información del sistema", mensaje)

def seleccionar_opcion(opcion):
    if opcion == 1:
        nombre_archivo = entry_nombre_archivo.get()
        crear_archivo(nombre_archivo)
    elif opcion == 2:
        nombre_archivo = entry_nombre_archivo.get()
        leer_archivo(nombre_archivo)
    elif opcion == 3:
        nombre_archivo = entry_nombre_archivo.get()
        eliminar_archivo(nombre_archivo)
    elif opcion == 4:
        directorio = entry_directorio.get()
        listar_archivos(directorio)
    elif opcion == 5:
        mostrar_info_sistema()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Gestor de Archivos y Sistema")
root.geometry("400x300")

label_nombre_archivo = tk.Label(root, text="Nombre del archivo:")
label_nombre_archivo.pack()
entry_nombre_archivo = tk.Entry(root)
entry_nombre_archivo.pack()

label_directorio = tk.Label(root, text="Directorio:")
label_directorio.pack()
entry_directorio = tk.Entry(root)
entry_directorio.pack()

def ejecutar_opcion():
    opcion = int(entry_opcion.get())
    seleccionar_opcion(opcion)

button_ejecutar = tk.Button(root, text="Ejecutar", command=ejecutar_opcion)
button_ejecutar.pack()

label_opcion = tk.Label(root, text="Digite una opción (1-5):")
label_opcion.pack()
entry_opcion = tk.Entry(root)
entry_opcion.pack()

root.mainloop()
