import unittest
from decimal import Decimal
from domain.value_objects.price import Price

class TestPrice(unittest.TestCase):
    def test_price_creation_with_valid_amount(self):
        price = Price(19.99, 'EUR')
        self.assertEqual(price.amount, Decimal('19.99'))
        self.assertEqual(price.amount, Decimal('19.99'))
        self.assertEqual(price.currency, 'EUR')

    def test_price_creation_with_invalid_amount(self):
        with self.assertRaises(ValueError):
            Price(-10, 'EUR')
        with self.assertRaises(TypeError):
            Price("free", "EUR")

    def test_price_creation_quantization(self):
        price = Price(19.9999, 'EUR')
        self.assertEqual(price.amount, Decimal('20.00'))  # Redondeado a 2 decimales

if __name__ == '__main__':
    unittest.main(verbosity=2)