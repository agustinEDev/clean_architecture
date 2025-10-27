"""
Caso de uso para obtener los detalles de una orden
"""
from typing import Optional
from application.ports.order_repository import OrderRepository
from application.dtos.get_order_dtos import GetOrderRequestDTO, GetOrderResponseDTO
from domain.value_objects.order_id import OrderId


class GetOrderUseCase:
    """
    Caso de uso para obtener los detalles completos de una orden
    incluyendo todos sus items y el total calculado
    """
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    def execute(self, request_dto: GetOrderRequestDTO) -> GetOrderResponseDTO | None:
        """
        Ejecuta el caso de uso para obtener detalles de una orden
        
        Args:
            request_dto: DTO con el ID de la orden a obtener
            
        Returns:
            GetOrderResponseDTO: DTO con los detalles de la orden y total calculado
            None: Si la orden no existe
        """
        # Obtener la orden del repositorio
        order_entity = self.order_repository.get(request_dto.order_id)
        
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