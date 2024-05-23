import json
from cryptography.fernet import Fernet
import os
import sys

# Genera una clave de cifrado aleatoria
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Función para cifrar la contraseña utilizando AES
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

# Función para descifrar la contraseña utilizando AES
def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

# Datos de perfiles
profiles_data = {
    "perfil1": {
        "image": "./Recursos/images/arranque.png",
        "username": "Jorge",
        "password": encrypt_password("user1"),
        "background_image": "./Recursos/images/perfil1.png"
    },
    "perfil2": {
        "image": "./Recursos/images/arranque.png",
        "background_image": "./Recursos/images/perfil2.png",
        "username": "Ivan",
        "password": encrypt_password("user2")
    },
    "perfil3": {
        "image": "./Recursos/images/arranque.png",
        "background_image": "./Recursos/images/perfil3.png",
        "username": "Garcia",
        "password": encrypt_password("user3")
    }
}

# Guardar los datos cifrados en un archivo JSON
with open('./Recursos/json/profiles.json', 'w') as jsonfile:
    json.dump(profiles_data, jsonfile, indent=4)

print("Contraseñas cifradas y guardadas en 'profiles.json'")
