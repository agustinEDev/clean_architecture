"""
Tests para el endpoint HTTP GET /orders/{order_id}
"""
import unittest
from decimal import Decimal
from fastapi.testclient import TestClient

# Importar la aplicación FastAPI
from main import app
from container import Container
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.price import Price
from domain.value_objects.quantity import Quantity


class TestGetOrderEndpoint(unittest.TestCase):
    
    def setUp(self):
        """Configurar el cliente de testing"""
        self.client = TestClient(app)
        # Obtener el repositorio para setup de datos
        self.container = app.container
        self.repository = self.container.get_repository()
    
    def tearDown(self):
        """Limpiar datos después de cada test"""
        # Limpiar el repositorio
        self.repository.orders.clear()
    
    def test_get_existing_order_success(self):
        """Test: GET /orders/{order_id} - Orden existente con items"""
        # Arrange: Crear orden con items
        order = Order(OrderId("ORDER-TEST1"), "customer-123")
        
        # Añadir items
        laptop_sku = SKU("LAPTOP456")
        laptop_price = Price(Decimal("1299.99"))
        laptop_quantity = Quantity(1)
        order.add_item(laptop_sku, laptop_quantity, laptop_price)
        
        keyboard_sku = SKU("KEYBOARD789")
        keyboard_price = Price(Decimal("89.99"))
        keyboard_quantity = Quantity(2)
        order.add_item(keyboard_sku, keyboard_quantity, keyboard_price)
        
        self.repository.save(order)
        
        # Act: Hacer petición GET
        response = self.client.get("/orders/ORDER-TEST1")
        
        # Assert: Verificar respuesta
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["order_id"], "ORDER-TEST1")
        self.assertEqual(data["customer_id"], "customer-123")
        self.assertEqual(data["items_count"], 2) # El número de líneas de items, no la cantidad total
        
        # Verificar total: 1299.99 + (89.99 * 2) = 1479.97
        expected_total = 1299.99 + (89.99 * 2)
        self.assertAlmostEqual(data["total_amount"], expected_total, places=2)
        
        # Verificar items
        items = data["items"]
        self.assertEqual(len(items), 2)
        
        # Buscar laptop
        laptop_item = next((item for item in items if item["sku"] == "LAPTOP456"), None)
        self.assertIsNotNone(laptop_item)
        self.assertEqual(laptop_item["quantity"], 1)
        self.assertEqual(laptop_item["price"], 1299.99)
        self.assertEqual(laptop_item["subtotal"], 1299.99)
        
        # Buscar keyboard
        keyboard_item = next((item for item in items if item["sku"] == "KEYBOARD789"), None)
        self.assertIsNotNone(keyboard_item)
        self.assertEqual(keyboard_item["quantity"], 2)
        self.assertEqual(keyboard_item["price"], 89.99)
        self.assertAlmostEqual(keyboard_item["subtotal"], 89.99 * 2, places=2)
    
    def test_get_empty_order_success(self):
        """Test: GET /orders/{order_id} - Orden existente sin items"""
        # Arrange: Crear orden vacía
        order = Order(OrderId("ORDER-EMPTY"), "customer-empty")
        self.repository.save(order)
        
        # Act: Hacer petición GET
        response = self.client.get("/orders/ORDER-EMPTY")
        
        # Assert: Verificar respuesta
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["order_id"], "ORDER-EMPTY")
        self.assertEqual(data["customer_id"], "customer-empty")
        self.assertEqual(data["items_count"], 0)
        self.assertEqual(data["total_amount"], 0.0)
        self.assertEqual(len(data["items"]), 0)
    
    def test_get_nonexistent_order_404(self):
        """Test: GET /orders/{order_id} - Orden que no existe"""
        # Act: Hacer petición GET para orden inexistente
        response = self.client.get("/orders/ORDER-NOTFOUND")
        
        # Assert: Debe retornar 404
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Order not found")
    
    def test_get_order_with_special_characters_in_id(self):
        """Test: GET /orders/{order_id} - ID con caracteres especiales válidos"""
        # Arrange: Crear orden con ID con guiones
        order = Order(OrderId("ORD-2024-1"), "customer-special")
        
        # Añadir un item
        item_sku = SKU("SPECIAL123")
        item_price = Price(Decimal("59.99"))
        item_quantity = Quantity(3)
        order.add_item(item_sku, item_quantity, item_price)
        
        self.repository.save(order)
        
        # Act: Hacer petición GET
        response = self.client.get("/orders/ORD-2024-1")
        
        # Assert: Verificar respuesta exitosa
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["order_id"], "ORD-2024-1")
        self.assertEqual(data["customer_id"], "customer-special")
        self.assertEqual(data["items_count"], 1)
        self.assertEqual(data["total_amount"], 59.99 * 3)


if __name__ == '__main__':
    unittest.main()