import unittest
from domain.value_objects.order_id import OrderId

class TestOrderId(unittest.TestCase):
    def test_order_id_creation(self):
        order_id = OrderId()
        self.assertIsInstance(order_id.code, str)
        self.assertEqual(len(order_id.code), 42)  # UUID length
        self.assertTrue(order_id.code.startswith("ORDER-"))  # Asegura que no esté vacío

    def test_order_id_equality(self):
        order_id1 = OrderId("12345678-1234-5678-1234-567812345678")
        order_id2 = OrderId("87654321-4321-6789-4321-678943214567")
        self.assertNotEqual(order_id1, order_id2)
        order_id3 = OrderId(order_id1.code)
        self.assertEqual(order_id1, order_id3)

if __name__ == '__main__':
    unittest.main(verbosity=2)