"""
Modelo SQLAlchemy para la entidad Order
"""

from sqlalchemy import Column, String, Numeric, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.database.connection import Base


class OrderModel(Base):
    """
    Modelo SQLAlchemy para la tabla orders
    """
    __tablename__ = "orders"
    
    # Columnas de la tabla
    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    currency = Column(String(3), nullable=False, default="EUR")
    items_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con items (para el futuro)
    items = relationship("OrderItemModel", back_populates="order")


class OrderItemModel(Base):
    """
    Modelo SQLAlchemy para la tabla order_items
    """
    __tablename__ = "order_items"
    
    # Columnas de la tabla
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.order_id"), nullable=False)
    sku = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación con order
    order = relationship("OrderModel", back_populates="items")