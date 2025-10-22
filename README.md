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

## 🐍 Implementación en Python

### 📁 Estructura del Proyecto

```
python_version/
├── entities/                 # 🎯 Entidades del negocio
│   └── users.py             # Clase User con validaciones
├── use_cases/               # 💼 Casos de uso
│   ├── user_repository_interface.py
│   └── create_user_use_case.py
├── adapters/                # 🔌 Adaptadores
│   ├── repositories/        # Acceso a datos
│   └── controllers/         # Control de entrada
├── external/                # 🌐 Capa externa
│   └── database/           # Base de datos simulada
├── tests/                   # 🧪 Tests por capa
│   ├── test_entities/
│   └── test_use_cases/
└── main.py                  # Punto de entrada
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

### 🔍 Características Técnicas

#### Validación de DNI
- ✅ Formato: 8 números + 1 letra
- ✅ Algoritmo de verificación español
- ✅ Cálculo del dígito de control

#### Principios SOLID
- **Single Responsibility**: Cada clase tiene una responsabilidad
- **Dependency Inversion**: Los Use Cases dependen de abstracciones
- **Interface Segregation**: Interfaces específicas y pequeñas

## 🧪 Testing

### Estrategia de Testing por Capas

```bash
# Ejecutar tests de entidades
python tests/test_entities/test_user.py

# Ejecutar tests de casos de uso
python tests/test_use_cases/test_create_user_use_case.py
```

### 🎭 Test Doubles
- **InMemoryUserRepository**: Implementación en memoria para testing
- **Casos válidos e inválidos**: Cobertura completa de escenarios
- **Testing aislado**: Cada capa se testea independientemente

## 📈 Progreso del Proyecto

### ✅ Completado
- [x] **Entities**: User con validación completa
- [x] **Use Cases**: CreateUserUseCase
- [x] **Repository Interface**: Contrato definido
- [x] **Testing**: Tests unitarios para entities y use cases

### 🚧 En Progreso
- [ ] **Use Cases adicionales**: FindUser, ListUsers, UpdateUser, DeleteUser
- [ ] **Adapters**: Controladores y repositorio real
- [ ] **External**: Base de datos simulada
- [ ] **Main**: Aplicación completa funcionando

### 📋 Pendiente
- [ ] **Implementación en TypeScript**
- [ ] **Comparación entre lenguajes**
- [ ] **Documentación de patrones aprendidos**

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
- ✅ **Testabilidad**: Cada capa se puede testear aisladamente
- ✅ **Mantenibilidad**: Cambios localizados por responsabilidad
- ✅ **Flexibilidad**: Fácil cambiar implementaciones
- ✅ **Comprensibilidad**: Estructura clara y predecible

## 🚀 Cómo ejecutar el proyecto

```bash
# Clonar el repositorio
git clone <tu-repo>
cd CleanArchitecture

# Ejecutar tests
cd python_version
python tests/test_entities/test_user.py
python tests/test_use_cases/test_create_user_use_case.py

# (Próximamente) Ejecutar la aplicación
python main.py
```

## 🤝 Contribuciones

Este es un proyecto educativo. Si encuentras mejoras o tienes sugerencias, ¡son bienvenidas!

## 📚 Referencias

- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architecture Book](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)

---

⭐ **¿Te está ayudando este proyecto?** ¡Dale una estrella en GitHub!

📝 **Documentando el aprendizaje paso a paso** - Cada commit representa un concepto aprendido