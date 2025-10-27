"""
Pricing Service Interface - Puerto para obtención de precios
"""
from  typing import Optional
from abc import ABC, abstractmethod
from domain.value_objects.sku import SKU
from domain.value_objects.price import Price

class PricingService(ABC):
    """
    Puerto para obtención de precios.
    Define el contrato que deben cumplir las implementaciones.
    """
    @abstractmethod
    def get_price(self, sku: SKU) -> Optional[Price]:
        """
        Obtiene el precio de un producto por su SKU.
        
        :param sku: El SKU del producto.
        :return: El precio del producto.
        """
        pass

    @abstractmethod
    def product_exists(self, sku: SKU) -> bool:
        """
        Verifica si un producto existe por su SKU.
        
        :param sku: El SKU del producto.
        :return: True si el producto existe, False en caso contrario.
        """
        pass