"""
Configuración de conexión a PostgreSQL usando SQLAlchemy
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión desde variable de entorno
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://orders_user:orders_pass@localhost:5433/orders_db"
)

# Motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para modelos
Base = declarative_base()

# Función para obtener sesión de base de datos
def get_db():
    """
    Obtiene una sesión de base de datos.
    Debe cerrarse después de usar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()