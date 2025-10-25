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

## 🎯 Implementaciones del Proyecto

### 🐍 Sistema de Usuarios (FUNCIONAL ✅)
**CRUD completo** para gestión de usuarios con Clean Architecture

**Funcionalidades:**
- ✅ Crear usuarios con validación de DNI español
- ✅ Buscar usuarios por DNI  
- ✅ Listar todos los usuarios
- ✅ Actualizar información de usuarios
- ✅ Eliminar usuarios
- ✅ **17 tests unitarios** + repositorio JSON

### 🛒 Orders Microservice (DOMAIN + APPLICATION ✅)
**Microservicio de pedidos** con DDD + Event-Driven Architecture

**Implementado:**
- ✅ **Domain Layer**: Value Objects, Entities, Domain Events
- ✅ **Application Layer**: Use Cases, Ports, DTOs
- ✅ **15 tests unitarios** con mocks + event-driven design
- 🔄 **Pendiente**: Infrastructure + HTTP + Composition Root

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

##  Cómo Usar el Proyecto

### 📋 Ejecución
```bash
# Validar estructura y ejecutar todos los tests
python scripts/dev.py

# Ejecutar solo Sistema de Usuarios
cd python_version && python main.py

# Ejecutar tests individuales por proyecto
cd python_version && python -m unittest discover tests -v
cd orders_ms && python -m tests.domain.entities.test_order
```

### 🎯 Funcionalidades Implementadas

####  Sistema de Usuarios
- ✅ **CRUD completo**: Crear, buscar, listar, actualizar, eliminar
- ✅ **Validación DNI español** con algoritmo real
- ✅ **Persistencia JSON** con formato legible
- ✅ **17 tests unitarios** con cobertura completa

#### 🛒 Orders Microservice  
- ✅ **Domain Layer**: Value Objects, Entities, Domain Events
- ✅ **Application Layer**: Use Cases, Ports, DTOs
- ✅ **Event-Driven**: OrderCreated, ItemAdded events
- ✅ **15 tests unitarios** con mocks para application layer

```

### 🎯 Capa 1: Entities

La entidad `User` encapsula las reglas de negocio fundamentales:

- **Validación automática** en el constructor
- **Inmutabilidad** después de la creación
- **Validación de DNI español** con algoritmo real

```python
# Ejemplo de uso
user = User("Juan", "Pérez", "12345678Z")  # ✅ Válido
user = User("", "Pérez", "12345678Z")      # ❌ ValueError
```

### 💼 Capa 2: Use Cases

Los casos de uso implementan la lógica específica de la aplicación:

#### ✅ CreateUserUseCase
- Recibe datos primitivos (strings)
- Crea y valida la entidad User  
- Persiste usando el repositorio
- Retorna el usuario creado

```python
use_case = CreateUserUseCase(repository)
user = use_case.execute("Ana", "García", "87654321X")
```

#### ✅ FindUserUseCase
- Busca un usuario específico por DNI
- Retorna el usuario encontrado o None
- Maneja casos donde el usuario no existe

```python
use_case = FindUserUseCase(repository)
user = use_case.execute("87654321X")  # Retorna User o None
```

#### ✅ ListUsersUseCase
- Lista todos los usuarios del sistema
- Retorna una lista de usuarios (puede estar vacía)
- Operación de solo lectura

```python
use_case = ListUsersUseCase(repository)
users = use_case.execute()  # Retorna List[User]
```

#### ✅ UpdateUserUseCase
- Actualiza información de un usuario existente
- Permite modificar nombre y apellidos (DNI inmutable)
- Valida existencia antes de actualizar
- Lanza excepción si el usuario no existe

```python
use_case = UpdateUserUseCase(repository)
user = use_case.execute("87654321X", "Ana María", "García López")
```

#### ✅ DeleteUserUseCase
- Elimina un usuario del sistema por DNI
- Valida existencia antes de eliminar
- Lanza excepción si el usuario no existe
- Operación irreversible

```python
use_case = DeleteUserUseCase(repository)
use_case.execute("87654321X")  # Elimina el usuario
```

### 🔌 Capa 3: Interface Adapters

Los adaptadores conectan las capas internas con el mundo exterior:

#### ✅ FileUserRepository
- **Persistencia en JSON**: Guarda usuarios en archivo local con formato legible
- **JSON formateado**: Indentación automática y soporte de caracteres especiales
- **Manejo de errores**: Archivos inexistentes o vacíos
- **Implementación intercambiable**: Cumple el contrato de la interfaz
- **CRUD completo**: Operaciones Create, Read, Update, Delete

```python
# El mismo caso de uso puede usar cualquier repositorio
file_repo = FileUserRepository("users.json")
memory_repo = InMemoryUserRepository()

# Ambos funcionan exactamente igual
use_case = CreateUserUseCase(file_repo)  # Persiste en archivo
use_case = CreateUserUseCase(memory_repo)  # Solo en memoria
```

### �🔍 Características Técnicas

#### Validación de DNI
- ✅ Formato: 8 números + 1 letra
- ✅ Algoritmo de verificación español
- ✅ Cálculo del dígito de control

#### Principios SOLID
- **Single Responsibility**: Cada clase tiene una responsabilidad
- **Dependency Inversion**: Los Use Cases dependen de abstracciones
- **Interface Segregation**: Interfaces específicas y pequeñas
- **Open/Closed**: Fácil agregar nuevos repositorios sin modificar código existente

## 🛠️ Desarrollo y CI/CD

### Script de Desarrollo Inteligente

El proyecto incluye un sistema de desarrollo automatizado con `scripts/dev.py`:

```bash
# Ejecutar validación completa del proyecto
python scripts/dev.py
```

#### 🎯 Funcionalidades del Script de Desarrollo:
- **🔍 Validación de Estructura**: Verifica que todos los archivos y carpetas estén presentes
- **📊 Estadísticas del Proyecto**: Cuenta tests, casos de uso, documentación
- **📝 Estado de Git**: Muestra cambios pendientes y rama actual  
- **🧪 Ejecución Automática de Tests**: Ejecuta todos los tests desde la raíz
- **✅ Exit Codes Apropiados**: 0 para éxito, 1 para errores (compatible con CI/CD)

#### 🚀 Integración con Workflows
Compatible con herramientas de automatización como **Warp Drive**:
```bash
wf-dev-push-unitest  # Workflow automático: validar → test → commit → push
```

El script valida tanto archivos de la raíz (README, .gitignore) como de `python_version/`, asegurando que no se pierdan cambios en ninguna parte del proyecto.

## 🧪 Testing

### Estrategia de Testing por Capas

```bash
# Validación completa + tests (RECOMENDADO para desarrollo)
python scripts/dev.py

# Ejecutar solo tests desde python_version/
cd python_version
python -m unittest discover tests/ -v

# O ejecutar tests por capa individualmente
cd python_version
python tests/test_entities/test_user.py
python tests/test_use_cases/test_create_user_use_case.py
python tests/test_use_cases/test_find_user_use_case.py
python tests/test_use_cases/test_list_users_user_case.py
python tests/test_use_cases/test_update_user_use_case.py
python tests/test_use_cases/test_delete_user_use_case.py
python tests/test_adapters/test_file_user_repository.py

# Ejecutar la aplicación completa con CRUD funcional
cd python_version
python main.py
```

### 🎭 Test Strategy
- **InMemoryUserRepository**: Mock para testing de Use Cases
- **FileUserRepository Tests**: Verificación de persistencia real
- **Temporary Files**: Tests aislados sin efectos secundarios
- **Cobertura completa**: Casos válidos, inválidos y edge cases
- **Testing por capas**: Cada capa se testea independientemente

## 📈 Estado del Proyecto

### ✅ Completado
- 🐍 **Sistema de Usuarios**: CRUD completo funcional (17 tests ✅)
- 🛒 **Orders MS - Domain Layer**: Value Objects + Entities + Events (11 tests ✅)  
- 🛒 **Orders MS - Application Layer**: Use Cases + Ports + DTOs (4 tests ✅)
- 🛠️ **Dev Tools**: Script unificado de tests y validación

### 🔄 Próximos Pasos
- 🛒 **Orders MS - Infrastructure Layer**: InMemory repositories + static pricing
- � **Orders MS - HTTP Layer**: FastAPI endpoints + REST API
- � **Orders MS - Composition Root**: Dependency injection container
- [ ] **Infrastructure Layer**: Implementar adaptadores
  - [ ] InMemoryOrderRepository para persistencia en memoria
  - [ ] StaticPricingService con precios fijos
  - [ ] NoOpEventBus para eventos (stub inicial)
- [ ] **HTTP Layer**: API REST con FastAPI
  - [ ] POST /orders endpoint para crear órdenes
  - [ ] POST /orders/{orderId}/items para agregar items
  - [ ] Validación de requests y manejo de errores HTTP
- [ ] **Integration**: Composición e inyección de dependencias
  - [ ] container.py para dependency injection
  - [ ] Configuración de entorno (dev/prod)
  - [ ] Tests de integración end-to-end

### 📋 Mejoras Futuras
- [ ] **Controllers**: Capa de presentación (CLI interactiva/Web)
- [ ] **External**: Base de datos real (SQLite/PostgreSQL)
- [ ] **Performance Monitoring**: Métricas y monitoring del microservicio
- [ ] **API Documentation**: OpenAPI/Swagger para endpoints REST
- [ ] **Documentación avanzada**: Patrones aprendidos y mejores prácticas

## 🎓 Conceptos Aprendidos

### 🏗️ Arquitectura
- ✅ **Separación en capas** con responsabilidades claras
- ✅ **Inversión de dependencias** con interfaces
- ✅ **Independencia de frameworks** y bases de datos

### 🔧 Técnicas
- ✅ **Inyección de dependencias** manual
- ✅ **Repository Pattern** para abstracción de datos
- ✅ **Value Objects** con validación automática
- ✅ **Test-Driven Development** por capas

### 💡 Beneficios Observados
- ✅ **Testabilidad**: Cada capa se puede testear aisladamente con mocks
- ✅ **Mantenibilidad**: Cambios localizados por responsabilidad
- ✅ **Flexibilidad**: Cambiar de archivo a base de datos sin tocar lógica
- ✅ **Comprensibilidad**: Flujo de dependencias claro hacia el centro
- ✅ **Reutilización**: El mismo Use Case funciona con cualquier repositorio
- ✅ **Evolución**: Fácil agregar nuevas funcionalidades sin romper existentes

## 🚀 Cómo ejecutar el proyecto

### 🐍 Python Version (FUNCIONAL)
```bash
# Clonar el repositorio
git clone <tu-repo>
cd CleanArchitecture

# Opción 1: Validación completa + tests TODOS LOS PROYECTOS (RECOMENDADO)
python scripts/dev.py  # Ejecuta Python Version (17 tests) + Orders MS (5 tests)

# Opción 2: Solo ejecutar la aplicación CRUD de usuarios
cd python_version
python main.py

# Opción 3: Solo ejecutar tests de Python Version
cd python_version
python -m unittest discover tests/ -v

# Opción 4: Desarrollo con workflow automatizado (requiere Warp Drive)
wf-dev-push-unitest  # Valida, testea, commitea y hace push automáticamente
```

### 🛒 Orders Microservice (DOMAIN + APPLICATION COMPLETADO ✅)

**Estado actual**: Domain Layer + Application Layer implementados y testeados

#### 🎯 Domain Layer (11 tests ✅)
- **Entidades**: Order con agregado raíz 
- **Value Objects**: OrderId, SKU, Quantity, Price
- **Eventos**: OrderCreated, ItemAdded
- **Tests**: 11/11 pasando

#### 💼 Application Layer (4 tests ✅) 
- **Puertos**: OrderRepository, PricingService, EventBus
- **DTOs**: CreateOrderRequest/Response, AddItemToOrderRequest/Response  
- **Casos de Uso**: CreateOrderUseCase, AddItemToOrderUseCase
- **Tests**: 4/4 pesando con mocks

```bash
# Ejecutar tests individuales de Orders MS
cd orders_ms

# Tests de dominio
python -m tests.domain.entities.test_order
python -m tests.domain.value_objects.test_price
python -m tests.domain.value_objects.test_sku

# Tests de aplicación (nuevos!)
python -m tests.application.use_cases.test_create_order_use_case
python -m tests.application.use_cases.test_add_item_to_order_use_case

# Probar el sistema de logging
python -c "
from config import setup_dev_logging
from domain.entities.order import Order
from domain.value_objects.order_id import OrderId
from domain.value_objects.sku import SKU
from domain.value_objects.quantity import Quantity
from domain.value_objects.price import Price

setup_dev_logging()  
order = Order.create(OrderId(), 'CUSTOMER123')
order.add_item(SKU('LAPTOP001'), Quantity(2), Price(999.99, 'EUR'))
print('✅ Domain + Application funcionando')
"
```

#### 🔄 Próximos pasos:
- **Infrastructure Layer**: InMemory repositories, static pricing
- **HTTP Layer**: FastAPI endpoints  
- **Composition Root**: Dependency injection container

### 🎯 Flujo de Desarrollo Recomendado

1. **🔍 Validar**: `python scripts/dev.py` (estructura + tests)
2. **💻 Desarrollar**: Hacer cambios en cualquier parte del proyecto  
3. **🧪 Verificar**: `python scripts/dev.py` (validar cambios)
4. **📝 Commitear**: `git add . && git commit -m "mensaje"`
5. **🚀 Push**: `git push`

O usar el workflow automatizado: `wf-dev-push-unitest` que hace todo en un comando.

## 🤝 Contribuciones

Este es un proyecto educativo. Si encuentras mejoras o tienes sugerencias, ¡son bienvenidas!

## 📚 Referencias

- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architecture Book](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)

---

⭐ **¿Te está ayudando este proyecto?** ¡Dale una estrella en GitHub!

📝 **Documentando el aprendizaje paso a paso** - Cada commit representa un concepto aprendido