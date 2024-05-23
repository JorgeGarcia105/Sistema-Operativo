import os
import json
import hashlib

class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {}

    def save_users(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.users, file, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password):
        if username in self.users:
            raise ValueError("El usuario ya existe")
        hashed_password = self.hash_password(password)
        self.users[username] = hashed_password
        self.save_users()

    def validate_user(self, username, password):
        hashed_password = self.hash_password(password)
        return self.users.get(username) == hashed_password
