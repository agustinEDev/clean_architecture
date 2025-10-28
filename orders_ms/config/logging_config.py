"""
Configuración de logging para Orders Microservice
"""
import logging
import logging.config
from pathlib import Path
import sys
from datetime import datetime

def setup_logging(log_level: str = "INFO", log_to_file: bool = True) -> None:
    """
    Configura el sistema de logging para el microservicio
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Si True, también guarda logs en archivo
    """
    
    # Crear directorio de logs si no existe
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configuración de logging
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(name)s - %(message)s'
            },
            'json': {
                'format': '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "function": "%(funcName)s", "line": %(lineno)d, "message": "%(message)s"}',
                'datefmt': '%Y-%m-%dT%H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'simple',
                'stream': sys.stdout
            }
        },
        'loggers': {
            'orders_ms': {
                'level': log_level,
                'handlers': ['console'],
                'propagate': False
            },
            'orders_ms.domain': {
                'level': log_level,
                'handlers': ['console'],
                'propagate': False
            },
            'orders_ms.application': {
                'level': log_level,
                'handlers': ['console'],
                'propagate': False
            },
            'orders_ms.infrastructure': {
                'level': log_level,
                'handlers': ['console'],
                'propagate': False
            }
        },
        'root': {
            'level': 'WARNING',
            'handlers': ['console']
        }
    }
    
    # Agregar handler de archivo si se solicita
    if log_to_file:
        timestamp = datetime.now().strftime("%Y%m%d")
        config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': log_level,
            'formatter': 'detailed',
            'filename': f'logs/orders_ms_{timestamp}.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        }
        
        # Agregar file handler a todos los loggers
        for logger_name in ['orders_ms', 'orders_ms.domain', 'orders_ms.application', 'orders_ms.infrastructure']:
            config['loggers'][logger_name]['handlers'].append('file')
    
    # Aplicar configuración
    logging.config.dictConfig(config)
    
    # Log inicial
    logger = logging.getLogger('orders_ms')
    logger.info("Sistema de logging configurado correctamente")
    logger.info(f"Nivel de logging: {log_level}")
    logger.info(f"Logging a archivo: {'Sí' if log_to_file else 'No'}")

def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para el módulo especificado
    
    Args:
        name: Nombre del módulo (ej: 'orders_ms.domain.entities')
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)

# Configuración por defecto para desarrollo
def setup_dev_logging():
    """Configuración de logging para desarrollo"""
    setup_logging(log_level="DEBUG", log_to_file=True)

# Configuración para producción
def setup_prod_logging():
    """Configuración de logging para producción"""
    setup_logging(log_level="INFO", log_to_file=True)

# Configuración para tests
def setup_test_logging():
    """Configuración de logging para tests (solo errores)"""
    setup_logging(log_level="ERROR", log_to_file=False)