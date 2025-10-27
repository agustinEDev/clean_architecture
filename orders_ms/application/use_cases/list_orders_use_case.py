"""
Caso de uso para listar todas las órdenes
"""
from application.ports.order_repository import OrderRepository
from application.dtos.list_orders_dtos import ListOrdersRequestDTO, ListOrdersResponseDTO, OrderSummaryDTO
from decimal import Decimal

class ListOrdersUseCase:
    """
    Caso de uso para obtener todas las órdenes con información resumida
    """
    
    def __init__(self, repository: OrderRepository):
        self.repository = repository
    
    def execute(self, request: ListOrdersRequestDTO) -> ListOrdersResponseDTO:
        """
        Ejecuta el caso de uso para listar todas las órdenes
        
        :param request: DTO con los datos de la petición
        :return: DTO con la lista de órdenes
        """
        # Obtener todas las órdenes del repositorio
        orders = self.repository.get_all()
        
        # Convertir a DTOs de resumen
        order_summaries = []
        for order in orders:
            # Calcular total de la orden sumando todos los items
            total_amount = Decimal('0')
            items_count = 0
            
            for item_tuple in order._items:
                sku, quantity, price = item_tuple
                subtotal = price.amount * quantity.amount
                total_amount += subtotal
                items_count += quantity.amount
            
            # Crear DTO de resumen
            summary = OrderSummaryDTO(
                order_id=order.order_id.code,
                customer_id=order.customer_id,
                items_count=items_count,
                total_amount=total_amount
            )
            order_summaries.append(summary)
        
        # Ordenar por order_id para consistencia
        order_summaries.sort(key=lambda x: x.order_id)
        
        return ListOrdersResponseDTO(
            orders=order_summaries,
            total_orders=len(order_summaries)
        )