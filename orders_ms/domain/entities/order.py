from ..value_objects.order_id import OrderId
from ..value_objects.sku import SKU
from ..value_objects.quantity import Quantity
from ..value_objects.price import Price
from ..events.order_created import OrderCreated
from ..events.item_added import ItemAdded

# Import logger - handle both direct execution and module execution
try:
    from ...config import get_logger
except ImportError:
    from config import get_logger

class Order:
    def __init__(self, order_id: OrderId, customer_id: str):
        self._logger = get_logger('orders_ms.domain.entities.order')
        self._order_id = order_id
        self._customer_id = customer_id
        self._items = []          # ← Agregar: Lista de items del pedido
        self._domain_events = []  # ← Agregar: Eventos pendientes de publicar
        self._logger.debug(f"Order created with ID: {order_id.code} for customer: {customer_id}")

    @property
    def order_id(self) -> OrderId:
        return self._order_id

    @property
    def customer_id(self) -> str:
        return self._customer_id
    
    @property
    def items(self) -> list:
        return self._items.copy()  # Retornar copia para inmutabilidad
    
    @classmethod
    def create(cls, order_id: OrderId, customer_id: str) -> 'Order':
        logger = get_logger('orders_ms.domain.entities.order')
        logger.info(f"Creating new order with ID: {order_id.code} for customer: {customer_id}")
        order = cls(order_id, customer_id)
        order._domain_events.append(OrderCreated(order_id.code, customer_id))
        logger.info(f"Order created successfully with ID: {order_id.code}")
        return order
    
    def add_item(self, sku: SKU, quantity: Quantity, price: Price):
        # Buscar si el SKU ya existe en la orden
        for i, (existing_sku, existing_quantity, existing_price) in enumerate(self._items):
            if existing_sku.code == sku.code:
                # Si existe, sumar las cantidades
                new_quantity = Quantity(existing_quantity.amount + quantity.amount)
                self._items[i] = (existing_sku, new_quantity, existing_price)
                self._logger.info(f"Updated item in order {self._order_id.code}: SKU={sku.code}, New Quantity={new_quantity.amount}")
                self._domain_events.append(ItemAdded(self._order_id.code, sku.code, quantity.amount, price.amount))
                return
        
        # Si no existe, agregar nuevo item
        self._logger.info(f"Adding new item to order {self._order_id.code}: SKU={sku.code}, Quantity={quantity.amount}, Price={price.amount}")
        self._items.append((sku, quantity, price))
        self._domain_events.append(ItemAdded(self._order_id.code, sku.code, quantity.amount, price.amount))
        self._logger.debug(f"Item added successfully. Order {self._order_id.code} now has {len(self._items)} unique items")

    def __str__(self):
        return f"Order(ID: {self._order_id}, CustomerID: {self._customer_id})"
    
    def __eq__(self, other):
        if not isinstance(other, Order):
            return False
        return self._order_id == other._order_id and self._customer_id == other._customer_id
    
    def __hash__(self):
        return hash((self._order_id, self._customer_id))
    
    def pull_domain_events(self):
        events = self._domain_events.copy()  # Copia los eventos
        self._domain_events.clear()          # Los limpia de la entidad
        return events                        # Los devuelve para publicar