"""
Tests para CreateOrderUseCase
"""
import unittest
from unittest.mock import MagicMock

from application.use_cases.create_order_use_case import CreateOrderUseCase
from application.dtos.create_order_dtos import CreateOrderRequestDTO, CreateOrderResponseDTO
from domain.entities.order import Order

class TestCreateOrderUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_order_repository = MagicMock()
        self.mock_event_bus = MagicMock()
        self.use_case = CreateOrderUseCase(
            order_repository=self.mock_order_repository,
            event_bus=self.mock_event_bus
        )

    def test_execute_creates_order_and_publishes_events(self):
        # Arrange
        customer_id = "customer-123"
        request_dto = CreateOrderRequestDTO(customer_id=customer_id)

        # Act
        response_dto = self.use_case.execute(request_dto)

        # Assert
        self.mock_order_repository.save.assert_called_once()
        saved_order = self.mock_order_repository.save.call_args[0][0]
        self.assertIsInstance(saved_order, Order)
        self.assertEqual(saved_order.customer_id, customer_id)

        self.mock_event_bus.publish_many.assert_called_once()
        published_events = self.mock_event_bus.publish_many.call_args[0][0]
        self.assertTrue(len(published_events) > 0)

        self.assertIsInstance(response_dto, CreateOrderResponseDTO)
        self.assertIsNotNone(response_dto.order_id)

if __name__ == '__main__':
    unittest.main(verbosity=2)