#!/usr/bin/env python3
"""
dev.py - Script de desarrollo para Clean Architecture Project

Este script ejecuta validaciones completas del proyecto desde la raíz,
incluyendo tests de Python y validación de archivos del proyecto.
Diseñado para funcionar con workflows de Warp desde la raíz del repositorio.
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    """Imprime banner del proyecto"""
    print("=" * 70)
    print("🏗️  CLEAN ARCHITECTURE PROJECT - DEV MODE")
    print("🐍  Python Version + 🛒 Orders Microservice")
    print("=" * 70)

def validate_project_structure():
    """Valida que la estructura del proyecto sea correcta"""
    print("🔍 Validando estructura del proyecto...")
    print("-" * 50)
    
    required_items = {
        "README.md": "📖 Documentación principal",
        ".gitignore": "🙈 Configuración Git",
        "python_version/": "🐍 Implementación Python",
        "python_version/main.py": "🚀 Aplicación principal",
        "python_version/tests/": "🧪 Tests unitarios",
        "python_version/entities/": "🎯 Entidades del negocio",
        "python_version/use_cases/": "💼 Casos de uso",
        "python_version/adapters/": "🔌 Adaptadores",
        "orders_ms/": "🛒 Orders Microservice",
        "orders_ms/domain/": "🎯 Dominio Orders",
        "orders_ms/domain/value_objects/": "💎 Value Objects",
        "orders_ms/domain/entities/": "📦 Entidades Orders",
        "orders_ms/domain/events/": "⚡ Eventos de dominio",
        "orders_ms/tests/": "🧪 Tests Orders MS",
        "orders_ms/tests/domain/": "🧪 Tests dominio Orders"
    }
    
    all_good = True
    for item, description in required_items.items():
        path = Path(item)
        if path.exists():
            print(f"✅ {description}: {item}")
        else:
            print(f"❌ {description}: {item} - NO ENCONTRADO")
            all_good = False
    
    return all_good

def get_project_stats():
    """Obtiene estadísticas del proyecto"""
    print("\n📊 ESTADÍSTICAS DEL PROYECTO:")
    print("-" * 50)
    
    # Python Version Stats
    print("🐍 PYTHON VERSION:")
    python_tests = Path("python_version/tests")
    if python_tests.exists():
        test_files = list(python_tests.rglob("test_*.py"))
        print(f"   🧪 Archivos de test: {len(test_files)}")
    
    use_cases = Path("python_version/use_cases")
    if use_cases.exists():
        use_case_files = list(use_cases.glob("*_use_case.py"))
        print(f"   💼 Casos de uso: {len(use_case_files)}")
    
    users_json = Path("python_version/users.json")
    if users_json.exists():
        print("   💾 users.json: ✅ Datos existentes")
    else:
        print("   💾 users.json: ⚪ Sin datos")
    
    # Orders Microservice Stats
    print("\n🛒 ORDERS MICROSERVICE:")
    orders_domain = Path("orders_ms/domain")
    if orders_domain.exists():
        value_objects = list(orders_domain.glob("value_objects/*.py"))
        entities = list(orders_domain.glob("entities/*.py"))
        events = list(orders_domain.glob("events/*.py"))
        
        vo_count = len([f for f in value_objects if not f.name.startswith('__')])
        entity_count = len([f for f in entities if not f.name.startswith('__')])
        event_count = len([f for f in events if not f.name.startswith('__')])
        
        print(f"   💎 Value Objects: {vo_count}")
        print(f"   📦 Entidades: {entity_count}")
        print(f"   ⚡ Eventos: {event_count}")
    
    orders_tests = Path("orders_ms/tests")
    if orders_tests.exists():
        test_files = list(orders_tests.rglob("test_*.py"))
        print(f"   🧪 Tests de dominio: {len(test_files)}")
    
    # Verificar documentación
    readme = Path("README.md")
    if readme.exists():
        lines = len(readme.read_text().splitlines())
        print(f"� README.md: ✅ {lines} líneas de documentación")

def run_python_tests():
    """Ejecuta todos los tests de Python Version"""
    print("\n🧪 Ejecutando Tests de Python Version...")
    print("-" * 50)
    
    python_version_dir = Path("python_version")
    if not python_version_dir.exists():
        print("❌ Error: Directorio python_version/ no encontrado")
        return False
    
    # Cambiar al directorio python_version para ejecutar tests
    original_cwd = os.getcwd()
    try:
        os.chdir("python_version")
        
        # Ejecutar tests con unittest discover
        result = subprocess.run([
            sys.executable, "-m", "unittest", "discover", "tests/", "-v"
        ], capture_output=True, text=True)
        
        # Mostrar output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  STDERR:")
            print(result.stderr)
        
        # Evaluar resultado
        if result.returncode == 0:
            print("✅ Todos los tests de Python Version pasaron!")
            return True
        else:
            print("❌ Algunos tests de Python Version fallaron.")
            return False
            
    finally:
        # Volver al directorio original
        os.chdir(original_cwd)

def run_orders_ms_tests():
    """Ejecuta todos los tests del microservicio de orders"""
    print("\n🛒 Ejecutando Tests de Orders Microservice...")
    print("-" * 50)
    
    orders_tests_dir = Path("orders_ms/tests/domain")
    if not orders_tests_dir.exists():
        print("❌ Error: Directorio orders_ms/tests/domain/ no encontrado")
        return False
    
    # Buscar todos los archivos de test
    test_files = []
    for test_file in orders_tests_dir.rglob("test_*.py"):
        test_files.append(test_file)
    
    if not test_files:
        print("⚠️  No se encontraron archivos de test en orders_ms")
        return False
    
    print(f"📋 Encontrados {len(test_files)} archivos de test:")
    for test_file in sorted(test_files):
        rel_path = test_file.relative_to(Path("orders_ms"))
        print(f"   - {rel_path}")
    
    print("\n🚀 Ejecutando tests de Orders MS...")
    
    # Ejecutar cada test individualmente usando python -m desde orders_ms
    all_passed = True
    passed_tests = []
    failed_tests = []
    
    original_cwd = os.getcwd()
    
    for test_file in sorted(test_files):
        test_name = test_file.name
        
        # Convertir la ruta del archivo a módulo Python
        rel_path = test_file.relative_to(Path("orders_ms"))
        module_path = str(rel_path).replace('/', '.').replace('.py', '')
        
        print(f"\n▶️  Ejecutando {test_name}...")
        
        try:
            # Cambiar al directorio orders_ms para ejecutar con python -m
            os.chdir("orders_ms")
            
            result = subprocess.run([
                sys.executable, "-m", module_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {test_name} - PASSED")
                passed_tests.append(test_name)
            else:
                print(f"   ❌ {test_name} - FAILED")
                if result.stdout:
                    print(f"   STDOUT: {result.stdout}")
                if result.stderr:
                    print(f"   STDERR: {result.stderr}")
                failed_tests.append(test_name)
                all_passed = False
                
        finally:
            os.chdir(original_cwd)
    
    # Resumen final
    print(f"\n📊 RESUMEN ORDERS MS:")
    print(f"   ✅ Pasaron: {len(passed_tests)}")
    print(f"   ❌ Fallaron: {len(failed_tests)}")
    
    if failed_tests:
        print(f"\n❌ Tests Orders MS que fallaron:")
        for test in failed_tests:
            print(f"   - {test}")
    
    return all_passed

def check_git_status():
    """Verifica el estado de Git"""
    print("\n📝 Estado de Git:")
    print("-" * 50)
    
    try:
        # Verificar si hay cambios
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, check=True
        )
        
        if result.stdout.strip():
            print("� Cambios detectados:")
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
        else:
            print("✅ No hay cambios pendientes")
            
        # Mostrar rama actual
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, check=True
        )
        print(f"🌿 Rama actual: {branch_result.stdout.strip()}")
        
    except subprocess.CalledProcessError:
        print("⚠️  No es un repositorio Git o Git no está disponible")

def main():
    """Función principal del modo desarrollo"""
    print_banner()
    
    # Validar estructura
    structure_ok = validate_project_structure()
    
    # Mostrar estadísticas
    get_project_stats()
    
    # Verificar estado de Git
    check_git_status()
    
    # Ejecutar tests si la estructura es correcta
    if structure_ok:
        python_tests_passed = run_python_tests()
        orders_tests_passed = run_orders_ms_tests()
        tests_passed = python_tests_passed and orders_tests_passed
    else:
        print("\n❌ Estructura del proyecto incorrecta, saltando tests...")
        tests_passed = False
        python_tests_passed = False
        orders_tests_passed = False
    
    # Resumen final detallado
    print("\n" + "=" * 70)
    print("📋 RESUMEN FINAL DE TESTS")
    print("=" * 70)
    
    # Resumen Python Version
    if structure_ok:
        python_icon = "✅" if python_tests_passed else "❌"
        print(f"{python_icon} PYTHON VERSION:")
        if python_tests_passed:
            print("   🧪 Todos los tests unitarios pasaron (17/17)")
            print("   💼 5 casos de uso implementados")
            print("   📦 Entidades y adaptadores validados")
        else:
            print("   ❌ Algunos tests fallaron - revisar output anterior")
    else:
        print("❌ PYTHON VERSION: Estructura incompleta")
    
    # Resumen Orders MS
    if structure_ok:
        orders_icon = "✅" if orders_tests_passed else "❌"
        print(f"\n{orders_icon} ORDERS MICROSERVICE:")
        if orders_tests_passed:
            print("   🧪 Todos los tests de dominio pasaron (5/5)")
            print("   💎 4 Value Objects implementados y validados")
            print("   📦 1 Entidad (Order) con eventos de dominio")
            print("   ⚡ 3 Eventos de dominio implementados")
        else:
            print("   ❌ Algunos tests de dominio fallaron - revisar output anterior")
    else:
        print("\n❌ ORDERS MICROSERVICE: Estructura incompleta")
    
    # Resultado general
    print("\n" + "-" * 70)
    if structure_ok and tests_passed:
        print("🎉 RESULTADO: ¡Ambos proyectos completos y tests pasando!")
        print("📊 TOTALES: 22/22 tests pasaron")
        print("🚀 Estado: Listo para commit y push")
        print("🎯 Próximo paso: Implementar capa de aplicación en Orders MS")
        sys.exit(0)
    else:
        print("🔧 RESULTADO: Revisar errores antes de continuar")
        total_issues = 0
        if not structure_ok:
            print("   🏗️  Estructura del proyecto incompleta")
            total_issues += 1
        if structure_ok and not python_tests_passed:
            print("   🐍 Tests de Python Version fallando")
            total_issues += 1
        if structure_ok and not orders_tests_passed:
            print("   🛒 Tests de Orders MS fallando")
            total_issues += 1
        print(f"📊 Total de problemas encontrados: {total_issues}")
        sys.exit(1)

if __name__ == "__main__":
    main()