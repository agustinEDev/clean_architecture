"""
Inicialización de base de datos - Crear tablas
"""

from infrastructure.database.connection import engine, Base
from infrastructure.database.models.order_model import OrderModel, OrderItemModel

def create_tables():
    """
    Crea todas las tablas en PostgreSQL
    """
    print("🗃️ Creando tablas en PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente!")

if __name__ == "__main__":
    create_tables()