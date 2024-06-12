import json
import os

def guardar_registro_usuario(usuario, datos):
    ruta = os.path.join("./Recursos/usuarios/", f"{usuario}_datos.json")
    with open(ruta, "w") as archivo:
        json.dump(datos, archivo)

def cargar_registro_usuario(usuario):
    ruta = os.path.join("./Recursos/usuarios/", f"{usuario}_datos.json")
    try:
        with open(ruta, "r") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        return None

# Ejemplo de uso
usuario = "usuario1"
datos_usuario = {
    "archivos": ["archivo1.txt", "archivo2.jpg"],
    "carpetas": ["documentos", "fotos"]
}

# Guardar los datos del usuario
guardar_registro_usuario(usuario, datos_usuario)

# Cargar los datos del usuario
datos_cargados = cargar_registro_usuario(usuario)
print("Datos del usuario cargados:", datos_cargados)
