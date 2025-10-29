"""
Caso de uso: Agregar Item a Pedido
"""
from application.ports.unit_of_work import UnitOfWork
from application.ports.pricing_service import PricingService
from application.ports.event_bus import EventBus
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.quantity import Quantity
from application.dtos.add_item_to_order_dtos import AddItemToOrderRequestDTO, AddItemToOrderResponseDTO

class AddItemToOrderUseCase:
    def __init__(self, uow: UnitOfWork, pricing_service: PricingService, event_bus: EventBus):
        self.uow = uow
        self.pricing_service = pricing_service
        self.event_bus = event_bus

    def execute(self, add_item_request_dto: AddItemToOrderRequestDTO) -> AddItemToOrderResponseDTO:
        order_id = OrderId(add_item_request_dto.order_id)
        sku = SKU(add_item_request_dto.sku)
        quantity = Quantity(add_item_request_dto.quantity)

        if not self.pricing_service.product_exists(sku):
            return AddItemToOrderResponseDTO(success=False)

        # ✅ Unit of Work: Transacción para agregar item a la orden
        with self.uow:
            order = self.uow.orders.get(order_id.code)
            if not order:
                return AddItemToOrderResponseDTO(success=False)

            price = self.pricing_service.get_price(sku)
            order.add_item(sku, quantity, price)
            self.uow.orders.save(order)
            # Extraer eventos antes de salir de la transacción
            events = order.pull_domain_events()

        # ✅ Publicar eventos solo si la transacción fue exitosa
        self.event_bus.publish_many(events)
        return AddItemToOrderResponseDTO(success=True)