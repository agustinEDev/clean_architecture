"""
Tests para StaticPricingService
"""
import unittest
from decimal import Decimal
from domain.value_objects.sku import SKU
from domain.value_objects.price import Price
from infrastructure.services.static_pricing_service import StaticPricingService

class TestStaticPricingService(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.pricing_service = StaticPricingService()
    
    def test_get_price_existing_product(self):
        """Test: Obtener precio de un producto que existe"""
        sku = SKU("LAPTOP123")
        price = self.pricing_service.get_price(sku)
        self.assertIsNotNone(price)
        self.assertIsInstance(price, Price)
        self.assertEqual(price.amount, Decimal("999.99"))
    
    def test_get_price_nonexistent_product(self):
        """Test: Obtener precio de un producto que no existe"""
        sku = SKU("FAKE99999")
        price = self.pricing_service.get_price(sku)
        self.assertIsNone(price)
    
    def test_product_exists_true(self):
        """Test: Verificar que un producto existe"""
        sku = SKU("MOUSE456")
        exists = self.pricing_service.product_exists(sku)
        self.assertTrue(exists)
    
    def test_product_exists_false(self):
        """Test: Verificar que un producto no existe"""
        sku = SKU("UNKNOWN000")
        exists = self.pricing_service.product_exists(sku)
        self.assertFalse(exists)

if __name__ == '__main__':
    unittest.main()