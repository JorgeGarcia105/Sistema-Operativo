import tkinter as tk
from load import BIOSInterface

def main():
    root = tk.Tk()
    root.title("Iniciando Sistemas Operativos GarciaOS")
    root.geometry("500x400")

    label = tk.Label(root, text="Bienvenido a GarciaOS", font=("Courier", 14))
    label.pack(pady=20)

    BIOSInterface(root)

    root.mainloop()

if __name__ == "__main__":
    main()
