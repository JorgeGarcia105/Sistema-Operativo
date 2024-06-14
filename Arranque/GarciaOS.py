import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from load import BIOSInterface

def round_image(image_path, corner_radius):
    
    img = Image.open(image_path).convert("RGBA")
    img = img.resize((400, 400))  # Cambiar el tamaño de la imagen
    circle = Image.new('L', (corner_radius * 2, corner_radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, corner_radius * 2, corner_radius * 2), fill=300)
    alpha = Image.new('L', img.size, 300)
    w, h = img.size
    alpha.paste(circle.crop((0, 0, corner_radius, corner_radius)), (0, 0))
    alpha.paste(circle.crop((0, corner_radius, corner_radius, corner_radius * 2)), (0, h - corner_radius))
    alpha.paste(circle.crop((corner_radius, 0, corner_radius * 2, corner_radius)), (w - corner_radius, 0))
    alpha.paste(circle.crop((corner_radius, corner_radius, corner_radius * 2, corner_radius * 2)), (w - corner_radius, h - corner_radius))
    img.putalpha(alpha)
    return img

def main():
    root = tk.Tk()
    root.title("Iniciando Sistemas Operativos GarciaOS")
    root.geometry("800x600")

    # Crear un marco negro alrededor de la imagen de fondo
    background_frame = tk.Frame(root, bg="black")
    background_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Redondear la imagen de fondo
    rounded_image = round_image("./Recursos/images/arranque.png", 100)  # Ajustar el radio según tu preferencia

    # Convertir la imagen redondeada para su uso en tkinter
    rounded_image_tk = ImageTk.PhotoImage(rounded_image)

    # Crear imagen de fondo dentro del marco negro
    background_label = tk.Label(background_frame, image=rounded_image_tk)
    background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Crear etiqueta de bienvenida
    label = tk.Label(root, text="Bienvenido a GarciaOS", font=("Courier", 14), fg="black", bg="white")
    label.pack(pady=200)
   
    BIOSInterface(root)

    root.mainloop()

if __name__ == "__main__":
    main()
