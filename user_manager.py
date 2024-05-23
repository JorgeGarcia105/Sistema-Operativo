import os
import pickle
import hashlib

class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as file:
                return pickle.load(file)
        return {}

    def save_users(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.users, file)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password):
        if username in self.users:
            raise ValueError("El usuario ya existe")
        hashed_password = self.hash_password(password)
        self.users[username] = hashed_password
        self.create_user_directories(username)
        self.save_users()

    def validate_user(self, username, password):
        hashed_password = self.hash_password(password)
        return self.users.get(username) == hashed_password

    def create_user_directories(self, username):
        base_path = os.path.join(os.getcwd(), username)
        os.makedirs(os.path.join(base_path, "Documentos"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "Escritorio"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "Descargas"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "Música"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "Videos"), exist_ok=True)
