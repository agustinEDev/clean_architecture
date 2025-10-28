"""
Implementación de OrderRepository usando PostgreSQL
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from application.ports.order_repository import OrderRepository
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.price import Price
from domain.value_objects.quantity import Quantity
from infrastructure.database.models.order_model import OrderModel, OrderItemModel
from infrastructure.database.connection import get_db


class PostgreSQLOrderRepository(OrderRepository):
    """
    Implementación de OrderRepository usando PostgreSQL con SQLAlchemy
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save(self, order: Order) -> None:
        """
        Guarda una orden en PostgreSQL
        """
        # Buscar si ya existe
        existing_order = self.db_session.query(OrderModel).filter(
            OrderModel.order_id == order.order_id.code
        ).first()
        
        if existing_order:
            # Actualizar orden existente
            # Calcular total usando la misma lógica que GetOrderUseCase
            total = sum(item[2].amount * item[1].amount for item in order.items)
            existing_order.total_amount = float(total)
            existing_order.items_count = len(order.items)
            
            # Eliminar items existentes y agregar los nuevos
            self.db_session.query(OrderItemModel).filter(
                OrderItemModel.order_id == order.order_id.code
            ).delete()
            
        else:
            # Crear nueva orden
            # Calcular total y obtener currency de los items
            total = sum(item[2].amount * item[1].amount for item in order.items) if order.items else 0.0
            currency = order.items[0][2].currency if order.items else "EUR"
            
            existing_order = OrderModel(
                order_id=order.order_id.code,
                customer_id=order.customer_id,
                total_amount=float(total),
                currency=currency,
                items_count=len(order.items)
            )
            self.db_session.add(existing_order)
        
        # Agregar items
        for item in order.items:
            # item es una tupla (sku, quantity, price)
            sku, quantity, price = item
            subtotal = price.amount * quantity.amount
            
            item_model = OrderItemModel(
                order_id=order.order_id.code,
                sku=sku.code,
                quantity=quantity.amount,
                price=float(price.amount),
                subtotal=float(subtotal)
            )
            self.db_session.add(item_model)
        
        # Confirmar cambios
        self.db_session.commit()
    
    def get(self, order_id: OrderId) -> Optional[Order]:
        """
        Obtiene una orden por ID desde PostgreSQL
        """
        # Determinar si order_id es string o OrderId
        order_id_str = order_id.code if hasattr(order_id, 'code') else str(order_id)
        
        order_model = self.db_session.query(OrderModel).filter(
            OrderModel.order_id == order_id_str
        ).first()
        
        if not order_model:
            return None
        
        # Convertir modelo a entidad de dominio
        return self._model_to_entity(order_model)
    
    def get_all(self) -> List[Order]:
        """
        Obtiene todas las órdenes desde PostgreSQL
        """
        order_models = self.db_session.query(OrderModel).all()
        return [self._model_to_entity(model) for model in order_models]
    
    def delete(self, order_id: OrderId) -> bool:
        """
            Elimina una orden por ID desde PostgreSQL
        """
        # Determinar si order_id es string o OrderId
        order_id_str = order_id.code if hasattr(order_id, 'code') else str(order_id)
        
        deleted_count = self.db_session.query(OrderModel).filter(
            OrderModel.order_id == order_id_str
        ).delete()
        
        # También eliminar los items relacionados
        self.db_session.query(OrderItemModel).filter(
            OrderItemModel.order_id == order_id_str
        ).delete()
        
        self.db_session.commit()
        return deleted_count > 0
    
    def _model_to_entity(self, order_model: OrderModel) -> Order:
        """
        Convierte un OrderModel a una entidad Order de dominio
        """
        # Crear la orden sin items primero
        order = Order(
            order_id=OrderId(order_model.order_id),
            customer_id=order_model.customer_id
        )
        
        # Agregar items
        for item_model in order_model.items:
            order.add_item(
                sku=SKU(item_model.sku),
                quantity=Quantity(item_model.quantity),
                price=Price(
                    amount=float(item_model.price),
                    currency=order_model.currency
                )
            )
        
        return order