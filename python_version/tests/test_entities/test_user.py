import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import unittest
from entities.users import User

class TestUser(unittest.TestCase):
    def test_valid_user_creation(self):
        user = User("Alice", "Smith", "12345678Z")
        self.assertEqual(user._username, "Alice")
        self.assertEqual(user._lastname, "Smith")
        self.assertEqual(user._dni, "12345678Z")
    
    def test_invalid_empty_username(self):
        with self.assertRaises(ValueError):
            User("", "Smith", "12345678Z")

    def test_invalid_empty_lastname(self):
        with self.assertRaises(ValueError):
            User("Alice", "", "12345678Z")

    def test_invalid_empty_dni(self):
        with self.assertRaises(ValueError):
            User("Alice", "Smith", "")

if __name__ == '__main__':
    unittest.main(verbosity=2)