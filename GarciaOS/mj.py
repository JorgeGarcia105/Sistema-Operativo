import os
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Funciones para manipular archivos

# funcion para crear un archivo
def crear_archivo(nombre_archivo, directorio):
    ruta_completa = os.path.join(directorio, nombre_archivo)
    with open(ruta_completa, "w") as archivo:
        archivo.write("Hola mundo!")
    messagebox.showinfo("Archivo creado", f"Se ha creado el archivo '{nombre_archivo}' en '{directorio}'.")

# funcion para leer un archivo 
def leer_archivo(nombre_archivo, directorio):
    ruta_completa = os.path.join(directorio, nombre_archivo)
    try:
        with open(ruta_completa, "r") as archivo:
            contenido = archivo.read()
            messagebox.showinfo("Contenido del archivo", contenido)
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no existe en '{directorio}'.")

# funcion para eliminar un archivo
def eliminar_archivo(nombre_archivo, directorio):
    ruta_completa = os.path.join(directorio, nombre_archivo)
    try:
        os.remove(ruta_completa)
        messagebox.showinfo("Archivo eliminado", f"Se ha eliminado el archivo '{nombre_archivo}' en '{directorio}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no existe en '{directorio}'.")

# funcion para crear un directorio
def crear_directorio(nombre_directorio, directorio):
    ruta_completa = os.path.join(directorio, nombre_directorio)
    os.mkdir(ruta_completa)
    messagebox.showinfo("Directorio creado", f"Se ha creado el directorio '{nombre_directorio}' en '{directorio}'.")

# funcion para eliminar un directorio
def eliminar_directorio(directorio):
    try:
        if messagebox.askyesno("Eliminar directorio", f"¿Está seguro de que desea eliminar el directorio '{directorio}' y todos sus archivos?"):
            if len(os.listdir(directorio)) > 0:
                for archivo in os.listdir(directorio):
                    ruta_completa = os.path.join(directorio, archivo)
                    if os.path.isfile(ruta_completa):
                        os.remove(ruta_completa)
                    else:
                        eliminar_directorio(ruta_completa)
                os.rmdir(directorio)
                messagebox.showinfo("Directorio eliminado", f"Se ha eliminado el directorio '{directorio}' con todos sus archivos.")
            else:
                os.rmdir(directorio)
                messagebox.showinfo("Directorio eliminado", f"Se ha eliminado el directorio '{directorio}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"El directorio '{directorio}' no existe.")
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo eliminar el directorio '{directorio}': {e.strerror}")

# funcion para seleccionar un archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo")
    entry_directorio.delete(0, tk.END)
    entry_directorio.insert(tk.END, archivo)

# funcion para seleccionar un directorio
def seleccionar_directorio():
    directorio = filedialog.askdirectory(initialdir="/", title="Seleccionar directorio")
    entry_directorio.delete(0, tk.END)
    entry_directorio.insert(tk.END, directorio)

# Función para listar archivos por nombre o ruta
def listar_archivos(directorio):
    try:
        if os.path.isdir(directorio):  # Si el directorio es válido
            archivos = os.listdir(directorio)
            mensaje = "Archivos en el directorio:\n" + "\n".join(archivos)
            messagebox.showinfo("Archivos en el directorio", mensaje)
        elif os.path.isfile(directorio):  # Si es una ruta de archivo
            mensaje = f"El archivo '{os.path.basename(directorio)}' existe."
            messagebox.showinfo("Archivo encontrado", mensaje)
        else:  # Si no se encuentra ni un directorio ni un archivo
            messagebox.showerror("Error", f"No se encontró el directorio o archivo '{directorio}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el directorio o archivo '{directorio}'.")

# funcion para seleccionar una opcion
def seleccionar_opcion():
    opcion = int(entry_opcion.get())
    if opcion in [1, 2, 3]:
        nombre_archivo = entry_nombre_archivo.get()
        directorio = entry_directorio.get()
        if opcion == 1:
            crear_archivo(nombre_archivo, directorio)
        elif opcion == 2:
            leer_archivo(nombre_archivo, directorio)
        elif opcion == 3:
            eliminar_archivo(nombre_archivo, directorio)
    elif opcion in [4, 5, 6]:
        directorio = entry_directorio.get()
        nombre_directorio = entry_nombre_archivo.get()  # Add this line to define the variable
        if opcion == 4:
            crear_directorio(nombre_directorio, directorio)
        elif opcion == 5:
            eliminar_directorio(directorio)
        elif opcion == 6:
            listar_archivos(directorio)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Gestor de Archivos y Directorios")
root.geometry("400x300")

frame_archivo = tk.Frame(root)
frame_archivo.pack(pady=10)

label_nombre_archivo = tk.Label(frame_archivo, text="Nombre del archivo:")
label_nombre_archivo.grid(row=0, column=0, padx=5, pady=5)

entry_nombre_archivo = tk.Entry(frame_archivo)
entry_nombre_archivo.grid(row=0, column=1, padx=5, pady=5)

button_seleccionar_archivo = tk.Button(frame_archivo, text="Seleccionar archivo", command=seleccionar_archivo)
button_seleccionar_archivo.grid(row=0, column=2, padx=5, pady=5)

button_seleccionar_directorio = tk.Button(frame_archivo, text="Seleccionar directorio", command=seleccionar_directorio)
button_seleccionar_directorio.grid(row=1, column=2, padx=5, pady=5)

label_directorio = tk.Label(frame_archivo, text="Ruta del archivo")
label_directorio.grid(row=1, column=0, padx=5, pady=5)

entry_directorio = tk.Entry(frame_archivo)
entry_directorio.grid(row=1, column=1, padx=5, pady=5)

frame_opciones = tk.Frame(root)
frame_opciones.pack(pady=10)

label_opcion = tk.Label(frame_opciones, text="Digite una opción (1-6):")
label_opcion.grid(row=0, column=0, padx=5, pady=5)

entry_opcion = tk.Entry(frame_opciones)
entry_opcion.grid(row=0, column=1, padx=5, pady=5)

button_ejecutar = tk.Button(frame_opciones, text="Ejecutar", command=seleccionar_opcion)
button_ejecutar.grid(row=0, column=2, padx=5, pady=5)

root.mainloop()