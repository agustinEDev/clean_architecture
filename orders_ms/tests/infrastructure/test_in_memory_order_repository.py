"""
Tests para el repositorio de órdenes en memoria.
"""

import unittest
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository

class TestInMemoryOrderRepository(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.repository = InMemoryOrderRepository()
        # Crear una orden de prueba
        self.order_id = OrderId("TEST-ORDER-123")
        self.customer_id = "customer-456"
        self.test_order = Order.create(self.order_id, self.customer_id)

    def test_save_and_get_order(self):
        """Test: Guardar y recuperar una orden"""
        # 1. Guardar la orden en el repositorio
        saved_order = self.repository.save(self.test_order)
        
        # 2. Recuperar la orden usando el código correcto
        retrieved_order = self.repository.get(self.test_order.order_id.code)
        
        # 3. Verificar que la orden recuperada sea la misma
        self.assertEqual(saved_order, self.test_order)
        self.assertEqual(retrieved_order, self.test_order)
        self.assertEqual(retrieved_order.order_id.code, self.test_order.order_id.code)
        self.assertEqual(retrieved_order.customer_id, "customer-456")

    def test_get_nonexistent_order(self):
        """Test: Intentar recuperar una orden que no existe"""
        # 1. Intentar recuperar una orden con ID que no existe
        result = self.repository.get("NONEXISTENT-ORDER")
        
        # 2. Verificar que retorna None
        self.assertIsNone(result)

    def test_delete_order(self):
        """Test: Eliminar una orden"""
        # 1. Guardar una orden
        self.repository.save(self.test_order)
        
        # 2. Verificar que existe usando el código correcto
        order_code = self.test_order.order_id.code
        self.assertIsNotNone(self.repository.get(order_code))
        
        # 3. Eliminar la orden
        self.repository.delete(order_code)
        
        # 4. Verificar que ya no se puede recuperar
        self.assertIsNone(self.repository.get(order_code))

if __name__ == '__main__':
    unittest.main(verbosity=2)