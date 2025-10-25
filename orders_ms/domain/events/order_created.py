from .domain_event import DomainEvent

class OrderCreated(DomainEvent):
    def __init__(self, order_id: str, customer_id: str):
        super().__init__()
        self.order_id = order_id
        self.customer_id = customer_id

