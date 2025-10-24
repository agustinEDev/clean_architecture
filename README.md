# 🏗️ Clean Architecture Learning Project

> Un proyecto educativo paso a paso para aprender Clean Architecture implementando un sistema de gestión de usuarios en Python y TypeScript.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.0+-blue.svg)](https://typescriptlang.org)
[![Tests](https://img.shields.io/badge/Tests-✅%20Passing-green.svg)](#testing)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-brightgreen.svg)](#arquitectura)

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

Implementar el **mismo sistema de gestión de usuarios** en dos lenguajes diferentes para entender cómo Clean Architecture es **independiente del lenguaje** y las **ventajas** que proporciona.

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
│   └── dev.py              # Script inteligente para validación y tests
├── python_version/          # 🐍 Implementación en Python
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
├── typescript_version/      # 🔷 Implementación en TypeScript (EN DESARROLLO)
│   ├── src/                # 📂 Código fuente
│   │   └── shared/         # 🔧 Utilidades compartidas
│   │       └── health.ts   # Health check para verificar el tooling
│   ├── tests/              # 🧪 Tests unitarios con Vitest
│   │   └── shared/
│   │       └── health.spec.ts
│   ├── main.ts             # Punto de entrada de la aplicación
│   ├── package.json        # Dependencias y scripts de Node.js
│   ├── tsconfig.json       # Configuración de TypeScript
│   └── vitest.config.ts    # Configuración de tests
├── README.md               # 📖 Documentación completa
└── .gitignore              # 🙈 Configuración Git
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

## 🔷 Implementación en TypeScript (EN DESARROLLO)

### 🚀 Configuración y Tooling

La versión TypeScript está configurada con un stack moderno de desarrollo:

- **TypeScript 5.9.3**: Tipado estático y compilación
- **tsx 4.20.6**: Ejecución rápida de TypeScript sin compilación previa
- **Vitest 4.0.2**: Framework de testing moderno y rápido
- **ES Modules**: Configuración moderna con import/export
- **Node.js Types**: Soporte completo para APIs de Node.js

### 📂 Estado Actual

#### ✅ Completado:
- **Health Check System**: Sistema trivial de verificación de salud
- **Tooling Setup**: Configuración completa de desarrollo y testing
- **Project Structure**: Estructura base organizada por capas
- **Testing Framework**: Vitest configurado con cobertura completa

#### 🔧 Health Check (`src/shared/health.ts`):
```typescript
// Interface para el estado de salud
export interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  timestamp: Date;
  uptime: number;
  service: string;
}

// Función principal de health check
export function getHealthStatus(serviceName?: string): HealthStatus;

// Verificación de disponibilidad del servicio
export function isServiceReady(): boolean;
```

### 🧪 Testing TypeScript

```bash
# Ejecutar tests una vez
cd typescript_version
npm test

# Ejecutar tests en modo watch (desarrollo)
npm run test:watch

# Ejecutar código directamente con tsx
npm run dev

# Compilar TypeScript a JavaScript
npm run build

# Ejecutar código compilado
npm start
```

### 📋 Próximos Pasos (TypeScript):
- [ ] **Value Objects**: Implementar DNI y User entity
- [ ] **Domain Layer**: Entidades de dominio equivalentes a Python
- [ ] **Use Cases**: Casos de uso CRUD con inyección de dependencias
- [ ] **Repository Pattern**: Interfaces y implementaciones
- [ ] **Infrastructure**: Adaptadores para persistencia
- [ ] **Testing**: Cobertura completa por capas como en Python

### 🎯 Objetivo de la Implementación TypeScript:
Demostrar que **Clean Architecture es independiente del lenguaje** implementando exactamente la misma funcionalidad CRUD con la misma estructura de capas, pero aprovechando las ventajas específicas de TypeScript:
- **Type Safety**: Prevención de errores en tiempo de compilación
- **Interfaces explícitas**: Contratos claros entre capas
- **Modern Tooling**: Desarrollo eficiente con hot reload y testing rápido

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

### 🔷 TypeScript Implementation - 🚧 EN DESARROLLO
- [x] **Project Setup**: Configuración completa de desarrollo
  - ✅ TypeScript 5.9.3 + tsx 4.20.6 para ejecución rápida
  - ✅ Vitest 4.0.2 para testing moderno
  - ✅ ES Modules con import/export
  - ✅ Configuración tsconfig.json optimizada
  - ✅ Scripts de desarrollo (dev, build, test, test:watch)
- [x] **Health Check System**: Sistema de verificación trivial
  - ✅ Interface HealthStatus con tipos estrictos
  - ✅ Funciones getHealthStatus() e isServiceReady()
  - ✅ 10 tests unitarios con cobertura completa
  - ✅ Verificación de tooling y compilación

### 📋 Próximos Pasos - Python
- [ ] **Interactive CLI**: Menú interactivo para operaciones CRUD
- [ ] **Controllers Layer**: Capa de presentación con interfaz de usuario
- [ ] **Input Validation**: Validación mejorada de entrada de usuario
- [ ] **Error Handling**: Manejo de errores más robusto en la interfaz
- [ ] **Configuration**: Sistema de configuración (archivo, variables de entorno)
- [ ] **Logging**: Sistema de logging para auditoría y debugging
- [ ] **Database Integration**: Migrar de JSON a SQLite/PostgreSQL
- [ ] **API REST**: Capa de API HTTP con Flask/FastAPI

### 📋 Próximos Pasos - TypeScript
- [ ] **Value Objects**: Implementar DNI validation y User entity en TypeScript
- [ ] **Domain Layer**: Entidades equivalentes con tipado estático
- [ ] **Use Cases**: Casos de uso CRUD con interfaces TypeScript
- [ ] **Repository Pattern**: Contratos e implementaciones tipadas
- [ ] **Infrastructure**: Adaptadores de persistencia
- [ ] **Testing**: Cobertura completa por capas
- [ ] **Main Application**: Aplicación funcional equivalente a Python

### 📋 Mejoras Futuras (Ambas Implementaciones)
- [ ] **Controllers**: Capa de presentación (CLI interactiva/Web)
- [ ] **External**: Base de datos real (SQLite/PostgreSQL)
- [ ] **Comparación entre lenguajes**: Análisis detallado de diferencias y similitudes
- [ ] **Performance Benchmarks**: Comparativa de rendimiento
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

# Opción 1: Validación completa + tests (RECOMENDADO)
python scripts/dev.py

# Opción 2: Solo ejecutar la aplicación CRUD
cd python_version
python main.py

# Opción 3: Solo ejecutar tests
cd python_version
python -m unittest discover tests/ -v

# Opción 4: Desarrollo con workflow automatizado (requiere Warp Drive)
wf-dev-push-unitest  # Valida, testea, commitea y hace push automáticamente
```

### 🔷 TypeScript Version (EN DESARROLLO)
```bash
# Navegar al proyecto TypeScript
cd typescript_version

# Instalar dependencias (solo la primera vez)
npm install

# Ejecutar health check (verificar tooling)
npm run dev

# Ejecutar tests
npm test

# Ejecutar tests en modo watch (desarrollo)
npm run test:watch

# Compilar a JavaScript
npm run build

# Ejecutar código compilado
npm start
```

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