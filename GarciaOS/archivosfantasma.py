import os
import tkinter as tk
from tkinter import filedialog, messagebox

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

# Función para generar archivos y carpetas predefinidos
def generar_archivos_carpetas():
    try:
        # Crear una carpeta llamada "Directorio_Prueba"
        os.mkdir("Directorio_Prueba")
        
        # Crear archivos dentro de la carpeta
        with open("Directorio_Prueba/archivo1.txt", "w") as archivo:
            archivo.write("Contenido del archivo 1")
        with open("Directorio_Prueba/archivo2.txt", "w") as archivo:
            archivo.write("Contenido del archivo 2")

        messagebox.showinfo("Archivos y Carpetas Generados", "Se han generado archivos y carpetas predefinidos.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron generar los archivos y carpetas: {str(e)}")

# Función para seleccionar un archivo o directorio
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo")
    entry_directorio.delete(0, tk.END)
    entry_directorio.insert(tk.END, archivo)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Gestor de Archivos y Directorios")
root.geometry("400x200")

label_directorio = tk.Label(root, text="Ruta del archivo o directorio:")
label_directorio.pack(pady=5)

entry_directorio = tk.Entry(root)
entry_directorio.pack(pady=5)

button_generar_archivos = tk.Button(root, text="Generar archivos y carpetas", command=generar_archivos_carpetas)
button_generar_archivos.pack(pady=5)

button_seleccionar_archivo = tk.Button(root, text="Seleccionar archivo", command=seleccionar_archivo)
button_seleccionar_archivo.pack(pady=5)

button_listar_archivos = tk.Button(root, text="Listar archivos", command=lambda: listar_archivos(entry_directorio.get()))
button_listar_archivos.pack(pady=5)

root.mainloop()
