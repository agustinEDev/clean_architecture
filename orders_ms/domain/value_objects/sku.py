class SKU:
    def __init__(self, code: str):
        code = code.strip().upper()
        # Comprobamos la longitud del código SKU sea de 8 a 12 caracteres
        if not (8 <= len(code) <= 12):
            raise ValueError("SKU code must be between 8 and 12 characters long")
        # Comprobamos que sea alfanumérico
        if not code.isalnum():
            raise ValueError("SKU code must be alphanumeric")
        
        self._code = code

    @property
    def code(self) -> str:
        return self._code
    
    def __eq__(self, other):
        if not isinstance(other, SKU):
            return False
        return self._code == other._code
    
    def __str__(self):
        return self._code
    
    def __hash__(self):
        return hash(self._code)