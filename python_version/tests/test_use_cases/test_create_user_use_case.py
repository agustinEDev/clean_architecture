import sys, os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from use_cases.create_user_use_case import CreateUserUseCase
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


class TestCreateUserUseCase(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryUserRepository()
        self.use_case = CreateUserUseCase(self.repository)
    
    def test_create_valid_user(self):
        result = self.use_case.execute("John", "Doe", "76826889N")
        self.assertIsNotNone(result)
        self.assertEqual(result._username, "John")
        self.assertEqual(result._lastname, "Doe")
        self.assertEqual(result._dni, "76826889N")

    def test_create_user_with_invalid_data(self):
        with self.assertRaises(ValueError):
            self.use_case.execute("", "Doe", "12345678Z")
        with self.assertRaises(ValueError):
            self.use_case.execute("John", "", "12345678Z")
        with self.assertRaises(ValueError):
            self.use_case.execute("John", "Doe", "")

if __name__ == '__main__':
    unittest.main(verbosity=2)