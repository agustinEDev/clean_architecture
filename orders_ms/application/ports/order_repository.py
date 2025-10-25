"""
Order Repository Interface - Puerto para persistencia de pedidos
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.value_objects.order_id import OrderId
from domain.entities.order import Order

class OrderRepository(ABC):
    """
    Puerto para persistencia de pedidos.
    Define el contrato que deben cumplir las implementaciones.
    """
    @abstractmethod
    def save(self, order: 'Order') -> 'Order':
        """
        Guarda una orden en el repositorio.
        
        :param order: La orden a guardar.
        :return: La orden guardada.
        """
        pass

    @abstractmethod
    def get(self, order_id: OrderId) -> Optional['Order']:
        """
        Recupera una orden por su ID.
        
        :param order_id: El ID de la orden a recuperar.
        :return: La orden si se encuentra, None en caso contrario.
        """
        pass

    @abstractmethod
    def delete(self, order_id: OrderId) -> None:
        """
        Elimina una orden por su ID.
        
        :param order_id: El ID de la orden a eliminar.
        """
        pass

    @abstractmethod
    def exists(self, order_id: OrderId) -> bool:
        """
        Verifica si una orden existe por su ID.
        
        :param order_id: El ID de la orden a verificar.
        :return: True si la orden existe, False en caso contrario.
        """
        pass