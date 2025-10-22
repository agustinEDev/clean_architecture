class User:
    def __init__(self, username: str, lastname: str, dni: str):
        # Validate parameters
        if not isinstance(username, str) or not username:
            raise ValueError("Username must be a non-empty string.")
        if not isinstance(lastname, str) or not lastname:
            raise ValueError("Lastname must be a non-empty string.")
        if not isinstance(dni, str) or not dni or not self.dni_validation(dni):
            raise ValueError("DNI must be a non-empty string.")
        self._username = username
        self._lastname = lastname
        self._dni = dni

    def __str__(self):
        return f"{self._username} {self._lastname} - DNI: {self._dni}"

    def dni_validation(self, dni: str) -> bool:
        # Spanish dni validation
        dni_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
        
        # 1. Validar longitud y formato básico
        if len(dni) != 9:
            return False
        number_str = dni[:8]
        letter = dni[8:].upper()
        # 2. Asegurarse de que los primeros 8 caracteres son números
        if not number_str.isdigit():
            return False
        # 3. Convertir la parte numérica a entero
        numero_dni = int(number_str)
        # 4. Calcular el resto de la división por 23 (el módulo)
        resto = numero_dni % 23
        # 5. Obtener la letra calculada usando el resto como índice
        letter_calculated = dni_letters[resto]
        # 6. Comparar la letra calculada con la letra introducida
        return letter_calculated == letter
