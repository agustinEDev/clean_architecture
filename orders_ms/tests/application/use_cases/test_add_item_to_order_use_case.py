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

class TestAddItemToOrderUseCase(unittest.TestCase):
    def setUp(self):
        # 1. Mock del Unit of Work (gestiona transacciones y repositorios)
        self.mock_uow = MagicMock()
        self.mock_orders_repo = MagicMock()
        self.mock_uow.orders = self.mock_orders_repo
        
        # 2. Mock del Pricing Service (obtiene precios de productos)
        self.mock_pricing_service = MagicMock()
        
        # 3. Mock del Event Bus (publica eventos de dominio)
        self.mock_event_bus = MagicMock()

        # 4. Crear use case con todas las dependencias
        self.use_case = AddItemToOrderUseCase(
            uow=self.mock_uow,
            pricing_service=self.mock_pricing_service,
            event_bus=self.mock_event_bus
        )

    def test_add_item_successful(self):
        # Configurar mocks
        order_id = OrderId()
        sku = SKU("TESTSKU1")
        quantity = Quantity(2)
        price = Price(100.0)

        order = Order.create(order_id, "customer_123")
        self.mock_orders_repo.get.return_value = order
        self.mock_pricing_service.product_exists.return_value = True
        self.mock_pricing_service.get_price.return_value = price

        # Ejecutar caso de uso
        request_dto = AddItemToOrderRequestDTO(
            order_id=str(order_id),
            sku=sku.code,
            quantity=quantity.amount
        )
        response_dto = self.use_case.execute(request_dto)

        # Verificar resultados
        self.assertTrue(response_dto.success)
        self.mock_orders_repo.save.assert_called_once_with(order)
        self.mock_event_bus.publish_many.assert_called_once()
        self.mock_pricing_service.product_exists.assert_called_once_with(sku)
        self.mock_pricing_service.get_price.assert_called_once_with(sku)

    def test_add_item_order_not_found(self):
        # Configurar mocks
        self.mock_orders_repo.get.return_value = None

        # Ejecutar caso de uso
        request_dto = AddItemToOrderRequestDTO(
            order_id=str(OrderId()),
            sku="NONEXISTSKU",
            quantity=1
        )
        response_dto = self.use_case.execute(request_dto)

        # Verificar resultados
        self.assertFalse(response_dto.success)
        self.mock_orders_repo.save.assert_not_called()
        self.mock_event_bus.publish_many.assert_not_called()

    def test_add_item_product_not_found(self):
        # Configurar mocks
        order_id = OrderId()
        sku = SKU("NONEXISTSKU")
        order = Order.create(order_id, "customer_123")
        self.mock_orders_repo.get.return_value = order
        self.mock_pricing_service.product_exists.return_value = False

        # Ejecutar caso de uso
        request_dto = AddItemToOrderRequestDTO(
            order_id=str(order_id),
            sku=sku.code,
            quantity=1
        )
        response_dto = self.use_case.execute(request_dto)

        # Verificar resultados
        self.assertFalse(response_dto.success)
        self.mock_orders_repo.save.assert_not_called()
        self.mock_event_bus.publish_many.assert_not_called()

if __name__ == '__main__':
    unittest.main(verbosity=2)