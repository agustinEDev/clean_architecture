# 🏗️ Clean Architecture Learning Project

> Proyecto educativo para aprender Clean Architecture con **dos implementaciones completas**:
> - 🐍 **Sistema de Usuarios** - CRUD completo con Clean Architecture
> - 🛒 **Orders Microservice** - DDD + Event-Driven Architecture

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-53%2F53%20✅%20Passing-green.svg)](#testing)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-brightgreen.svg)](#arquitectura)
[![DDD](https://img.shields.io/badge/DDD-Domain%20Driven%20Design-purple.svg)](#orders-microservice)

## 📚 ¿Qué es Clean Architecture?

Clean Architecture separa el código en **capas concéntricas** donde las dependencias apuntan hacia el centro, garantizando que la lógica de negocio sea independiente de frameworks y tecnologías externas.

```
┌─────────────────────────────────────────────────────────┐
│            🌐 HTTP/API + Database + External            │
│  ┌─────────────────────────────────────────────────┐    │
│  │          🔌 Controllers + Repositories          │    │
│  │  ┌─────────────────────────────────────────┐    │    │
│  │  │          💼 Use Cases + DTOs            │    │    │
│  │  │  ┌─────────────────────────────────┐    │    │    │
│  │  │  │      🎯 Domain Logic Core       │    │    │    │
│  │  │  └─────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Los Dos Proyectos

### 🐍 Sistema de Usuarios - CRUD Completo
**Clean Architecture tradicional** con sistema funcional end-to-end

**✅ Implementado:**
- **Entities**: User con validación DNI español
- **Use Cases**: 5 casos de uso CRUD completos
- **Adapters**: FileUserRepository con persistencia JSON
- **Main**: Aplicación CLI ejecutable
- **Tests**: 17 tests unitarios con cobertura completa

### 🛒 Orders Microservice - DDD + Events + Web API
**Domain-Driven Design** con arquitectura dirigida por eventos y API REST completa

**✅ Implementado:**
- **Domain Layer**: Value Objects, Entities, Domain Events
- **Application Layer**: 4 Use Cases completos, Ports, DTOs
- **Infrastructure Layer**: Repositories, Services, Container DI
- **HTTP Layer**: FastAPI con endpoints REST
- **Tests**: 36 tests unitarios con cobertura completa
- **Frontend**: Interfaz web profesional con diseño B&N responsive

## 📁 Estructura del Proyecto

```
CleanArchitecture/
├── scripts/dev.py          # 🛠️ Script unificado (44/44 tests ✅)
├── python_version/         # 🐍 Sistema de Usuarios (FUNCIONAL)
│   ├── entities/          # 🎯 User con validación DNI español
│   ├── use_cases/         # 💼 CRUD completo (5 casos de uso)
│   ├── adapters/          # 🔌 FileUserRepository (JSON)
│   ├── tests/             # 🧪 17 tests unitarios ✅
│   └── main.py            # 🚀 Aplicación CLI funcional
└── orders_ms/             # 🛒 Orders Microservice (COMPLETO) 
    ├── domain/            # 🎯 Value Objects + Entities + Events
    ├── application/       # 💼 4 Use Cases + Ports + DTOs ✅
    ├── infrastructure/    # 🔧 Repositories + Services + Container DI
    ├── static/            # 🌐 Frontend elegante (HTML+CSS+JS)
    ├── tests/             # 🧪 27 tests unitarios ✅
    ├── main.py            # 🚀 FastAPI server con endpoints REST
    ├── container.py       # 📦 Dependency Injection Container
    ├── config/            # ⚙️ Sistema de logging profesional
    └── logs/              # 📝 Rotación automática de logs
```

## 🚀 Cómo Usar el Proyecto

### Ejecución Rápida
```bash
# Validar estructura y ejecutar todos los tests
python scripts/dev.py

# Ejecutar Sistema de Usuarios
cd python_version && python main.py

# Ejecutar Orders Microservice (FastAPI Web Server)
cd orders_ms && python main.py
# Abrir: http://localhost:8000/app

# Tests individuales por proyecto
cd python_version && python -m unittest discover tests -v
cd orders_ms && python -m unittest tests.domain.entities.test_order -v
```

### 🎯 Funcionalidades Destacadas

#### 🐍 Sistema de Usuarios
- **CRUD completo**: Crear, buscar, listar, actualizar, eliminar
- **Validación DNI español** con algoritmo de verificación real
- **Persistencia JSON** con formato legible y manejo de errores
- **17 tests unitarios** con cobertura completa de casos
- **Aplicación CLI funcional** lista para usar

#### 🛒 Orders Microservice
- **Domain Layer**: Value Objects (OrderId, SKU, Price, Quantity) + Order Entity
- **Application Layer**: 4 Use Cases completos (Create, AddItem, GetOrder, ListOrders)
- **Infrastructure Layer**: InMemoryRepository, StaticPricingService, EventBus
- **HTTP REST API**: FastAPI con endpoints para gestión completa de órdenes
- **Frontend Elegante**: Interfaz web responsive con diseño B&N profesional
- **Event-Driven**: OrderCreated, ItemAdded events para integración
- **27 tests unitarios** con cobertura completa de todas las capas
- **Dependency Injection**: Container para composición de dependencias
- **Logging profesional** con rotación automática y niveles configurables

## 🧪 Testing

Ambos proyectos incluyen tests unitarios exhaustivos:

```bash
# Ejecutar todos los tests (44 total)
python scripts/dev.py

# Output esperado:
# ✅ python_version: 17/17 tests passed  
# ✅ orders_ms: 27/27 tests passed
# ✅ Total: 44/44 tests passed
```

### Cobertura de Tests

#### Sistema de Usuarios (17 tests)
- `test_user.py`: Validación de entidades y DNI
- `test_use_cases.py`: Todos los casos de uso CRUD
- `test_adapters.py`: Persistencia JSON y manejo de errores

#### Orders Microservice (27 tests)
- **Domain Layer (11 tests)**: OrderId, SKU, Price, Quantity + Order entity
- **Application Layer (16 tests)**: 4 Use Cases + DTOs + Ports con coverage completa
  - `CreateOrderUseCase`: Creación de órdenes
  - `AddItemToOrderUseCase`: Añadir productos a órdenes  
  - `GetOrderUseCase`: Obtener detalles de órdenes con cálculos
  - `ListOrdersUseCase`: Listar todas las órdenes con resúmenes
- **Infrastructure Tests**: Repository, Container, Services
- **Integration Tests**: Workflows completos end-to-end

## 📖 Conceptos Clave Implementados

### 🎯 Separación de Responsabilidades
- **Entities**: Lógica de negocio pura (validación DNI, Order rules)
- **Use Cases**: Orquestación de la lógica de aplicación
- **Adapters**: Implementaciones concretas (FileRepository, etc.)

### 🔄 Dependency Inversion
```python
# Use Case depende de abstracción, no de implementación
class CreateUserUseCase:
    def __init__(self, repository: UserRepository):  # Interface
        self._repository = repository
        
# Inyección de dependencia en tiempo de ejecución
repository = FileUserRepository("users.json")  # Implementación concreta
use_case = CreateUserUseCase(repository)
```

### 📢 Event-Driven Design (Orders MS)
```python
# Domain Events para desacoplamiento
order.add_item(product_id, quantity, price)
# Publica: ItemAdded event automáticamente

# Application layer maneja events
event_bus.publish(OrderCreated(order.id, order.customer_id))
```

### 🌐 API REST Completa (Orders MS)
```python
# FastAPI Endpoints implementados
POST   /orders                    # Crear nueva orden
POST   /orders/{id}/items         # Añadir item a orden
GET    /orders/{id}               # Obtener detalles de orden
GET    /orders                    # Listar todas las órdenes
GET    /app                       # Frontend web elegante
```

### 🎨 Frontend Elegante
- **Diseño B&N profesional** con fuentes Inter + JetBrains Mono
- **Responsive design** que se adapta a cualquier pantalla
- **3 secciones principales**:
  - ✨ Crear órdenes con Customer ID
  - 📦 Añadir items con desplegables inteligentes  
  - 📊 Ver resúmenes con layout compacto horizontal
- **Funcionalidades avanzadas**:
  - 🔄 Desplegables que se actualizan automáticamente
  - 📋 Agrupación de items duplicados (ej: "Laptop x2")
  - 💰 Cálculos automáticos de totales y subtotales
  - 📝 Historial de acciones con localStorage

## 🛠️ Próximos Pasos

### Para Orders Microservice:
1. **✅ COMPLETADO**: Infrastructure + HTTP API + Frontend completo
2. **Database Layer**: PostgreSQL/SQLite repository para persistencia real
3. **Authentication**: Sistema de login/logout con JWT tokens
4. **OpenAPI Docs**: Documentación automática de la API
5. **Docker**: Containerización para deployment fácil

### Para Sistema de Usuarios:
1. **Database Adapter**: Implementar SQLite/PostgreSQL repository
2. **HTTP API**: REST endpoints para operaciones CRUD
3. **Authentication**: Login/logout con JWT tokens
4. **Frontend**: Interfaz web simple con HTML/CSS/JS

## 🚀 Demo Rápido

### Orders Microservice - ¡Pruébalo ahora!

```bash
# 1. Clonar y navegar
git clone https://github.com/agustinEDev/clean_architecture.git
cd clean_architecture/orders_ms

# 2. Ejecutar servidor
python main.py
# Servidor iniciado en http://localhost:8000

# 3. Abrir frontend elegante
# Navegador → http://localhost:8000/app

# 4. Probar API REST
curl -X POST "http://localhost:8000/orders" \
     -H "Content-Type: application/json" \
     -d '{"customer_id": "customer-123"}'

# 5. Ejecutar tests
python -m unittest discover tests -v
```

**🎯 En 2 minutos tendrás**:
- ✅ Microservicio completo funcionando
- ✅ API REST con 4 endpoints  
- ✅ Frontend elegante y responsive
- ✅ 27 tests pasando
- ✅ Clean Architecture aplicada correctamente

## 🤝 Contribuciones

Este es un proyecto educativo. Si encuentras mejoras o tienes sugerencias, ¡son bienvenidas!

## 📚 Referencias

- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design - Eric Evans](https://www.domainlanguage.com/ddd/)
- [Hexagonal Architecture - Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)

---

⭐ **¿Te está ayudando este proyecto?** ¡Dale una estrella en GitHub!

📝 **Documentando el aprendizaje paso a paso** - Cada commit representa un concepto aprendido