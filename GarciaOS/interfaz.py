from cProfile import label
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class GestorArchivos:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestor de Archivos y Directorios")
        self.root.geometry("500x350")

        # Pestañas
        self.tabControl = ttk.Notebook(self.root)
        self.tab_archivos = ttk.Frame(self.tabControl)
        self.tab_directorios = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_archivos, text="Archivos")
        self.tabControl.add(self.tab_directorios, text="Directorios")
        self.tabControl.pack(expand=True, fill="both")

        # Interfaz para archivos
        self.interfaz_archivos()

        # Interfaz para directorios
        self.interfaz_directorios()

        self.root.mainloop()

    def interfaz_archivos(self):
        label_nombre_archivo = ttk.Label(self.tab_archivos, text="Nombre del archivo:")
        label_nombre_archivo.grid(row=0, column=0, padx=5, pady=5)

        self.entry_nombre_archivo = ttk.Entry(self.tab_archivos)
        self.entry_nombre_archivo.grid(row=0, column=1, padx=5, pady=5)

        label_directorio = ttk.Label(self.tab_archivos, text="Ruta del archivo:")
        label_directorio.grid(row=1, column=0, padx=5, pady=5)

        self.entry_directorio = ttk.Entry(self.tab_archivos)
        self.entry_directorio.grid(row=1, column=1, padx=5, pady=5)

        button_seleccionar_archivo = ttk.Button(self.tab_archivos, text="Seleccionar archivo", command=self.seleccionar_archivo)
        button_seleccionar_archivo.grid(row=0, column=2, padx=5, pady=5)

        label_opcion = ttk.Label(self.tab_archivos, text="Digite una opción (1-3):")
        label_opcion.grid(row=2, column=0, padx=5, pady=5)

        self.entry_opcion = ttk.Entry(self.tab_archivos)
        self.entry_opcion.grid(row=2, column=1, padx=5, pady=5)

        button_ejecutar = ttk.Button(self.tab_archivos, text="Ejecutar", command=self.seleccionar_opcion_archivos)
        button_ejecutar.grid(row=2, column=2, padx=5, pady=5)

    def interfaz_directorios(self):
        label_nombre_directorio = ttk.Label(self.tab_directorios, text="Nombre del directorio:")
        label_nombre_directorio.grid(row=0, column=0, padx=5, pady=5)

        self.entry_nombre_directorio = ttk.Entry(self.tab_directorios)
        self.entry_nombre_directorio.grid(row=0, column=1, padx=5, pady=5)

        label_directorio_padre = ttk.Label(self.tab_directorios, text="Ruta del directorio padre:")
        label_directorio_padre.grid(row=1, column=0, padx=5, pady=5)

        self.entry_directorio_padre = ttk.Entry(self.tab_directorios)
        self.entry_directorio_padre.grid(row=1, column=1, padx=5, pady=5)

        button_seleccionar_directorio = ttk.Button(self.tab_directorios, text="Seleccionar directorio", command=self.seleccionar_directorio)
        button_seleccionar_directorio.grid(row=1, column=2, padx=5, pady=5)

        # Add a label to the tab_directorios
        label_opcion = ttk.Label(self.tab_directorios, text="Digite una opción (1-3):")
        label_opcion.grid(row=2, column=0, padx=5, pady=5)

        self.entry_opcion_directorios = ttk.Entry(self.tab_directorios)
        self.entry_opcion_directorios.grid(row=2, column=1, padx=5, pady=5)

        button_ejecutar = ttk.Button(self.tab_directorios, text="Ejecutar", command=self.seleccionar_opcion_directorios)
        button_ejecutar.grid(row=2, column=2, padx=5, pady=5)

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo")
        self.entry_directorio.delete(0, tk.END)
        self.entry_directorio.insert(tk.END, archivo)

    def seleccionar_opcion_archivos(self):
        opcion = int(self.entry_opcion.get())
        if opcion == 1:
            self.crear_archivo()
        elif opcion == 2:
            self.leer_archivo()
        elif opcion == 3:
            self.eliminar_archivo()

    def seleccionar_directorio(self):
        directorio = filedialog.askdirectory(initialdir="/", title="Seleccionar directorio")
        self.entry_directorio_padre.delete(0, tk.END)
        self.entry_directorio_padre.insert(tk.END, directorio)

    def seleccionar_opcion_directorios(self):
        opcion = int(self.entry_opcion_directorios.get())
        if opcion == 1:
            self.crear_directorio()
        elif opcion == 2:
            self.eliminar_directorio()
        elif opcion == 3:
            self.listar_archivos()

    def crear_archivo(self):
        nombre_archivo = self.entry_nombre_archivo.get()
        directorio = self.entry_directorio.get()
        ruta_completa = os.path.join(directorio, nombre_archivo)
        with open(ruta_completa, "w") as archivo:
            archivo.write("Hola mundo!")
        messagebox.showinfo("Archivo creado", f"Se ha creado el archivo '{nombre_archivo}' en '{directorio}'.")

    def leer_archivo(self):
        nombre_archivo = self.entry_nombre_archivo.get()
        directorio = self.entry_directorio.get()
        ruta_completa = os.path.join(directorio, nombre_archivo)
        try:
            with open(ruta_completa, "r") as archivo:
                contenido = archivo.read()
                messagebox.showinfo("Contenido del archivo", contenido)
        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no existe en '{directorio}'.")

    def eliminar_archivo(self):
        nombre_archivo = self.entry_nombre_archivo.get()
        directorio = self.entry_directorio.get()
        ruta_completa = os.path.join(directorio, nombre_archivo)
        try:
            os.remove(ruta_completa)
            messagebox.showinfo("Archivo eliminado", f"Se ha eliminado el archivo '{nombre_archivo}' en '{directorio}'.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo '{nombre_archivo}' no existe en '{directorio}'.")

    def crear_directorio(self):
        nombre_directorio = self.entry_nombre_directorio.get()
        directorio_padre = self.entry_directorio_padre.get()
        ruta_completa = os.path.join(directorio_padre, nombre_directorio)
        os.mkdir(ruta_completa)
        messagebox.showinfo("Directorio creado", f"Se ha creado el directorio '{nombre_directorio}' en '{directorio_padre}'.")

    def listar_archivos(self):
        directorio = self.entry_directorio_padre.get()
        try:
            archivos = os.listdir(directorio)
            mensaje = "Archivos en el directorio:\n" + "\n".join(archivos)
            messagebox.showinfo("Archivos en el directorio", mensaje)
        except FileNotFoundError:
            messagebox.showerror("Error", f"El directorio '{directorio}' no existe.")
    

    def eliminar_directorio(self):
        directorio = self.entry_directorio_padre.get()
        try:
            if messagebox.askyesno("Eliminar directorio", f"¿Está seguro de que desea eliminar el directorio '{directorio}' y todos sus archivos?"):
                if len(os.listdir(directorio)) > 0:
                    for archivo in os.listdir(directorio):
                        ruta_completa = os.path.join(directorio, archivo)
                        if os.path.isfile(ruta_completa):
                            os.remove(ruta_completa)
                        else:
                            self.eliminar_directorio()  # Remove the unnecessary call to eliminar_directorio
                    os.rmdir(directorio)
                    messagebox.showinfo("Directorio eliminado", f"Se ha eliminado el directorio '{directorio}' con todos sus archivos.")
                else:
                    os.rmdir(directorio)
                    messagebox.showinfo("Directorio eliminado", f"Se ha eliminado el directorio '{directorio}'.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"El directorio '{directorio}' no existe.")
        except OSError as e:
            messagebox.showerror("Error", f"No se pudo eliminar el directorio '{directorio}': {e.strerror}")

if __name__ == "__main__":
    gestor_archivos = GestorArchivos()
