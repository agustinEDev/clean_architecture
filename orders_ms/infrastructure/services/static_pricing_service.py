"""
Servicio de precios estáticos para el microservicio de pedidos.
"""

from typing import Dict, Optional
from decimal import Decimal
from domain.value_objects.sku import SKU
from domain.value_objects.price import Price
from application.ports.pricing_service import PricingService

class StaticPricingService(PricingService):
    def __init__(self):
        super().__init__()
        self.prices: Dict[str, Decimal] = {
            "LAPTOP123": Decimal("999.99"),
            "MOUSE456": Decimal("29.99"),
            "KEYBOARD789": Decimal("39.99"),
            "MONITOR147": Decimal("249.99"),
            "MOBOARD321": Decimal("199.99"),
            "HEADPHONE654": Decimal("89.99"),
            "GRAPHICS987": Decimal("499.99"),
            "PRINTER258": Decimal("149.99"),
            "WEBCAM369": Decimal("79.99"),
            "SPEAKERS159": Decimal("59.99"),
            "SSD512GBNVME": Decimal("89.99"),
            "RAM16GBDDR4": Decimal("74.99"),
            "CPUINTELI7K": Decimal("329.99"),
            "PSU750WGOLD": Decimal("119.99"),
            "CASEATXMID": Decimal("99.99"),
        }

    def get_price(self, sku: SKU) -> Optional[Price]:
        price = self.prices.get(sku.code)
        if price:
            return Price(price)
        return None

    def product_exists(self, sku: SKU) -> bool:
        return sku.code in self.prices