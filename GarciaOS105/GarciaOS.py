import tkinter as tk
from load import BIOSInterface

def main():
    root = tk.Tk()
    root.title("Iniciando Sistemas Operativos GarciaOS")
    root.geometry("800x600")

    # Ocupar todo el espacio de la pantalla pero conservar la barra de tareas
    #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    #root.attributes("-fullscreen", True)
    
    # Crear imagen de fondo
    background_image = tk.PhotoImage(file="./GarciaOS105/images/arranque.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Crear etiqueta de bienvenida
    label = tk.Label(root, text="Bienvenido a GarciaOS", font=("Courier", 14))
    label.pack(pady=20)

   

    BIOSInterface(root)

    root.mainloop()

if __name__ == "__main__":
    main()
