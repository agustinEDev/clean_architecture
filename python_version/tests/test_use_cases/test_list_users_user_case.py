import sys, os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from use_cases.list_users_use_case import ListUsersUseCase
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
    
class TestListUsersUseCase(unittest.TestCase):
    def setUp(self):
        repository = InMemoryUserRepository()
        self.use_case = ListUsersUseCase(repository)

    def test_list_users_with_existing_users(self):
        # 1. Crear y guardar varios usuarios
        user1 = User("Alice", "Smith", "12345678Z")
        user2 = User("Bob", "Johnson", "87654321X")
        self.use_case.repository.save(user1)
        self.use_case.repository.save(user2)
        # 2. Listarlos con ListUsersUseCase
        users = self.use_case.execute()
        # 3. Verificar que se obtienen todos los usuarios
        self.assertEqual(len(users), 2)
        self.assertTrue(any(u._dni == "12345678Z" for u in users))
        self.assertTrue(any(u._dni == "87654321X" for u in users))

    def test_list_users_with_no_users(self):
        # 1. Asegurarse de que no hay usuarios en el repositorio
        users = self.use_case.execute()
        # 2. Verificar que la lista está vacía
        self.assertEqual(len(users), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)