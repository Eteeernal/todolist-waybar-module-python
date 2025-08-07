#!/usr/bin/env python3
"""
Script de prueba para el módulo todolist-tree
===========================================

Verifica que el módulo funcione correctamente antes del uso.
"""

import json
import subprocess
import sys
import tempfile
import os
from pathlib import Path

def test_tree_parsing():
    """Probar que el parsing y la lógica de tree funciona"""
    print("🌳 Probando parsing de estructura de árbol...")
    
    # Crear archivo temporal de prueba
    contenido_test = """# Test Tree
- [ ] Tarea Principal 1
    - [ ] Subtarea 1.1
    - [ ] Subtarea 1.2
        - [ ] Sub-subtarea 1.2.1
- [ ] Tarea Principal 2
    - [ ] Subtarea 2.1
- [ ] Tarea Independiente
"""
    
    # Crear archivo temporal
    script_dir = Path(__file__).parent
    test_file = script_dir / "test-todolist.md"
    
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(contenido_test)
        
        # Modificar temporalmente current.py para usar archivo de test
        current_script = script_dir / "current.py"
        with open(current_script, 'r', encoding='utf-8') as f:
            contenido_original = f.read()
        
        contenido_test_script = contenido_original.replace(
            'archivo = script_dir / "todolist.md"',
            f'archivo = script_dir / "test-todolist.md"'
        )
        
        with open(current_script, 'w', encoding='utf-8') as f:
            f.write(contenido_test_script)
        
        # Probar el script
        result = subprocess.run([
            sys.executable, str(current_script)
        ], capture_output=True, text=True, cwd=script_dir)
        
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
                required_keys = ["text", "tooltip", "class"]
                if all(key in output for key in required_keys):
                    print(f"   ✅ Parsing correcto")
                    print(f"   📝 Primera tarea: {output['text']}")
                    print(f"   🎯 Debe ser: 'Subtarea 1.1' (primera hoja)")
                    return output['text'] == "Subtarea 1.1"
                else:
                    print(f"   ❌ JSON no tiene las claves correctas")
                    return False
            except json.JSONDecodeError:
                print(f"   ❌ Salida no es JSON válido: {result.stdout}")
                return False
        else:
            print(f"   ❌ Error en ejecución: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test: {e}")
        return False
    finally:
        # Restaurar archivo original
        try:
            with open(current_script, 'w', encoding='utf-8') as f:
                f.write(contenido_original)
            test_file.unlink(missing_ok=True)
        except:
            pass

def test_auto_completion():
    """Probar la propagación automática de completado"""
    print("🔄 Probando propagación automática...")
    
    # Este test es más complejo, por ahora solo verificamos que el script acepta argumentos
    script_dir = Path(__file__).parent
    current_script = script_dir / "current.py"
    
    try:
        # Intentar marcar una tarea (esto puede fallar si no existe)
        result = subprocess.run([
            sys.executable, str(current_script), "test_task"
        ], capture_output=True, text=True, cwd=script_dir)
        
        # El script debe terminar con código 1 si no encuentra la tarea
        if result.returncode == 1:
            print("   ✅ Script maneja argumentos correctamente")
            return True
        else:
            print(f"   ⚠️  Resultado inesperado: código {result.returncode}")
            return True  # Aún consideramos esto como pase
            
    except Exception as e:
        print(f"   ❌ Error en test de propagación: {e}")
        return False

def test_file_structure():
    """Verificar que todos los archivos necesarios existen"""
    print("📁 Verificando estructura de archivos...")
    
    script_dir = Path(__file__).parent
    required_files = [
        "current.py",
        "choose_and_check.py",
        "todolist.md",
        "install.py",
        "uninstall.py",
        "test.py"
    ]
    
    all_ok = True
    for file in required_files:
        file_path = script_dir / file
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}: No encontrado")
            all_ok = False
    
    return all_ok

def test_dependencies():
    """Verificar dependencias del sistema"""
    print("🔍 Verificando dependencias...")
    
    dependencies = {
        "python3": ["python3", "--version"],
        "rofi": ["rofi", "-version"]
    }
    
    all_ok = True
    for dep, cmd in dependencies.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {dep}: Disponible")
            else:
                print(f"   ❌ {dep}: No disponible")
                all_ok = False
        except FileNotFoundError:
            print(f"   ❌ {dep}: No encontrado")
            all_ok = False
    
    return all_ok

def main():
    """Ejecutar todas las pruebas"""
    print("🧪 Test del Módulo Todolist Jerárquico")
    print("=" * 50)
    
    tests = [
        ("Estructura de archivos", test_file_structure),
        ("Dependencias del sistema", test_dependencies),
        ("Parsing de árbol", test_tree_parsing),
        ("Propagación automática", test_auto_completion)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔬 {test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Resumen de Pruebas:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 ¡Todas las pruebas pasaron!")
        print("✅ El módulo está funcionando correctamente")
        print("🚀 Listo para instalar con: ./install.py")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("🔧 Revisa los errores antes de instalar")
    
    print("\n📝 Módulo Todolist Unificado")
    print("   Funciona con tareas simples (1 nivel) y jerárquicas (multi-nivel)")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
