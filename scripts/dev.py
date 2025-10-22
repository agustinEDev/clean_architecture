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
        "python_version/adapters/": "🔌 Adaptadores"
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
    
    # Contar archivos de test
    python_tests = Path("python_version/tests")
    if python_tests.exists():
        test_files = list(python_tests.rglob("test_*.py"))
        print(f"🧪 Archivos de test Python: {len(test_files)}")
    
    # Contar casos de uso
    use_cases = Path("python_version/use_cases")
    if use_cases.exists():
        use_case_files = list(use_cases.glob("*_use_case.py"))
        print(f"💼 Casos de uso implementados: {len(use_case_files)}")
    
    # Verificar archivos de datos
    users_json = Path("python_version/users.json")
    if users_json.exists():
        print("💾 users.json: ✅ Datos existentes")
    else:
        print("💾 users.json: ⚪ Sin datos")
    
    # Verificar documentación
    readme = Path("README.md")
    if readme.exists():
        lines = len(readme.read_text().splitlines())
        print(f"� README.md: ✅ {lines} líneas de documentación")

def run_python_tests():
    """Ejecuta todos los tests de Python"""
    print("\n🧪 Ejecutando Tests de Python...")
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
            print("✅ Todos los tests de Python pasaron!")
            return True
        else:
            print("❌ Algunos tests de Python fallaron.")
            return False
            
    finally:
        # Volver al directorio original
        os.chdir(original_cwd)

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
        tests_passed = run_python_tests()
    else:
        print("\n❌ Estructura del proyecto incorrecta, saltando tests...")
        tests_passed = False
    
    # Resultado final
    print("\n" + "=" * 70)
    if structure_ok and tests_passed:
        print("🎉 DEV MODE: ¡Proyecto completo y todos los tests pasan!")
        print("🚀 Listo para commit y push")
        sys.exit(0)
    else:
        print("🔧 DEV MODE: Revisar errores antes de continuar")
        if not structure_ok:
            print("   - Estructura del proyecto incompleta")
        if structure_ok and not tests_passed:
            print("   - Tests fallando")
        sys.exit(1)

if __name__ == "__main__":
    main()
    main()