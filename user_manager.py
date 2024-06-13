import os
import json
import hashlib

class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.users = self.cargar_usuarios()

    def cargar_usuarios(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {}

    def guardar_usuarios(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.users, file, indent=4)

    def cifrar_contraseña(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def crear_usuario(self, username, password):
        if username in self.users:
            raise ValueError("El usuario ya existe")
        hashed_password = self.cifrar_contraseña(password)
        self.users[username] = hashed_password
        self.guardar_usuarios()

    def validar_usuario(self, username, password):
        hashed_password = self.cifrar_contraseña(password)
        return self.users.get(username) == hashed_password
