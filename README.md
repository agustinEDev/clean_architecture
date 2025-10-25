# 🏗️ Clean Architecture Learning Project

> Un proyecto educativo paso a paso para aprender Clean Architecture implementando:
> - 🐍 **Sistema de gestión de usuarios** (Python - FUNCIONAL)
> - 🛒 **Orders Microservice** (Python - EN DESARROLLO con Domain + Application Layer completado)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-32%2F32%20✅%20Passing-green.svg)](#testing)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-brightgreen.svg)](#arquitectura)
[![Microservices](https://img.shields.io/badge/Microservices-🛒%20Orders%20MS-orange.svg)](#orders-microservice)

## 📚 ¿Qué es Clean Architecture?

Clean Architecture es un patrón de diseño que separa el código en capas concéntricas, donde cada capa tiene una responsabilidad específica y las dependencias apuntan hacia el centro.

```
┌─────────────────────────────────────────────────────────┐
│                    🌐 Frameworks & Drivers              │
│  ┌─────────────────────────────────────────────────┐    │
│  │              🔌 Interface Adapters              │    │
│  │  ┌─────────────────────────────────────────┐    │    │
│  │  │              💼 Use Cases               │    │    │
│  │  │  ┌─────────────────────────────────┐    │    │    │
│  │  │  │          🎯 Entities            │    │    │    │
│  │  │  │                                 │    │    │    │
│  │  │  └─────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Objetivo del Proyecto

Implementar un **sistema de gestión de usuarios** en Python para entender los principios de Clean Architecture y las **ventajas** que proporciona en el desarrollo de software.

### ✨ Características del Sistema
- ✅ Crear usuarios con validación de DNI español
- ✅ Buscar usuarios por DNI
- ✅ Listar todos los usuarios
- ✅ Actualizar información de usuarios
- ✅ Eliminar usuarios

##  Estructura del Proyecto

```
CleanArchitecture/           # 🏗️ Raíz del proyecto
├── scripts/                 # 🛠️ Scripts de desarrollo y CI/CD
│   └── dev.py              # Script inteligente para validación y tests unificados
├── python_version/          # 🐍 Implementación en Python (Sistema de Usuarios)
│   ├── entities/           # 🎯 Entidades del negocio
│   │   └── users.py        # Clase User con validaciones
│   ├── use_cases/          # 💼 Casos de uso
│   │   ├── user_repository_interface.py
│   │   ├── create_user_use_case.py
│   │   ├── find_user_use_case.py
│   │   ├── list_users_use_case.py
│   │   ├── update_user_use_case.py
│   │   └── delete_user_use_case.py
│   ├── adapters/           # 🔌 Adaptadores
│   │   └── repositories/   # Acceso a datos
│   │       └── file_user_repository.py
│   ├── tests/              # 🧪 Tests completos por capa
│   │   ├── test_entities/
│   │   ├── test_use_cases/
│   │   └── test_adapters/
│   └── main.py             # Aplicación principal funcional
├── orders_ms/              # 🛒 Orders Microservice (Clean Architecture)
│   ├── domain/             # 🎯 Capa de Dominio
│   │   ├── entities/       # 📦 Entidades del negocio
│   │   │   └── order.py    # Order con factory methods y eventos
│   │   ├── value_objects/  # 💎 Value Objects inmutables
│   │   │   ├── price.py    # Price con Decimal y validación currency
│   │   │   ├── sku.py      # SKU con normalización y validación
│   │   │   ├── quantity.py # Quantity con rangos válidos
│   │   │   └── order_id.py # OrderId con UUID y prefijo
│   │   └── events/         # ⚡ Eventos de dominio
│   │       ├── domain_event.py   # Base para eventos
│   │       ├── order_created.py  # Evento orden creada
│   │       └── item_added.py     # Evento item agregado
│   ├── application/        # 💼 Capa de Aplicación (✅ COMPLETADO)
│   │   ├── ports/         # 🔌 Interfaces/Contratos (3 puertos)
│   │   ├── dtos/          # 📋 Data Transfer Objects (4 DTOs)
│   │   └── use_cases/     # 💼 Casos de uso (2 implementados)
│   ├── infrastructure/     # 🔧 Capa de Infraestructura (pendiente)
│   ├── http/              # 🌐 Capa HTTP/API REST (pendiente)
│   ├── config/            # ⚙️ Configuración
│   │   ├── __init__.py    # Exportaciones de configuración
│   │   └── logging_config.py # Sistema completo de logging
│   ├── tests/             # 🧪 Tests unitarios completos (15/15 ✅)
│   │   ├── domain/        # Tests de dominio (11/11 ✅)
│   │   │   ├── entities/  # Tests de entidades
│   │   │   ├── events/    # Tests de eventos
│   │   │   └── value_objects/ # Tests de value objects
│   │   └── application/   # Tests de aplicación (4/4 ✅)
│   │       └── use_cases/ # Tests de casos de uso
│   └── logs/              # 📝 Archivos de log (rotación automática)
├── README.md              # 📖 Documentación completa
└── .gitignore             # 🙈 Configuración Git actualizada
```

## 🐍 Implementación en Python

### 📁 Estructura Detallada

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

## 📈 Progreso del Proyecto

### 🐍 Python Implementation - 🔧 FUNCIONAL (Con potencial de expansión)
- [x] **Entities**: User con validación completa de DNI español
- [x] **Use Cases CRUD Completo**: 
  - ✅ CreateUserUseCase con inyección de dependencias
  - ✅ FindUserUseCase para búsqueda por DNI
  - ✅ ListUsersUseCase para listar todos los usuarios
  - ✅ UpdateUserUseCase para modificar usuarios existentes
  - ✅ DeleteUserUseCase para eliminar usuarios
- [x] **Repository Interface**: Contrato bien definido y desacoplado
- [x] **Adapters**: FileUserRepository con persistencia JSON formateada
- [x] **Testing Completo**: 
  - ✅ Tests unitarios para User (casos válidos/inválidos)
  - ✅ Tests para todos los Use Cases con repositorio mock
  - ✅ Tests de casos de éxito y manejo de errores
  - ✅ Tests de integración para FileUserRepository
  - ✅ Tests de persistencia real en archivos
  - ✅ Cobertura completa de operaciones CRUD
- [x] **Aplicación Principal**: Main.py con funcionalidad CRUD completa
- [x] **Mejoras de Calidad**: 
  - ✅ JSON formateado con indentación y caracteres especiales
  - ✅ Manejo consistente de errores
  - ✅ Arquitectura limpia y código mantenible
- [x] **Sistema de Desarrollo y CI/CD**:
  - ✅ Script de desarrollo inteligente (scripts/dev.py)
  - ✅ Validación automática de estructura del proyecto
  - ✅ Ejecución automatizada de tests desde cualquier ubicación
  - ✅ Integración con workflows de automatización (Warp Drive)
  - ✅ Detección de cambios en todo el repositorio
  - ✅ Exit codes apropiados para CI/CD

### � Orders Microservice - 🚧 EN DESARROLLO ACTIVO
- [x] **Domain Layer (COMPLETO)**: Lógica de negocio con eventos
  - ✅ **Value Objects**: Price, SKU, Quantity, OrderId con validaciones completas
  - ✅ **Entities**: Order con factory methods y gestión de items
  - ✅ **Domain Events**: OrderCreated, ItemAdded con DomainEvent base
  - ✅ **Event-Driven Architecture**: Eventos de dominio para comunicación entre capas
- [x] **Testing System (COMPLETO)**: Tests unitarios por componente
  - ✅ 5 tests unitarios con cobertura completa del dominio
  - ✅ Importaciones limpias con módulos Python (__init__.py)
  - ✅ Script dev.py unificado (22/22 tests: Python + Orders MS)
  - ✅ Ejecución con python -m desde raíz del proyecto
- [x] **Logging System (COMPLETO)**: Sistema profesional de trazabilidad
  - ✅ Configuración por niveles (DEBUG, INFO, WARNING, ERROR)
  - ✅ Logging a consola y archivos con rotación automática
  - ✅ Separación por capas (domain, application, infrastructure)
  - ✅ Integración en entidades de dominio para trazabilidad completa
- [x] **Project Structure (COMPLETO)**: Arquitectura limpia y modular
  - ✅ Separación estricta por capas (domain/, application/, infrastructure/, http/)
  - ✅ Módulos Python con __init__.py para importaciones limpias
  - ✅ Configuración centralizada (config/) con logging_config.py
  - ✅ Sistema de logs (logs/) con .gitignore configurado
- [ ] **Application Layer**: Casos de uso y puertos
  - 🔄 CreateOrderUseCase y AddItemToOrderUseCase
  - 🔄 Puertos: OrderRepository, PricingService, EventBus
  - 🔄 DTOs: CreateOrderRequest/Response, AddItemToOrderRequest/Response
- [ ] **Infrastructure Layer**: Adaptadores e implementaciones
  - 🔄 InMemoryOrderRepository para persistencia
  - 🔄 StaticPricingService para precios
  - 🔄 NoOpEventBus para eventos
- [ ] **HTTP Layer**: API REST con FastAPI
  - 🔄 POST /orders - Crear nueva orden
  - 🔄 POST /orders/{orderId}/items - Agregar item a orden
- [ ] **Composition Root**: Inyección de dependencias
  - 🔄 container.py para composición de objetos
  - 🔄 Configuración de dependencias

###  Próximos Pasos - Python Version
- [ ] **Interactive CLI**: Menú interactivo para operaciones CRUD
- [ ] **Controllers Layer**: Capa de presentación con interfaz de usuario
- [ ] **Input Validation**: Validación mejorada de entrada de usuario
- [ ] **Error Handling**: Manejo de errores más robusto en la interfaz
- [ ] **Configuration**: Sistema de configuración (archivo, variables de entorno)
- [ ] **Database Integration**: Migrar de JSON a SQLite/PostgreSQL
- [ ] **API REST**: Capa de API HTTP con Flask/FastAPI

### 📋 Próximos Pasos - Orders Microservice
- [ ] **Application Layer**: Completar capa de aplicación
  - [ ] CreateOrderUseCase y AddItemToOrderUseCase
  - [ ] Puertos: OrderRepository, PricingService, EventBus interfaces
  - [ ] DTOs para requests y responses
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