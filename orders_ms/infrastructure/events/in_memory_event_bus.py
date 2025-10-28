"""
Bus de eventos en memoria para el microservicio de pedidos.
"""
from typing import List
from application.ports.event_bus import EventBus
from domain.events.domain_event import DomainEvent

# Importamos el logger configurado
try:
    from ...config import get_logger
except ImportError:
    from config import get_logger

class InMemoryEventBus(EventBus):
    def __init__(self):
        super().__init__()
        self._logger = get_logger('orders_ms.infrastructure.events.in_memory_event_bus')
        # Lista para almacenar eventos publicados
        self._published_events: List[DomainEvent] = []

    def publish(self, event: DomainEvent) -> None:
        # Emitir evento (aquí solo lo registramos y almacenamos)
        self._logger.info(f"📢 Event published: {event}")
        self._published_events.append(event)

    def publish_many(self, events: List[DomainEvent]) -> None:
        # Emitir varios eventos
        for event in events:
            self.publish(event)

    def get_published_events(self) -> List[DomainEvent]:
        # Obtener eventos publicados
        return self._published_events.copy()
    
    def clear_published_events(self) -> None:
        # Limpiar eventos publicados
        self._published_events.clear()

    def get_events_count(self) -> int:
        # Obtener número de eventos publicados
        return len(self._published_events)
    
# Nota: Este bus de eventos en memoria es útil para pruebas y desarrollo local.
# En un entorno de producción, se debería implementar un bus de eventos real
# que interactúe con sistemas de mensajería como Kafka, RabbitMQ, etc.
