from .domain_event import DomainEvent
from ..value_objects.price import Price
from ..value_objects.sku import SKU
from ..value_objects.quantity import Quantity

class ItemAdded(DomainEvent):
    def __init__(self, order_id: str, sku: SKU, quantity: Quantity, price: Price):
        super().__init__()
        self.order_id = order_id
        self.sku = sku
        self.quantity = quantity
        self.price = price