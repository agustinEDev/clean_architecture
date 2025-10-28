"""
DTOs para agregar items a un pedido.
"""

from dataclasses import dataclass

# DTOs para agregar items a un pedido
@dataclass
class AddItemToOrderRequestDTO:
    order_id: str
    sku: str
    quantity: int

# DTOs para la respuesta de agregar items a un pedido
@dataclass
class AddItemToOrderResponseDTO:
    success: bool
