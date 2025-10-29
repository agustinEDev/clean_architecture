"""
Unit of Work pattern - Puerto (interface) para gestión transaccional
"""
from abc import ABC, abstractmethod
from application.ports.order_repository import OrderRepository


class UnitOfWork(ABC):
    """
    Port (interface) para Unit of Work pattern.
    
    Gestiona transacciones y garantiza consistencia de datos
    sin que los Use Cases conozcan detalles de implementación.
    """
    
    # Repository disponible en esta UoW
    orders: OrderRepository # Tipo de repositorio para órdenes
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.close()
    
    @abstractmethod
    def commit(self):
        """Confirma los cambios"""
        pass
    
    @abstractmethod
    def rollback(self):
        """Deshace los cambios"""
        pass
    
    @abstractmethod
    def close(self):
        """Cierra la unidad de trabajo"""
        pass