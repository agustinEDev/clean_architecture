import uuid

class OrderId:
    def __init__(self, code: str = None):
        if code is None:
            self._code = 'ORDER-' + str(uuid.uuid4())
        else:
            self._code = code

    @property
    def code(self) -> str:
        return self._code

    def __str__(self):
        return self.code
    
    def __eq__(self, other):
        if not isinstance(other, OrderId):
            return False
        return self._code == other._code

    def __hash__(self):
        return hash(self._code)