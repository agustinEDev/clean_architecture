"""
Tests para Container - Composition Root
"""
import unittest
from container import Container
from application.use_cases.create_order_use_case import CreateOrderUseCase
from application.use_cases.add_item_to_order_use_case import AddItemToOrderUseCase
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.services.static_pricing_service import StaticPricingService
from infrastructure.events.in_memory_event_bus import InMemoryEventBus
from application.dtos.create_order_dtos import CreateOrderRequestDTO
from application.dtos.add_item_to_order_dtos import AddItemToOrderRequestDTO

class TestContainer(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.container = Container()
    
    def test_container_creates_infrastructure_components(self):
        """Test: Container crea correctamente los componentes de infrastructure"""
        self.assertIsInstance(self.container.get_repository(), InMemoryOrderRepository)
        self.assertIsInstance(self.container.get_event_bus(), InMemoryEventBus)
    
    def test_container_creates_use_cases(self):
        """Test: Container crea correctamente los casos de uso"""
        self.assertIsInstance(self.container.create_order_use_case(), CreateOrderUseCase)
        self.assertIsInstance(self.container.add_item_use_case(), AddItemToOrderUseCase)
    
    def test_use_cases_share_same_dependencies(self):
        """Test: Los casos de uso comparten las mismas instancias de dependencias"""
        # Verificar que el container usa las mismas instancias
        repo1 = self.container.get_repository()
        repo2 = self.container.get_repository()
        event_bus1 = self.container.get_event_bus()
        event_bus2 = self.container.get_event_bus()
        
        self.assertIs(repo1, repo2)
        self.assertIs(event_bus1, event_bus2)
    
    def test_integration_create_order_workflow(self):
        """Test: Flujo completo de crear orden usando container"""
        uc = self.container.create_order_use_case()
        request_dto = CreateOrderRequestDTO(customer_id="customer-123")
        response_dto = uc.execute(request_dto)
        
        # Verificar que la orden se creó correctamente
        self.assertIsNotNone(response_dto.order_id)
        self.assertIsInstance(response_dto.order_id, str)
        self.assertTrue(len(response_dto.order_id) > 0)
        
        # Verificar que se publicaron eventos
        event_bus = self.container.get_event_bus()
        self.assertGreater(event_bus.get_events_count(), 0)
    
    def test_integration_add_item_workflow(self):
        """Test: Flujo completo de añadir item usando container"""
        # Crear una orden primero
        uc_create = self.container.create_order_use_case()
        request_create = CreateOrderRequestDTO(customer_id="customer-123")
        response_create = uc_create.execute(request_create)
        self.assertIsNotNone(response_create.order_id)

        # Verificar que la orden existe en el repositorio
        repository = self.container.get_repository()
        saved_order = repository.get(response_create.order_id)
        self.assertIsNotNone(saved_order, "La orden debería estar guardada en el repositorio")

        # Ahora añadir un item
        uc_add_item = self.container.add_item_use_case()
        request_add_item = AddItemToOrderRequestDTO(
            order_id=response_create.order_id, 
            sku="LAPTOP123", 
            quantity=2
        )
        response_add_item = uc_add_item.execute(request_add_item)
        
        # Verificar que el item se añadió correctamente
        self.assertIsNotNone(response_add_item)
        self.assertTrue(response_add_item.success, f"Esperaba success=True pero obtuve success={response_add_item.success}")
        
        # Verificar que se publicaron más eventos
        event_bus = self.container.get_event_bus()
        self.assertGreater(event_bus.get_events_count(), 1)

    
    def test_container_isolation_between_instances(self):
        """Test: Diferentes instancias de Container están aisladas"""
        container1 = Container()
        container2 = Container()
        self.assertIsNot(container1.get_repository(), container2.get_repository())
        self.assertIsNot(container1.get_event_bus(), container2.get_event_bus())
        container1_uc = container1.create_order_use_case()
        request_dto = CreateOrderRequestDTO(customer_id="customer-123")
        response_dto = container1_uc.execute(request_dto)
        order_id = response_dto.order_id
        self.assertIsNone(container2.get_repository().get(order_id))
        self.assertEqual(container2.get_event_bus().get_events_count(), 0)

if __name__ == '__main__':
    unittest.main()