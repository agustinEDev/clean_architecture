"""
Unit of Work implementation para producción - SQLAlchemy
"""
from sqlalchemy.orm import Session
from application.ports.unit_of_work import UnitOfWork
from infrastructure.repositories.postgresql_order_repository import PostgreSQLOrderRepository


class SQLAlchemyUnitOfWork(UnitOfWork):
    """
    Implementación SQLAlchemy del Unit of Work para producción.
    
    Gestiona transacciones reales de PostgreSQL y cierra sesiones correctamente.
    Soluciona el memory leak de sesiones.
    """
    
    def __init__(self, session_factory):
        """
        Inicializa con una factory de sesiones SQLAlchemy.
        
        Args:
            session_factory: Callable que crea sesiones SQLAlchemy
        """
        self._session_factory = session_factory
        self._session: Session = None
        self.orders: PostgreSQLOrderRepository = None
    
    def __enter__(self):
        """
        Inicia la sesión y crea los repositorios.
        Se ejecuta al entrar al 'with' statement.
        """
        self._session = self._session_factory()
        self.orders = PostgreSQLOrderRepository(self._session)
        return super().__enter__()
    
    def commit(self):
        """
        Confirma la transacción en PostgreSQL.
        """
        if self._session:
            self._session.commit()
    
    def rollback(self):
        """
        Deshace la transacción en PostgreSQL.
        """
        if self._session:
            self._session.rollback()
    
    def close(self):
        """
        Cierra la sesión SQLAlchemy.
        ¡CRÍTICO! Esto soluciona el memory leak.
        """
        if self._session:
            self._session.close()
            self._session = None