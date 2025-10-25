import unittest
from domain.value_objects.sku import SKU

class TestSKU(unittest.TestCase):
    def test_valid_sku_creation(self):
        sku = SKU("ABC1234")
        self.assertEqual(sku.code, "ABC1234")

    def test_invalid_empty_sku(self):
        with self.assertRaises(ValueError):
            SKU("")