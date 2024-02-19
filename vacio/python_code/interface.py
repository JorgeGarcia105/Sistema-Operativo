# interface.py
import tkinter as tk
from tkinter import messagebox
import ctypes

# Cargar la biblioteca compartida
lib = ctypes.CDLL('../vacio/build/sum.so')
lib.sum_c.argtypes = (ctypes.c_int, ctypes.c_int)
lib.sum_c.restype = ctypes.c_int

# Función para manejar el botón de suma
def sumar():
    num1 = int(entry1.get())
    num2 = int(entry2.get())
    result = lib.sum_c(num1, num2)
    messagebox.showinfo("Resultado", f"La suma es: {result}")

# Crear la ventana
window = tk.Tk()
window.title("Sumadora")

# Crear etiquetas y campos de entrada
label1 = tk.Label(window, text="Número 1:")
label1.pack()
entry1 = tk.Entry(window)
entry1.pack()

label2 = tk.Label(window, text="Número 2:")
label2.pack()
entry2 = tk.Entry(window)
entry2.pack()

# Botón de suma
button = tk.Button(window, text="Sumar", command=sumar)
button.pack()

# Ejecutar la aplicación
window.mainloop()
