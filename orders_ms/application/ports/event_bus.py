"""
Event Bus Interface - Puerto para la comunicación entre módulos
"""
from abc import ABC, abstractmethod
from domain.events.domain_event import DomainEvent


class EventBus(ABC):
    """
    Puerto para la comunicación entre módulos.
    Define el contrato que deben cumplir las implementaciones.
    """
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """
        Publica un evento en el bus de eventos.
        
        :param event: El evento a publicar.
        """
        pass

    @abstractmethod
    def publish_many(self, events: list[DomainEvent]) -> None:
        """
        Publica múltiples eventos en el bus de eventos.
        
        :param events: La lista de eventos a publicar.
        """
        pass