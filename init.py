import tkinter as tk
from tkinter import messagebox

def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Mi Sistema Operativo Creativo")

    # Crear un widget de menú
    menu = tk.Menu(root)
    root.config(menu=menu)

    # Crear las opciones del menú
    filemenu = tk.Menu(menu)
    menu.add_cascade(label="Archivo", menu=filemenu)
    filemenu.add_command(label="Nuevo", command=nuevo)
    filemenu.add_command(label="Abrir...", command=abrir)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.quit)

    helpmenu = tk.Menu(menu)
    menu.add_cascade(label="Ayuda", menu=helpmenu)
    helpmenu.add_command(label="Acerca de...", command=acerca_de)

    # Ejecutar el bucle principal de eventos
    root.mainloop()

#funcion crer de un nuevo archivo
def nuevo():
    print("Crear un nuevo archivo...")
    
def abrir():
    print("Abrir un archivo existente...")

def acerca_de():
    messagebox.showinfo("Acerca de", "Mi Sistema Operativo Creativo v1.0")

if __name__ == "__main__":
    main()
