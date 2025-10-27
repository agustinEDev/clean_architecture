"""
Tests para InMemoryEventBus
"""
import unittest
from infrastructure.events.in_memory_event_bus import InMemoryEventBus
from domain.events.order_created import OrderCreated
from domain.events.item_added import ItemAdded

class TestInMemoryEventBus(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.event_bus = InMemoryEventBus()
    
    def test_publish_single_event(self):
        """Test: Publicar un evento individual"""
        event = OrderCreated(order_id="ORDER123", customer_id="customer456")
        self.event_bus.publish(event)
        self.assertEqual(self.event_bus.get_events_count(), 1)
        self.assertIn(event, self.event_bus.get_published_events())
    
    def test_publish_many_events(self):
        """Test: Publicar múltiples eventos"""
        list_events = [
            ItemAdded(order_id="ORDER123", sku="SKU123", quantity=2, price=50.0),
            ItemAdded(order_id="ORDER123", sku="SKU456", quantity=1, price=30.0),
            OrderCreated(order_id="ORDER124", customer_id="customer789")
        ]
        self.event_bus.publish_many(list_events)
        self.assertEqual(self.event_bus.get_events_count(), 3)
        for event in list_events:
            self.assertIn(event, self.event_bus.get_published_events())
    
    def test_clear_events(self):
        """Test: Limpiar eventos publicados"""
        self.event_bus.publish(OrderCreated(order_id="ORDER123", customer_id="customer456"))
        self.event_bus.clear_published_events()
        self.assertEqual(self.event_bus.get_events_count(), 0)
    
    def test_get_published_events_returns_copy(self):
        """Test: get_published_events retorna una copia, no la lista original"""
        event = OrderCreated(order_id="ORDER123", customer_id="customer456")
        self.event_bus.publish(event)
        
        # Obtener la lista y modificarla
        lista_obtenida = self.event_bus.get_published_events()
        lista_obtenida.clear()  # Modificar la lista obtenida
        
        # Verificar que el event_bus aún tiene el evento original
        self.assertEqual(self.event_bus.get_events_count(), 1)
        self.assertIn(event, self.event_bus.get_published_events())


if __name__ == '__main__':
    unittest.main()