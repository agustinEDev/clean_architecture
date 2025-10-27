"""
Order Repository Interface - Puerto para persistencia de pedidos
"""
from abc import ABC, abstractmethod
from domain.entities.order import Order
from typing import Optional

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
    def get(self, order_id: str) -> Optional['Order']:
        """
        Recupera una orden por su ID.
        
        :param order_id: El ID de la orden a recuperar.
        :return: La orden si se encuentra, None en caso contrario.
        """
        pass

    @abstractmethod
    def delete(self, order_id: str) -> None:
        """
        Elimina una orden por su ID.
        
        :param order_id: El ID de la orden a eliminar.
        """
        pass

    @abstractmethod
    def get_all(self) -> list['Order']:
        """
        Obtiene todas las órdenes.
        
        :return: Lista con todas las órdenes.
        """
        pass