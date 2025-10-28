"""
Tests para PostgreSQLOrderRepository
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.quantity import Quantity
from domain.value_objects.price import Price

# Import condicional para evitar dependencias de SQLAlchemy en testing
try:
    from infrastructure.repositories.postgresql_order_repository import PostgreSQLOrderRepository
    POSTGRESQL_AVAILABLE = True
except ImportError:
    # Mock para cuando SQLAlchemy no está disponible
    POSTGRESQL_AVAILABLE = False
    PostgreSQLOrderRepository = Mock


@unittest.skipUnless(POSTGRESQL_AVAILABLE, "SQLAlchemy no disponible en entorno de testing")
class TestPostgreSQLOrderRepository(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.mock_session = Mock()
        self.repository = PostgreSQLOrderRepository(self.mock_session)
        
        # Crear orden de prueba (igual que InMemoryOrderRepository)
        self.order_id = OrderId("TEST-ORDER-123")
        self.customer_id = "customer-456"
        self.test_order = Order.create(self.order_id, self.customer_id)
        
    def test_save_new_order_without_items(self):
        """Test: Guardar nueva orden sin items"""
        # Simular que la orden no existe (nueva orden)
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        self.repository.save(self.test_order)
        
        # Assert
        self.mock_session.add.assert_called_once()  # Nueva orden añadida
        self.mock_session.commit.assert_called_once()  # Cambios confirmados
        
    def test_save_new_order_with_items(self):
        """Test: Guardar nueva orden con items"""
        # Añadir item a la orden
        self.test_order.add_item(
            sku=SKU("LAPTOP123"),
            quantity=Quantity(2), 
            price=Price(999.99, "EUR")
        )
        
        # Simular que la orden no existe
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        self.repository.save(self.test_order)
        
        # Assert
        self.mock_session.add.assert_called()  # Orden + Item añadidos
        self.mock_session.commit.assert_called_once()
        
    def test_get_existing_order(self):
        """Test: Obtener orden existente"""
        # Simular orden en BD sin items
        mock_order_model = Mock()
        mock_order_model.order_id = self.order_id.code
        mock_order_model.customer_id = self.customer_id
        mock_order_model.currency = "EUR"
        mock_order_model.items = []  # Sin items para simplificar
        
        self.mock_session.query.return_value.filter.return_value.first.return_value = mock_order_model
        
        # Act
        result = self.repository.get(self.order_id)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.order_id.code, self.order_id.code)
        self.assertEqual(result.customer_id, self.customer_id)
        
    def test_get_nonexistent_order(self):
        """Test: Obtener orden que no existe"""
        # Simular que no existe en BD
        self.mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = self.repository.get(self.order_id)
        
        # Assert
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()