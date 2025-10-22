import sys, os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from use_cases.update_user_use_case import UpdateUserUseCase
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

class TestUpdateUserUseCase(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryUserRepository()
        self.use_case = UpdateUserUseCase(self.repository)
        # Pre-populate the repository with a user
        self.existing_user = User("John", "Doe", "12345678Z")
        self.repository.save(self.existing_user)
    
    def test_update_existing_user(self):
        result = self.use_case.execute("12345678Z", "Jane", "Smith")
        self.assertIsNotNone(result)
        self.assertEqual(result._username, "Jane")
        self.assertEqual(result._lastname, "Smith")
        self.assertEqual(result._dni, "12345678Z")

    def test_update_nonexistent_user(self):
        with self.assertRaises(ValueError):
            self.use_case.execute("87654321X", "Alice", "Johnson")

if __name__ == '__main__':
    unittest.main(verbosity=2)