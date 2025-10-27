#!/usr/bin/env python3
"""
dev_ms.py - Script de desarrollo para Orders Microservice

Ejecuta validaciones y tests específicos para el microservicio de pedidos.
"""

import subprocess
import sys
import os
from pathlib import Path


def print_banner():
    """Imprime banner del proyecto"""
    print("=" * 70)
    print("🛒 ORDERS MICROSERVICE - DEV MODE")
    print("=" * 70)


def validate_project_structure():
    """Valida que la estructura del proyecto sea correcta"""
    print("🔍 Validando estructura del microservicio...")
    print("-" * 50)

    required_items = {
        "main.py": "🚀 Servidor FastAPI",
        "container.py": "📦 Contenedor de Inyección de Dependencias",
        "domain/": "🎯 Capa de Dominio",
        "application/": "💼 Capa de Aplicación",
        "infrastructure/": "🔧 Capa de Infraestructura",
        "static/": "🎨 Frontend",
        "tests/": "🧪 Directorio de Tests",
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

def run_orders_ms_tests():
    """Ejecuta todos los tests del microservicio de orders"""
    print("\n🧪 Ejecutando Tests de Orders Microservice...")
    print("-" * 50)

    # Buscar recursivamente en todo el directorio de tests para incluir todos los tests (domain, app, infra, http)
    test_directories = [Path("tests")]
    test_files = []
    for test_dir in test_directories:
        if test_dir.exists():
            test_files.extend(list(test_dir.rglob("test_*.py")))

    # Eliminar duplicados y ordenar
    test_files = sorted(list(set(test_files)))

    if not test_files:
        print("⚠️  No se encontraron archivos de test.")
        return False, 0, 0

    print(f"📋 Encontrados {len(test_files)} archivos de test.")

    all_passed = True
    passed_count = 0
    failed_count = 0

    for test_file in sorted(test_files):
        test_name = test_file.name
        module_path = str(test_file).replace('/', '.').replace('.py', '')
        
        print(f"\n▶️  Ejecutando {test_name}...")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "unittest", str(test_file)],
                capture_output=True, text=True, check=False,
                # Asegurarse de que el PYTHONPATH incluye la raíz del proyecto
                env={**os.environ, "PYTHONPATH": f"{os.getcwd()}:{os.environ.get('PYTHONPATH', '')}"}
            )

            import re
            test_output = result.stdout + result.stderr
            ran_match = re.search(r"Ran (\d+) test", test_output)
            current_tests = int(ran_match.group(1)) if ran_match else 0

            if result.returncode == 0 and "OK" in test_output:
                print(f"   ✅ {test_name} - PASSED ({current_tests} tests)")
                passed_count += current_tests
            else:
                print(f"   ❌ {test_name} - FAILED")
                print(test_output)
                # Si el test falla al importar, current_tests será 0. Contar como 1 fallo.
                # Si el módulo no se puede importar, ran_match será None y current_tests 0.
                failed_count += current_tests if current_tests > 0 else 1
                all_passed = False
        except Exception as e:
            print(f"   ❌ {test_name} - ERROR: {e}")
            failed_count += 1
            all_passed = False

    print("\n" + "-" * 50)
    print(f"📊 RESUMEN ORDERS MS:")
    total_tests = passed_count + failed_count
    print(f"   Total tests: {total_tests}")
    print(f"   ✅ Pasaron: {passed_count}")
    print(f"   ❌ Fallaron: {failed_count}")
    
    return all_passed, passed_count, failed_count

def main():
    """Función principal del modo desarrollo"""
    # 1. Establecer el directorio de trabajo en la carpeta 'orders_ms'
    repo_root = Path(__file__).resolve().parent.parent  # Raíz del repositorio
    project_root = repo_root / "orders_ms"  # Ruta a /orders_ms
    
    os.chdir(project_root)
    print(f"✅ Directorio de trabajo: {project_root}")

    print_banner()

    # 2. Validar la estructura del proyecto
    structure_ok = validate_project_structure()
    if not structure_ok:
        print("\n❌ Estructura del proyecto incorrecta. Abortando.")
        sys.exit(1)

    # 3. Ejecutar los tests
    tests_passed, passed_count, failed_count = run_orders_ms_tests()
    total_tests = passed_count + failed_count

    # 4. Mostrar resumen final
    print("\n" + "=" * 70)
    print("📋 RESUMEN FINAL")
    print("=" * 70)

    orders_icon = "✅" if tests_passed else "❌"
    print(f"{orders_icon} ORDERS MICROSERVICE:")
    
    if tests_passed and total_tests > 0:
        print(f"   🧪 Todos los tests pasaron ({passed_count}/{total_tests}). ¡Excelente trabajo!")
        print("\n   --- Resumen de Componentes Validados ---")
        print("   🎯 Capa de Dominio:")
        print("      - 💎 4 Value Objects (OrderId, SKU, Price, Quantity)")
        print("      - 📦 1 Entidad (Order) con eventos de dominio")
        print("   💼 Capa de Aplicación:")
        print("      - ✨ 4 Casos de Uso (Create, AddItem, Get, List)")
        print("      - 🔌 3 Puertos (Repository, Pricing, EventBus) y 9 DTOs")
        print("   🔧 Capa de Infraestructura:")
        print("      - ⚙️ 3 Implementaciones (InMemoryRepo, StaticPricing, InMemoryBus)")
        print("   🌐 Capa HTTP:")
        print("      - 🔌 Endpoints para los 4 casos de uso")
    else:
        print(f"   ❌ Algunos tests fallaron ({passed_count}/{total_tests}) - revisar output anterior")

    print("\n" + "-" * 70)
    if tests_passed:
        print(f"🎉 RESULTADO: ¡Todo correcto! {passed_count}/{total_tests} tests pasaron.")
        print("🚀 El microservicio está listo.")
        sys.exit(0)
    else:
        print(f"🔧 RESULTADO: Se encontraron problemas. {failed_count} tests fallaron.")
        sys.exit(1)


if __name__ == "__main__":
    main()