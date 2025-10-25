import unittest
from domain.value_objects.quantity import Quantity

class TestQuantity(unittest.TestCase):
    def test_quantity_creation_with_valid_value(self):
        quantity = Quantity(5)
        self.assertEqual(quantity.amount, 5)

    def test_quantity_creation_with_invalid_value(self):
        with self.assertRaises(ValueError):
            Quantity(0)
        with self.assertRaises(ValueError):
            Quantity(-3)
        with self.assertRaises(TypeError):
            Quantity("ten")

if __name__ == '__main__':
    unittest.main(verbosity=2)