"""
DTOs para el caso de uso de listar todas las órdenes
"""
from dataclasses import dataclass
from typing import List
from decimal import Decimal

@dataclass
class OrderSummaryDTO:
    """DTO que representa un resumen de una orden"""
    order_id: str
    customer_id: str
    items_count: int
    total_amount: Decimal

@dataclass
class ListOrdersRequestDTO:
    """DTO para la petición de listar órdenes"""
    pass  # No necesita parámetros por ahora

@dataclass
class ListOrdersResponseDTO:
    """DTO para la respuesta de listar órdenes"""
    orders: List[OrderSummaryDTO]
    total_orders: int