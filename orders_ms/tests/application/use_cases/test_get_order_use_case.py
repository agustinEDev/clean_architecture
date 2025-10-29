"""
Tests para el caso de uso GetOrderUseCase
"""
import unittest
from decimal import Decimal

from application.use_cases.get_order_use_case import GetOrderUseCase  
from application.dtos.get_order_dtos import GetOrderRequestDTO
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.price import Price
from domain.value_objects.quantity import Quantity
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.database.in_memory_unit_of_work import InMemoryUnitOfWork


class TestGetOrderUseCase(unittest.TestCase):

    def setUp(self):
        """Configurar el entorno de testing"""
        self.repository = InMemoryOrderRepository()
        self.uow = InMemoryUnitOfWork(self.repository)
        self.use_case = GetOrderUseCase(self.uow)

    def test_get_existing_order_with_items(self):
        """Test: Obtener una orden existente con items"""
        # Arrange: Crear y guardar una orden con items
        order = Order(OrderId("ORDER-123"), "customer-456")
        
        # Añadir algunos items
        laptop_sku = SKU("LAPTOP123")
        laptop_price = Price(Decimal("999.99"))
        laptop_quantity = Quantity(2)
        order.add_item(laptop_sku, laptop_quantity, laptop_price)
        
        mouse_sku = SKU("MOUSE456")
        mouse_price = Price(Decimal("29.99"))
        mouse_quantity = Quantity(1)
        order.add_item(mouse_sku, mouse_quantity, mouse_price)
        
        self.repository.save(order)
        
        # Act: Obtener la orden
        request_dto = GetOrderRequestDTO(order_id="ORDER-123")
        response_dto = self.use_case.execute(request_dto)
        
        # Assert: Verificar la respuesta
        self.assertIsNotNone(response_dto)
        self.assertEqual(response_dto.order_id, "ORDER-123")
        self.assertEqual(response_dto.customer_id, "customer-456")
        self.assertEqual(response_dto.items_count, 2)
        
        # Verificar total calculado: (999.99 * 2) + (29.99 * 1) = 2029.97
        expected_total = Decimal("999.99") * 2 + Decimal("29.99") * 1
        self.assertEqual(response_dto.total_amount, expected_total)
        
        # Verificar items
        self.assertEqual(len(response_dto.items), 2)
        
        # Verificar primer item (laptop)
        laptop_item = next((item for item in response_dto.items if item["sku"] == "LAPTOP123"), None)
        self.assertIsNotNone(laptop_item)
        self.assertEqual(laptop_item["quantity"], 2)
        self.assertEqual(laptop_item["price"], Decimal("999.99"))
        self.assertEqual(laptop_item["subtotal"], Decimal("999.99") * 2)
        
        # Verificar segundo item (mouse)
        mouse_item = next((item for item in response_dto.items if item["sku"] == "MOUSE456"), None)
        self.assertIsNotNone(mouse_item)
        self.assertEqual(mouse_item["quantity"], 1)
        self.assertEqual(mouse_item["price"], Decimal("29.99"))
        self.assertEqual(mouse_item["subtotal"], Decimal("29.99"))
    
    def test_get_empty_order(self):
        """Test: Obtener una orden sin items"""
        # Arrange: Crear orden vacía
        order = Order(OrderId("ORDER-EMPTY"), "customer-789")
        self.repository.save(order)
        
        # Act: Obtener la orden
        request_dto = GetOrderRequestDTO(order_id="ORDER-EMPTY")
        response_dto = self.use_case.execute(request_dto)
        
        # Assert: Verificar orden vacía
        self.assertIsNotNone(response_dto)
        self.assertEqual(response_dto.order_id, "ORDER-EMPTY")
        self.assertEqual(response_dto.customer_id, "customer-789")
        self.assertEqual(response_dto.items_count, 0)
        self.assertEqual(response_dto.total_amount, 0.0)
        self.assertEqual(len(response_dto.items), 0)
    
    def test_get_nonexistent_order(self):
        """Test: Intentar obtener una orden que no existe"""
        # Act: Intentar obtener orden inexistente
        request_dto = GetOrderRequestDTO(order_id="ORDER-NONEXISTENT")
        response_dto = self.use_case.execute(request_dto)
        
        # Assert: Debe retornar None
        self.assertIsNone(response_dto)
    
    def test_get_order_with_invalid_id(self):
        """Test: Obtener orden con ID inválido debe retornar None"""
        # Arrange: ID que no existe en el repositorio
        request_dto = GetOrderRequestDTO(order_id="ORDER-nonexistent")
        
        # Act
        response_dto = self.use_case.execute(request_dto)
        
        # Assert: Debe retornar None
        self.assertIsNone(response_dto)


if __name__ == '__main__':
    unittest.main()