import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from PIL import Image

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Aquí puedes agregar tu lógica de autenticación
    # Por ejemplo, comparar con una base de datos o credenciales almacenadas.

    # Ejemplo de autenticación básica
    if username == "usuario" and password == "contraseña":
        messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido, {}!".format(username))
    else:
        messagebox.showerror("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos")

# Crear la ventana
root = tk.Tk()
root.title("Inicio de sesión")

# Configurar la geometría de la ventana para que ocupe toda la pantalla
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("{}x{}".format(width, height))

# Cargar la imagen de fondo
background_image = Image.open("./GarciaOS105/images/arranque.png")  # Ruta de tu imagen
background_image = background_image.resize((width, height))
background_image = ImageTk.PhotoImage(background_image)

# Colocar la imagen en el lienzo
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Crear y posicionar los widgets
username_label = tk.Label(root, text="Nombre de usuario:", font=("Arial", 20), bg="white")
username_label.place(relx=0.1, rely=0.3)

username_entry = tk.Entry(root, font=("Arial", 16))
username_entry.place(relx=0.4, rely=0.3)

password_label = tk.Label(root, text="Contraseña:", font=("Arial", 20), bg="white")
password_label.place(relx=0.1, rely=0.5)

password_entry = tk.Entry(root, show="*", font=("Arial", 16))
password_entry.place(relx=0.4, rely=0.5)

login_button = tk.Button(root, text="Iniciar sesión", font=("Arial", 20, "bold"), command=login, bg="#4CAF50", fg="white", relief=tk.FLAT)
login_button.place(relx=0.3, rely=0.7, relwidth=0.4, relheight=0.1)

# Iniciar el bucle de eventos
root.mainloop()
