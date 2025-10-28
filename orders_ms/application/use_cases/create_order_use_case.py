"""
Caso de uso: Crear Pedido
"""
from application.ports.order_repository import OrderRepository
from application.ports.event_bus import EventBus
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from application.dtos.create_order_dtos import CreateOrderRequestDTO, CreateOrderResponseDTO



class CreateOrderUseCase:
    def __init__(self, order_repository: OrderRepository, event_bus: EventBus):
        self.order_repository = order_repository
        self.event_bus = event_bus

    def execute(self, create_order_request_dto: CreateOrderRequestDTO) -> CreateOrderResponseDTO:
        order_id = OrderId()
        order = Order.create(order_id, create_order_request_dto.customer_id)
        self.order_repository.save(order)
        self.event_bus.publish_many(order.pull_domain_events())
        return CreateOrderResponseDTO(order_id=str(order.order_id))