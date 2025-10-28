"""
Composition Root - Container para inyección de dependencias
"""
from infrastructure.services.static_pricing_service import StaticPricingService
from infrastructure.events.in_memory_event_bus import InMemoryEventBus
from application.use_cases.create_order_use_case import CreateOrderUseCase
from application.use_cases.add_item_to_order_use_case import AddItemToOrderUseCase
from application.use_cases.get_order_use_case import GetOrderUseCase
from application.use_cases.list_orders_use_case import ListOrdersUseCase

class Container:
    """
    Container principal que ensambla toda la aplicación.
    Aquí se conectan todas las dependencias siguiendo Clean Architecture.
    """
    
    def __init__(self):
        """Inicializa todas las dependencias necesarias"""
        # Detectar si estamos en entorno de testing con múltiples métodos
        import os
        import sys
        
        is_testing = (
            os.getenv('TESTING', 'false').lower() == 'true' or
            'unittest' in sys.modules or
            'pytest' in sys.modules or
            any('test' in arg for arg in sys.argv) or
            'unittest' in ' '.join(sys.argv)
        )
        
        if is_testing:
            # Usar InMemory para tests
            from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
            self._repository = InMemoryOrderRepository()
        else:
            # Usar PostgreSQL para producción
            from infrastructure.database.connection import SessionLocal
            from infrastructure.repositories.postgresql_order_repository import PostgreSQLOrderRepository
            # Almacenar la factory de sesiones, no una sesión específica
            self._session_factory = SessionLocal
            self._repository = None  # Se creará bajo demanda
        
        self._pricing_service = StaticPricingService()
        self._event_bus = InMemoryEventBus()
    
    def _get_repository(self):
        """Obtiene el repositorio apropiado (con nueva sesión para PostgreSQL)"""
        if hasattr(self, '_session_factory'):
            # PostgreSQL: crear nueva sesión cada vez
            from infrastructure.repositories.postgresql_order_repository import PostgreSQLOrderRepository
            db_session = self._session_factory()
            return PostgreSQLOrderRepository(db_session)
        else:
            # InMemory para testing
            return self._repository
    
    def create_order_use_case(self) -> CreateOrderUseCase:
        """Retorna caso de uso configurado para crear órdenes"""
        return CreateOrderUseCase(self._get_repository(), self._event_bus)
    
    def add_item_use_case(self) -> AddItemToOrderUseCase:
        """Retorna caso de uso configurado para añadir items"""
        return AddItemToOrderUseCase(self._get_repository(), self._pricing_service, self._event_bus)
    
    def get_order_use_case(self) -> GetOrderUseCase:
        """Retorna caso de uso configurado para obtener órdenes"""
        return GetOrderUseCase(self._get_repository())
    
    def list_orders_use_case(self) -> ListOrdersUseCase:
        """Retorna caso de uso configurado para listar todas las órdenes"""
        return ListOrdersUseCase(self._get_repository())
    
    # Métodos de acceso a infrastructure (útiles para testing)
    def get_repository(self):
        """Acceso al repositorio (útil para tests)"""
        return self._get_repository()
    
    def get_event_bus(self):
        """Acceso al event bus (útil para tests)"""
        return self._event_bus