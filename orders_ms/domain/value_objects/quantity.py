class Quantity:
    def __init__(self, amount: int):
        if amount <= 0:
            raise ValueError("Quantity must be a positive integer")
        if amount >= 1000:
            raise ValueError("Quantity must be less than 1000")
        self._amount = amount

    @property
    def amount(self) -> int:
        return self._amount
    
    def __eq__(self, other):
        if not isinstance(other, Quantity):
            return False
        return self._amount == other._amount
    
    def __str__(self):
        return str(self._amount)

    def __hash__(self):
        return hash(self._amount)