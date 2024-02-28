import os
import psutil
import tkinter as tk
from tkinter import messagebox

# Funciones para manipular archivos
def crear_archivo(nombre_archivo, directorio):
    ruta_completa = os.path.join(directorio, nombre_archivo)
    with open(ruta_completa, "w") as archivo:
        archivo.write("Hola mundo!")
    messagebox.showinfo("Archivo creado", f"Se ha creado el archivo '{nombre_archivo}' en '{directorio}'.")

def leer_archivo(nombre_archivo, directorio):
    ruta_completa = os.path.join(directorio, nombre_archivo)
    try:
        with open(ruta_completa, "r") as archivo:
            contenido = archivo.read()
            messagebox.showinfo("Contenido del archivo", contenido)
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no existe en '{directorio}'.")

def eliminar_archivo(nombre_archivo, directorio):
    ruta_completa = os.path.join(directorio, nombre_archivo)
    try:
        os.remove(ruta_completa)
        messagebox.showinfo("Archivo eliminado", f"Se ha eliminado el archivo '{nombre_archivo}' en '{directorio}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no existe en '{directorio}'.")

def eliminar_directorio(directorio):
    try:
        if len(os.listdir(directorio)) > 0:
            if messagebox.askyesno("Eliminar directorio", f"El directorio '{directorio}' contiene archivos. ¿Desea eliminarlo con todos sus archivos?"):
                for archivo in os.listdir(directorio):
                    ruta_completa = os.path.join(directorio, archivo)
                    if os.path.isfile(ruta_completa):
                        os.remove(ruta_completa)
                    else:
                        eliminar_directorio(ruta_completa)
                os.rmdir(directorio)
                messagebox.showinfo("Directorio eliminado", f"Se ha eliminado el directorio '{directorio}' con todos sus archivos.")
            else:
                messagebox.showinfo("Operación cancelada", "La eliminación del directorio fue cancelada.")
        else:
            os.rmdir(directorio)
            messagebox.showinfo("Directorio eliminado", f"Se ha eliminado el directorio '{directorio}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"El directorio '{directorio}' no existe.")
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo eliminar el directorio '{directorio}': {e.strerror}")

def listar_archivos(directorio):
    try:
        archivos = os.listdir(directorio)
        mensaje = "Archivos en el directorio:\n" + "\n".join(archivos)
        messagebox.showinfo("Archivos en el directorio", mensaje)
    except FileNotFoundError:
        messagebox.showerror("Error", f"El directorio '{directorio}' no existe.")

def mostrar_info_sistema():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    mensaje = f"CPU: {cpu_percent}%\nMemoria: {mem_percent}%"
    messagebox.showinfo("Información del sistema", mensaje)

def seleccionar_opcion(opcion):
    if opcion == 1:
        nombre_archivo = entry_nombre_archivo.get()
        directorio = os.path.abspath(entry_directorio.get())
        crear_archivo(nombre_archivo, directorio)
    elif opcion == 2:
        nombre_archivo = entry_nombre_archivo.get()
        directorio = os.path.abspath(entry_directorio.get())
        leer_archivo(nombre_archivo, directorio)
    elif opcion == 3:
        nombre_archivo = entry_nombre_archivo.get()
        directorio = os.path.abspath(entry_directorio.get())
        eliminar_archivo(nombre_archivo, directorio)
    elif opcion == 4:
        directorio = os.path.abspath(entry_directorio.get())
        eliminar_directorio(directorio)
    elif opcion == 5:
        directorio = os.path.abspath(entry_directorio.get())
        listar_archivos(directorio)
    elif opcion == 6:
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

label_opcion = tk.Label(root, text="Digite una opción (1-6):")
label_opcion.pack()
entry_opcion = tk.Entry(root)
entry_opcion.pack()

root.mainloop()
