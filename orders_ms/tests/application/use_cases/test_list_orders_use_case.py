"""
Tests para el caso de uso ListOrdersUseCase
"""
import unittest
from decimal import Decimal

from application.use_cases.list_orders_use_case import ListOrdersUseCase
from application.dtos.list_orders_dtos import ListOrdersRequestDTO
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.price import Price
from domain.value_objects.quantity import Quantity
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository


class TestListOrdersUseCase(unittest.TestCase):
    
    def setUp(self):
        """Configurar el entorno de testing"""
        self.repository = InMemoryOrderRepository()
        self.use_case = ListOrdersUseCase(self.repository)
    
    def test_list_orders_empty_repository(self):
        """Test: Listar órdenes cuando el repositorio está vacío"""
        # Act: Listar órdenes
        request_dto = ListOrdersRequestDTO()
        response_dto = self.use_case.execute(request_dto)
        
        # Assert: Verificar respuesta vacía
        self.assertIsNotNone(response_dto)
        self.assertEqual(response_dto.total_orders, 0)
        self.assertEqual(len(response_dto.orders), 0)
    
    def test_list_orders_with_data(self):
        """Test: Listar órdenes cuando hay datos"""
        # Arrange: Crear y guardar múltiples órdenes con items
        order1 = Order(OrderId("ORDER-001"), "customer-1")
        laptop_sku = SKU("LAPTOP123")
        laptop_price = Price(Decimal("999.99"))
        laptop_quantity = Quantity(2)
        order1.add_item(laptop_sku, laptop_quantity, laptop_price)
        
        order2 = Order(OrderId("ORDER-002"), "customer-2")
        mouse_sku = SKU("MOUSE456")
        mouse_price = Price(Decimal("29.99"))
        mouse_quantity = Quantity(1)
        order2.add_item(mouse_sku, mouse_quantity, mouse_price)
        
        order3 = Order(OrderId("ORDER-003"), "customer-3")  # Orden vacía
        
        self.repository.save(order1)
        self.repository.save(order2)
        self.repository.save(order3)
        
        # Act: Listar órdenes
        request_dto = ListOrdersRequestDTO()
        response_dto = self.use_case.execute(request_dto)
        
        # Assert: Verificar respuesta
        self.assertIsNotNone(response_dto)
        self.assertEqual(response_dto.total_orders, 3)
        self.assertEqual(len(response_dto.orders), 3)
        
        # Verificar que las órdenes están ordenadas por order_id
        order_ids = [order.order_id for order in response_dto.orders]
        self.assertEqual(order_ids, ["ORDER-001", "ORDER-002", "ORDER-003"])
    
    def test_list_orders_calculates_totals_correctly(self):
        """Test: Verificar que los totales se calculan correctamente"""
        # Arrange: Crear orden con múltiples items
        order = Order(OrderId("ORDER-MULTI"), "customer-multi")
        
        # Añadir múltiples items
        laptop_sku = SKU("LAPTOP123")
        laptop_price = Price(Decimal("999.99"))
        laptop_quantity = Quantity(2)
        order.add_item(laptop_sku, laptop_quantity, laptop_price)
        
        mouse_sku = SKU("MOUSE456")
        mouse_price = Price(Decimal("29.99"))
        mouse_quantity = Quantity(3)
        order.add_item(mouse_sku, mouse_quantity, mouse_price)
        
        self.repository.save(order)
        
        # Act: Listar órdenes
        request_dto = ListOrdersRequestDTO()
        response_dto = self.use_case.execute(request_dto)
        
        # Assert: Verificar cálculos
        self.assertEqual(len(response_dto.orders), 1)
        order_summary = response_dto.orders[0]
        
        self.assertEqual(order_summary.order_id, "ORDER-MULTI")
        self.assertEqual(order_summary.customer_id, "customer-multi")
        self.assertEqual(order_summary.items_count, 5)  # 2 laptops + 3 mice
        
        # Total: (999.99 * 2) + (29.99 * 3) = 1999.98 + 89.97 = 2089.95
        expected_total = Decimal("999.99") * 2 + Decimal("29.99") * 3
        self.assertEqual(order_summary.total_amount, expected_total)
    
    def test_list_orders_handles_empty_orders(self):
        """Test: Manejar órdenes sin items"""
        # Arrange: Crear orden vacía
        empty_order = Order(OrderId("ORDER-EMPTY"), "customer-empty")
        self.repository.save(empty_order)
        
        # Act: Listar órdenes
        request_dto = ListOrdersRequestDTO()
        response_dto = self.use_case.execute(request_dto)
        
        # Assert: Verificar orden vacía
        self.assertEqual(len(response_dto.orders), 1)
        order_summary = response_dto.orders[0]
        
        self.assertEqual(order_summary.order_id, "ORDER-EMPTY")
        self.assertEqual(order_summary.customer_id, "customer-empty")
        self.assertEqual(order_summary.items_count, 0)
        self.assertEqual(order_summary.total_amount, Decimal('0'))


if __name__ == '__main__':
    unittest.main(verbosity=2)