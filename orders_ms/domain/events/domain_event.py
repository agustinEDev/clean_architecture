import uuid
from datetime import datetime

class DomainEvent:
    def __init__(self):
        # Genera un UUID único para cada evento
        self.event_id = str(uuid.uuid4())
        # Registra el timestamp actual
        self.occurred_on = datetime.now()

    @property
    def id(self) -> str:
        return self.event_id

    @property
    def event_date(self) -> datetime:
        return self.occurred_on