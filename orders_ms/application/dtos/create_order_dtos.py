"""
DTOs para la creación de pedidos.
"""

from dataclasses import dataclass

# DTOs para crear pedido
@dataclass
class CreateOrderRequestDTO:
    customer_id: str

# DTOs para la respuesta de creación de pedido
@dataclass
class CreateOrderResponseDTO:
    order_id: str

