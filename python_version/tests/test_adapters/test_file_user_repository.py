import tempfile
import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from adapters.repositories.file_user_repository import FileUserRepository
from entities.users import User


class TestFileUserRepository(unittest.TestCase):
    def setUp(self):
        # Crear un archivo temporal para las pruebas
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.repository = FileUserRepository(self.temp_file.name)

    def test_save_and_get_user(self):
        # 1. Crear un usuario de prueba
        user = User("Ana", "García", "12345678Z")
        
        # 2. Guardarlo en el repositorio
        saved_user = self.repository.save(user)

        # 3. Recuperarlo del repositorio
        retrieved_user = self.repository.get("12345678Z")

        # 4. Verificar que son iguales
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user._username, "Ana")
        self.assertEqual(retrieved_user._lastname, "García")
        self.assertEqual(retrieved_user._dni, "12345678Z")

    def test_get_nonexistent_user(self):
        # Intentar obtener un usuario que no existe
        result = self.repository.get("99999999R")
        # Should return None
        self.assertIsNone(result)

    def test_data_persist_in_file(self):
        # 1. Guardar un usuario
        user = User("Carlos", "Ruiz", "87654321X")
        self.repository.save(user)
        
        # 2. Crear un NUEVO repositorio con el mismo archivo
        new_repository = FileUserRepository(self.temp_file.name)
        
        # 3. Verificar que el usuario sigue ahí
        retrieved_user = new_repository.get("87654321X")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user._username, "Carlos")
        self.assertEqual(retrieved_user._lastname, "Ruiz")
        self.assertEqual(retrieved_user._dni, "87654321X")

if __name__ == '__main__':
    unittest.main(verbosity=2)