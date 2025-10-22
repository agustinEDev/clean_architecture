import json
from typing import List, Optional
from use_cases.user_repository_interface import UserRepositoryInterface
from entities.users import User

class FileUserRepository(UserRepositoryInterface):
    def __init__(self, file_path: str = 'users.json'):
        self.file_path = file_path
        try:
            with open(self.file_path, 'r') as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

    def _persist(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.users, file)

    def save(self, user: User) -> User:
        self.users[user._dni] = {
            'username': user._username,
            'lastname': user._lastname,
            'dni': user._dni
        }
        self._persist()
        return user
    
    def get(self, dni: str) -> Optional[User]:
        user_data = self.users.get(dni)
        if user_data:
            return User(user_data['username'], user_data['lastname'], user_data['dni'])
        return None
    
    def delete(self, dni: str) -> None:
        if dni in self.users:
            del self.users[dni]
            self._persist()

    def list(self) -> List[User]:
        return [User(data['username'], data['lastname'], data['dni']) for data in self.users.values()]