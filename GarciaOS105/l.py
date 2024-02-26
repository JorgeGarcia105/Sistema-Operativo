import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

class BIOSInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistemas Operativos GarciaOS")
        self.master.geometry("500x400")

        # Descargar la imagen desde GitHub
        self.url = "https://github.com/JorgeGarcia105/Sistema-Operativo/raw/main/GarciaOS105/images/login.jpg"
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa
            self.image_data = response.content
            self.bg_image = Image.open(BytesIO(self.image_data))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.master, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Error al descargar la imagen:", e)
            # Aquí puedes manejar el error de acuerdo a tus necesidades

        self.label = tk.Label(self.master, text="Bienvenido a GarciaOS", font=("Courier", 14))
        self.label.pack(pady=20)

def main():
    root = tk.Tk()
    BIOSInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
