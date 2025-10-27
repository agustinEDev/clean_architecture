"""
Tests para los DTOs de GetOrder
"""
import unittest

from application.dtos.get_order_dtos import GetOrderRequestDTO, GetOrderResponseDTO


class TestGetOrderDTOs(unittest.TestCase):
    
    def test_get_order_request_dto_creation(self):
        """Test: Crear GetOrderRequestDTO correctamente"""
        # Act: Crear DTO de request
        request_dto = GetOrderRequestDTO(order_id="ORDER-12345")
        
        # Assert: Verificar propiedades
        self.assertEqual(request_dto.order_id, "ORDER-12345")
    
    def test_get_order_response_dto_creation_with_items(self):
        """Test: Crear GetOrderResponseDTO con items"""
        # Arrange: Preparar datos de items
        items = [
            {
                "sku": "LAPTOP123",
                "quantity": 2,
                "unit_price": 999.99,
                "total_price": 1999.98
            },
            {
                "sku": "MOUSE456", 
                "quantity": 1,
                "unit_price": 29.99,
                "total_price": 29.99
            }
        ]
        
        # Act: Crear DTO de response
        response_dto = GetOrderResponseDTO(
            order_id="ORDER-12345",
            customer_id="customer-789",
            items_count=2,
            total_amount=2029.97,
            items=items
        )
        
        # Assert: Verificar propiedades
        self.assertEqual(response_dto.order_id, "ORDER-12345")
        self.assertEqual(response_dto.customer_id, "customer-789")
        self.assertEqual(response_dto.items_count, 2)
        self.assertEqual(response_dto.total_amount, 2029.97)
        self.assertEqual(len(response_dto.items), 2)
        
        # Verificar primer item
        first_item = response_dto.items[0]
        self.assertEqual(first_item["sku"], "LAPTOP123")
        self.assertEqual(first_item["quantity"], 2)
        self.assertEqual(first_item["unit_price"], 999.99)
        self.assertEqual(first_item["total_price"], 1999.98)
    
    def test_get_order_response_dto_empty_order(self):
        """Test: Crear GetOrderResponseDTO para orden vacía"""
        # Act: Crear DTO para orden sin items
        response_dto = GetOrderResponseDTO(
            order_id="ORDER-EMPTY",
            customer_id="customer-empty",
            items_count=0,
            total_amount=0.0,
            items=[]
        )
        
        # Assert: Verificar orden vacía
        self.assertEqual(response_dto.order_id, "ORDER-EMPTY")
        self.assertEqual(response_dto.customer_id, "customer-empty")
        self.assertEqual(response_dto.items_count, 0)
        self.assertEqual(response_dto.total_amount, 0.0)
        self.assertEqual(len(response_dto.items), 0)
    
    def test_get_order_request_dto_with_different_id_formats(self):
        """Test: GetOrderRequestDTO con diferentes formatos de ID"""
        # Test con diferentes formatos válidos
        test_cases = [
            "ORDER-123",
            "ORD-2024-1", 
            "12345678",
            "ABC-DEF-01"
        ]
        
        for order_id in test_cases:
            with self.subTest(order_id=order_id):
                request_dto = GetOrderRequestDTO(order_id=order_id)
                self.assertEqual(request_dto.order_id, order_id)


if __name__ == '__main__':
    unittest.main()