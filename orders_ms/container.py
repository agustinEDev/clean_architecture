"""
Composition Root - Container para inyección de dependencias
"""
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
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
        self._repository = InMemoryOrderRepository()
        self._pricing_service = StaticPricingService()
        self._event_bus = InMemoryEventBus()
    
    def create_order_use_case(self) -> CreateOrderUseCase:
        """Retorna caso de uso configurado para crear órdenes"""
        return CreateOrderUseCase(self._repository, self._event_bus)
    
    def add_item_use_case(self) -> AddItemToOrderUseCase:
        """Retorna caso de uso configurado para añadir items"""
        return AddItemToOrderUseCase(self._repository, self._pricing_service, self._event_bus)
    
    def get_order_use_case(self) -> GetOrderUseCase:
        """Retorna caso de uso configurado para obtener órdenes"""
        return GetOrderUseCase(self._repository)
    
    def list_orders_use_case(self) -> ListOrdersUseCase:
        """Retorna caso de uso configurado para listar todas las órdenes"""
        return ListOrdersUseCase(self._repository)
    
    # Métodos de acceso a infrastructure (útiles para testing)
    def get_repository(self):
        """Acceso al repositorio (útil para tests)"""
        return self._repository
    
    def get_event_bus(self):
        """Acceso al event bus (útil para tests)"""
        return self._event_bus