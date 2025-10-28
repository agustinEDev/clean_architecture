"""
Pruebas para el caso de uso: Agregar Item a Pedido
"""
import unittest
from unittest.mock import MagicMock

from application.use_cases.add_item_to_order_use_case import AddItemToOrderUseCase
from application.dtos.add_item_to_order_dtos import AddItemToOrderRequestDTO, AddItemToOrderResponseDTO
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.quantity import Quantity
from domain.value_objects.price import Price
from domain.entities.order import Order
from application.ports.pricing_service import PricingService
from application.ports.event_bus import EventBus
from application.ports.order_repository import OrderRepository

class TestAddItemToOrderUseCase(unittest.TestCase):
    def setUp(self):
        self.order_repository = MagicMock(spec=OrderRepository)
        self.pricing_service = MagicMock(spec=PricingService)
        self.event_bus = MagicMock(spec=EventBus)
        self.use_case = AddItemToOrderUseCase(
            order_repository=self.order_repository,
            pricing_service=self.pricing_service,
            event_bus=self.event_bus
        )

    def test_add_item_successful(self):
        # Configurar mocks
        order_id = OrderId()
        sku = SKU("TESTSKU1")
        quantity = Quantity(2)
        price = Price(100.0)

        order = Order.create(order_id, "customer_123")
        self.order_repository.get.return_value = order
        self.pricing_service.product_exists.return_value = True
        self.pricing_service.get_price.return_value = price

        # Ejecutar caso de uso
        request_dto = AddItemToOrderRequestDTO(
            order_id=str(order_id),
            sku=sku.code,
            quantity=quantity.amount
        )
        response_dto = self.use_case.execute(request_dto)

        # Verificar resultados
        self.assertTrue(response_dto.success)
        self.order_repository.save.assert_called_once_with(order)
        self.event_bus.publish_many.assert_called_once()
        self.pricing_service.product_exists.assert_called_once_with(sku)
        self.pricing_service.get_price.assert_called_once_with(sku)

    def test_add_item_order_not_found(self):
        # Configurar mocks
        self.order_repository.get.return_value = None

        # Ejecutar caso de uso
        request_dto = AddItemToOrderRequestDTO(
            order_id=str(OrderId()),
            sku="NONEXISTSKU",
            quantity=1
        )
        response_dto = self.use_case.execute(request_dto)

        # Verificar resultados
        self.assertFalse(response_dto.success)
        self.order_repository.save.assert_not_called()
        self.event_bus.publish_many.assert_not_called()

    def test_add_item_product_not_found(self):
        # Configurar mocks
        order_id = OrderId()
        sku = SKU("NONEXISTSKU")
        order = Order.create(order_id, "customer_123")
        self.order_repository.get.return_value = order
        self.pricing_service.product_exists.return_value = False

        # Ejecutar caso de uso
        request_dto = AddItemToOrderRequestDTO(
            order_id=str(order_id),
            sku=sku.code,
            quantity=1
        )
        response_dto = self.use_case.execute(request_dto)

        # Verificar resultados
        self.assertFalse(response_dto.success)
        self.order_repository.save.assert_not_called()
        self.event_bus.publish_many.assert_not_called()

if __name__ == '__main__':
    unittest.main(verbosity=2)