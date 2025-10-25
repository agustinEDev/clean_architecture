import unittest
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from domain.events.order_created import OrderCreated
from domain.events.item_added import ItemAdded
from domain.value_objects.sku import SKU
from domain.value_objects.quantity import Quantity
from domain.value_objects.price import Price


class TestOrder(unittest.TestCase):
    def test_constructor_creates_order_with_empty_state(self):
        # Test del constructor básico
        order_id = OrderId()
        customer_id = "123456789"
        order = Order.create(order_id, customer_id)
        self.assertEqual(order.order_id, order_id)
        self.assertEqual(order.customer_id, customer_id)

    def test_create_factory_method_emits_order_created_event(self):
        # Test del factory method
        order_id = OrderId()
        customer_id = "123456789"
        order = Order.create(order_id, customer_id)
        events = order.pull_domain_events()
        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], OrderCreated)

    def test_add_item_emits_item_added_event(self):
        # Test de add_item
        order_id = OrderId()
        customer_id = "123456789"
        order = Order.create(order_id, customer_id)
        sku = SKU("ITEM1234")
        quantity = Quantity(2)
        price = Price(19.99)
        order.add_item(sku, quantity, price)
        events = order.pull_domain_events()
        self.assertEqual(len(events), 2)  # OrderCreated + ItemAdded
        self.assertIsInstance(events[1], ItemAdded)

if __name__ == '__main__':
    unittest.main(verbosity=2)