"""
Repositorio en memoria para la entidad Order.
"""
from typing import Dict, Optional
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from application.ports.order_repository import OrderRepository

class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        super().__init__()
        self.orders: Dict[str, Order] = {}

    def save(self, order: 'Order') -> Order:
        self.orders[order.order_id.code] = order
        return order
    
    def get(self, order_id: str) -> Optional['Order']:
        return self.orders.get(order_id)
    
    def delete(self, order_id: str) -> None:
        if order_id in self.orders:
            del self.orders[order_id]
    
    def get_all(self) -> list['Order']:
        """Obtiene todas las órdenes almacenadas"""
        return list(self.orders.values())