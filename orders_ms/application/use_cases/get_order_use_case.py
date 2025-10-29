"""
Caso de uso para obtener los detalles de una orden
"""
from application.ports.unit_of_work import UnitOfWork
from application.dtos.get_order_dtos import GetOrderRequestDTO, GetOrderResponseDTO
from domain.value_objects.order_id import OrderId


class GetOrderUseCase:
    """
    Caso de uso para obtener los detalles completos de una orden
    incluyendo todos sus items y el total calculado
    """

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, request_dto: GetOrderRequestDTO) -> GetOrderResponseDTO | None:
        """
        Ejecuta el caso de uso para obtener detalles de una orden
        
        Args:
            request_dto: DTO con el ID de la orden a obtener
            
        Returns:
            GetOrderResponseDTO: DTO con los detalles de la orden y total calculado
            None: Si la orden no existe
        """
        # ✅ Unit of Work: Transacción para obtener la orden
        with self.uow:
            order_entity = self.uow.orders.get(request_dto.order_id)
        
            # Si la orden no existe, retornar None
            if order_entity is None:
                return None
        
            # Obtener items de la orden
            order_items = order_entity.items
            
            # Calcular total sumando todos los subtotales
            total = sum(item[2].amount * item[1].amount for item in order_items)
        
            # Mapear items para el DTO de respuesta
            items_data = [
                {
                    "sku": item[0].code,
                    "quantity": item[1].amount,
                    "price": item[2].amount,
                    "subtotal": item[2].amount * item[1].amount
                }
                for item in order_items
            ]
        
            # Crear y retornar DTO de respuesta
            return GetOrderResponseDTO(
                order_id=order_entity.order_id.code,
                customer_id=order_entity.customer_id,
                items=items_data,
                total_amount=total,
                items_count=len(order_items)
            )