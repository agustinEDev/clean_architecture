"""
DTOs para obtener detalles de una orden
"""
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class GetOrderRequestDTO:
    order_id: str

@dataclass  
class GetOrderResponseDTO:
    order_id: str
    customer_id: str
    items: List[Dict[str, Any]]  # Lista de items con sus detalles
    total_amount: float
    items_count: int