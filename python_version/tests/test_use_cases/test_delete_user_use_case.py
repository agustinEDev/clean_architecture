import sys, os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from use_cases.delete_user_use_case import DeleteUserUseCase
from use_cases.user_repository_interface import UserRepositoryInterface
from entities.users import User
from typing import Optional

class InMemoryUserRepository(UserRepositoryInterface):
    def __init__(self):
        self.users = {}

    def save(self, user: User) -> User:
        self.users[user._dni] = user
        return user

    def get(self, dni: str) -> User:
        return self.users.get(dni)

    def delete(self, dni: str) -> None:
        if dni in self.users:
            del self.users[dni]

    def list(self) -> list[User]:
        return list(self.users.values())
    
    def update(self, dni: str, new_username: str, new_last_name: str) -> Optional[User]:
        if not self.users.get(dni):
            return None
        # Crear nuevo objeto User (inmutabilidad)
        updated_user = User(new_username, new_last_name, dni)
        self.users[dni] = updated_user
        return updated_user
    
class TestDeleteUserUseCase(unittest.TestCase):
    def setUp(self):
        repository = InMemoryUserRepository()
        self.use_case = DeleteUserUseCase(repository)

    def test_delete_existing_user(self):
        # 1. Crear y guardar un usuario
        user = User("Alice", "Smith", "12345678Z")
        self.use_case.repository.save(user)
        # 2. Eliminarlo con DeleteUserUseCase
        self.use_case.execute("12345678Z")
        # 3. Verificar que ya no existe
        self.assertIsNone(self.use_case.repository.get("12345678Z"))

    def test_delete_nonexistent_user(self):
        # 1. Intentar eliminar un usuario que no existe
        with self.assertRaises(ValueError):
            self.use_case.execute("00000000Y")

if __name__ == '__main__':
    unittest.main(verbosity=2)