"""
Caso de uso: Agregar Item a Pedido
"""
from application.ports.order_repository import OrderRepository
from application.ports.pricing_service import PricingService
from application.ports.event_bus import EventBus
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.quantity import Quantity
from application.dtos.add_item_to_order_dtos import AddItemToOrderRequestDTO, AddItemToOrderResponseDTO

class AddItemToOrderUseCase:
    def __init__(self, order_repository: OrderRepository, pricing_service: PricingService, event_bus: EventBus):
        self.order_repository = order_repository
        self.pricing_service = pricing_service
        self.event_bus = event_bus

    def execute(self, add_item_request_dto: AddItemToOrderRequestDTO) -> AddItemToOrderResponseDTO:
        order_id = OrderId(add_item_request_dto.order_id)
        sku = SKU(add_item_request_dto.sku)
        quantity = Quantity(add_item_request_dto.quantity)

        print(f"🔍 USE CASE DEBUG: Buscando orden con ID: {order_id.code}")
        order = self.order_repository.get(order_id.code)
        if not order:
            print(f"❌ USE CASE DEBUG: Orden no encontrada: {order_id.code}")
            return AddItemToOrderResponseDTO(success=False)
        print(f"✅ USE CASE DEBUG: Orden encontrada: {order_id.code}")

        print(f"🔍 USE CASE DEBUG: Verificando si producto existe: {sku.code}")
        if not self.pricing_service.product_exists(sku):
            print(f"❌ USE CASE DEBUG: Producto no existe: {sku.code}")
            return AddItemToOrderResponseDTO(success=False)
        print(f"✅ USE CASE DEBUG: Producto existe: {sku.code}")

        price = self.pricing_service.get_price(sku)
        order.add_item(sku, quantity, price)

        self.order_repository.save(order)
        self.event_bus.publish_many(order.pull_domain_events())

        return AddItemToOrderResponseDTO(success=True)