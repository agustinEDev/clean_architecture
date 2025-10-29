"""
Caso de uso: Crear Pedido
Refactorizado para usar Unit of Work pattern
"""
from application.ports.unit_of_work import UnitOfWork
from application.ports.event_bus import EventBus
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from application.dtos.create_order_dtos import CreateOrderRequestDTO, CreateOrderResponseDTO


class CreateOrderUseCase:
    def __init__(self, uow: UnitOfWork, event_bus: EventBus):
        self.uow = uow
        self.event_bus = event_bus

    def execute(self, create_order_request_dto: CreateOrderRequestDTO) -> CreateOrderResponseDTO:
        # ✅ Unit of Work: Transacción para crear la orden
        with self.uow:
            order_id = OrderId()
            order = Order.create(order_id, create_order_request_dto.customer_id)
            self.uow.orders.save(order)
            # Guardar eventos antes de salir de la transacción
            events = order.pull_domain_events()
        
        # ✅ Publicar eventos solo si la transacción fue exitosa
        self.event_bus.publish_many(events)
        
        return CreateOrderResponseDTO(order_id=str(order.order_id))