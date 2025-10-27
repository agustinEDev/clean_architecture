# 🛒 Orders Microservice - DDD + Clean Architecture

Un microservicio completo para la gestión de pedidos que aplica principios de **Domain-Driven Design (DDD)** y **Clean Architecture**. Incluye una API REST con FastAPI y un frontend web funcional.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-36%2F36%20✅-green.svg)](#testing)
[![DDD](https://img.shields.io/badge/DDD-Domain%20Driven%20Design-purple.svg)](#)

## 🎯 Funcionalidades

- **API REST Completa**: Endpoints para crear órdenes, añadir artículos, y consultar órdenes.
- **Frontend Elegante**: Interfaz web responsive y profesional para interactuar con la API.
- **Domain-Driven Design**: Modelado del dominio con Value Objects, Entities y Domain Events.
- **Arquitectura Dirigida por Eventos**: Los eventos de dominio (ej. `OrderCreated`) desacoplan la lógica.
- **Inyección de Dependencias**: Un `Container` se encarga de construir y proveer las dependencias.
- **Tests Unitarios y de Integración**: 36 tests que cubren todas las capas del microservicio.
- **Logging Profesional**: Sistema de logging configurable con rotación de ficheros.

## 📁 Estructura del Proyecto

```
orders_ms/
├── domain/            # 🎯 Value Objects, Entities, Events (DDD Core)
├── application/       # 💼 Use Cases, Ports, DTOs
├── infrastructure/    # 🔧 Repositories, Services, EventBus
├── static/            # 🎨 Frontend (HTML, CSS, JS)
├── tests/             # 🧪 36 tests unitarios y de integración
├── main.py            # 🚀 Servidor FastAPI
├── container.py       # 📦 Contenedor de Inyección de Dependencias
├── scripts/dev_ms.py  # 🛠️ Script de desarrollo y testing
└── README_MS.md       # 📖 Esta documentación
```

## 🚀 Cómo Usar

Asegúrate de estar en el directorio `orders_ms/`.

### Ejecutar el Microservicio

```bash
# Inicia el servidor web de FastAPI
python main.py
```

Una vez iniciado, puedes:
- **Abrir el frontend**: `http://localhost:8000/app`
- **Interactuar con la API**: `http://localhost:8000/orders`

### Ejecutar los Tests

El proyecto incluye un script de desarrollo para validar la estructura y ejecutar todos los tests.

```bash
# Ejecuta el script de desarrollo (tests + validaciones)
python dev_ms.py

# O ejecuta los tests directamente con unittest
python -m unittest discover tests -v
```

## 📖 Conceptos Clave Implementados

### Capas de la Arquitectura

1.  **Domain**: El corazón del software. Contiene los `Value Objects` (SKU, Price), la entidad `Order` (Aggregate Root) y los `Domain Events` (OrderCreated). No tiene dependencias externas.
2.  **Application**: Orquesta la lógica de negocio. Contiene los `Use Cases` (CreateOrderUseCase), los `Ports` (interfaces como `OrderRepository`) y los `DTOs` para la transferencia de datos.
3.  **Infrastructure**: Implementa los puertos definidos en la capa de aplicación. Contiene `InMemoryOrderRepository`, `StaticPricingService` y el `InMemoryEventBus`.
4.  **Presentation (main.py)**: Expone la funcionalidad al mundo exterior a través de una API REST (FastAPI). Es el punto de entrada de las peticiones.

### Frontend

La interfaz de usuario está construida con HTML, CSS y JavaScript puro, demostrando cómo un cliente puede consumir la API.

- **Diseño Profesional**: Estilo minimalista en blanco y negro.
- **Responsive**: Se adapta a dispositivos móviles y de escritorio.
- **Funcionalidades**:
  - Creación de órdenes.
  - Adición de artículos a través de desplegables que se actualizan dinámicamente.
  - Visualización de resúmenes de órdenes con un layout optimizado.
  - Historial de acciones persistido en `localStorage`.

### Testing

- **Tests de Dominio**: Verifican la lógica de negocio pura en las entidades y value objects.
- **Tests de Aplicación**: Prueban los casos de uso con `mocks` para las dependencias externas (repositorios, servicios).
- **Tests de Infraestructura**: Aseguran que las implementaciones concretas (como el `InMemoryOrderRepository` y el `Container`) funcionan como se espera.

## 🛠️ Próximos Pasos

- [ ] **Persistencia en Base de Datos**: Reemplazar `InMemoryOrderRepository` por una implementación con PostgreSQL.
- [ ] **Autenticación y Autorización**: Proteger los endpoints de la API con JWT.
- [ ] **Documentación de API**: Generar documentación automática con OpenAPI/Swagger.
- [ ] **Dockerización**: Crear un `Dockerfile` para facilitar el despliegue del microservicio.