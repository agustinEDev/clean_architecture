# 🏗️ Clean Architecture Learning Project

> Proyecto educativo para aprender Clean Architecture con **dos implementaciones completas**:
> - 🐍 **Sistema de Usuarios** - CRUD completo con Clean Architecture
> - 🛒 **Orders Microservice** - DDD + Event-Driven Architecture

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-32%2F32%20✅%20Passing-green.svg)](#testing)
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

### 🛒 Orders Microservice - DDD + Events
**Domain-Driven Design** con arquitectura dirigida por eventos

**✅ Implementado:**
- **Domain Layer**: Value Objects, Entities, Domain Events
- **Application Layer**: Use Cases, Ports, DTOs
- **Tests**: 15 tests unitarios con mocks para application layer
- **🔄 Pendiente**: Infrastructure + HTTP + Composition Root

## 📁 Estructura del Proyecto

```
CleanArchitecture/
├── scripts/dev.py          # 🛠️ Script unificado (32/32 tests ✅)
├── python_version/         # 🐍 Sistema de Usuarios (FUNCIONAL)
│   ├── entities/          # 🎯 User con validación DNI español
│   ├── use_cases/         # 💼 CRUD completo (5 casos de uso)
│   ├── adapters/          # 🔌 FileUserRepository (JSON)
│   ├── tests/             # 🧪 17 tests unitarios ✅
│   └── main.py            # 🚀 Aplicación CLI funcional
└── orders_ms/             # 🛒 Orders Microservice (DDD + Events)
    ├── domain/            # 🎯 Value Objects + Entities + Events
    ├── application/       # 💼 Use Cases + Ports + DTOs ✅
    ├── tests/             # 🧪 15 tests unitarios ✅
    ├── config/            # ⚙️ Sistema de logging profesional
    └── logs/              # 📝 Rotación automática de logs
```

## 🚀 Cómo Usar el Proyecto

### Ejecución Rápida
```bash
# Validar estructura y ejecutar todos los tests
python scripts/dev.py

# Ejecutar solo Sistema de Usuarios
cd python_version && python main.py

# Tests individuales por proyecto
cd python_version && python -m unittest discover tests -v
cd orders_ms && python -m tests.domain.entities.test_order
```

### 🎯 Funcionalidades Destacadas

#### 🐍 Sistema de Usuarios
- **CRUD completo**: Crear, buscar, listar, actualizar, eliminar
- **Validación DNI español** con algoritmo de verificación real
- **Persistencia JSON** con formato legible y manejo de errores
- **17 tests unitarios** con cobertura completa de casos
- **Aplicación CLI funcional** lista para usar

#### 🛒 Orders Microservice
- **Domain Layer**: Value Objects (OrderId, CustomerId, Money) + Order Entity
- **Application Layer**: CreateOrderUseCase, AddItemToOrderUseCase + Ports/DTOs
- **Event-Driven**: OrderCreated, ItemAdded events para integración
- **15 tests unitarios** con mocks completos para application layer
- **Logging profesional** con rotación automática y niveles configurables

## 🧪 Testing

Ambos proyectos incluyen tests unitarios exhaustivos:

```bash
# Ejecutar todos los tests (32 total)
python scripts/dev.py

# Output esperado:
# ✅ python_version: 17/17 tests passed
# ✅ orders_ms: 15/15 tests passed
# ✅ Total: 32/32 tests passed
```

### Cobertura de Tests

#### Sistema de Usuarios (17 tests)
- `test_user.py`: Validación de entidades y DNI
- `test_use_cases.py`: Todos los casos de uso CRUD
- `test_adapters.py`: Persistencia JSON y manejo de errores

#### Orders Microservice (15 tests)
- `test_value_objects.py`: OrderId, CustomerId, Money
- `test_order.py`: Entidad Order y domain events
- `test_use_cases.py`: Application layer con mocks

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

## 🛠️ Próximos Pasos

### Para Orders Microservice:
1. **Infrastructure Layer**: PostgreSQL repository, HTTP controllers
2. **HTTP API**: FastAPI/Flask endpoints con OpenAPI docs
3. **Composition Root**: Dependency injection container
4. **Integration Tests**: Tests end-to-end con base de datos real

### Para Sistema de Usuarios:
1. **Database Adapter**: Implementar SQLite/PostgreSQL repository
2. **HTTP API**: REST endpoints para operaciones CRUD
3. **Authentication**: Login/logout con JWT tokens
4. **Frontend**: Interfaz web simple con HTML/CSS/JS

## 🤝 Contribuciones

Este es un proyecto educativo. Si encuentras mejoras o tienes sugerencias, ¡son bienvenidas!

## 📚 Referencias

- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design - Eric Evans](https://www.domainlanguage.com/ddd/)
- [Hexagonal Architecture - Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)

---

⭐ **¿Te está ayudando este proyecto?** ¡Dale una estrella en GitHub!

📝 **Documentando el aprendizaje paso a paso** - Cada commit representa un concepto aprendido