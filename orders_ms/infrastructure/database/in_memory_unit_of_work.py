"""
Unit of Work implementation para tests - InMemory
"""
from application.ports.unit_of_work import UnitOfWork
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository


class InMemoryUnitOfWork(UnitOfWork):
    """
    Implementación InMemory del Unit of Work para tests.
    
    No usa base de datos real, todo queda en memoria.
    Perfecto para tests rápidos y aislados.
    """
    
    def __init__(self, repository: InMemoryOrderRepository):
        """
        Inicializa con un repositorio InMemory ya creado.
        
        Args:
            repository: Instancia de InMemoryOrderRepository
        """
        self.orders = repository
    
    def commit(self):
        """
        En InMemory no hay transacciones reales.
        Los datos ya están 'guardados' en memoria.
        """
        pass  # No hay nada que hacer
    
    def rollback(self):
        """
        En InMemory no podemos hacer rollback real.
        Para tests, usualmente no es necesario.
        """
        pass  # No hay nada que deshacer
    
    def close(self):
        """
        En InMemory no hay conexiones que cerrar.
        El repositorio sigue disponible para otros tests.
        """
        pass  # No hay recursos que liberar