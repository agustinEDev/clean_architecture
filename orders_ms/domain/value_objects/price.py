from decimal import Decimal
from typing import Union

class Price:
    def __init__(self, amount: Union[float, Decimal], currency: str = "EUR"):
        if not isinstance(amount, (int, float, Decimal)):
            raise TypeError("Amount must be a number")
        if amount < 0:
            raise ValueError("Price amount cannot be negative")
        if not currency or len(currency) != 3:
            raise ValueError("Currency must be a 3-letter code")
        
        self._amount = Decimal(str(amount)).quantize(Decimal('0.01'))
        self._currency = currency.upper()
    
    @property
    def amount(self) -> Decimal:
        return self._amount
    
    @property
    def currency(self) -> str:
        return self._currency
    
    def __eq__(self, other):
        if not isinstance(other, Price):
            return False
        return self._amount == other._amount and self._currency == other._currency
    
    def __str__(self):
        return f"{self._amount} {self._currency}"