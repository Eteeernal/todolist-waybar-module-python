#!/usr/bin/env python3
"""
Script para reiniciar la configuración del módulo todolist
Automatiza el proceso: uninstall.py + install.py

Uso:
    ./restart-config.py                # Reinicio con confirmación
    ./restart-config.py --force        # Reinicio automático sin confirmación
    ./restart-config.py --quiet        # Reinicio silencioso
    ./restart-config.py --help         # Mostrar ayuda
"""

import sys
import subprocess
import argparse
from pathlib import Path
import time

class ModuleRestarter:
    def __init__(self, force=False, quiet=False):
        self.force = force
        self.quiet = quiet
        self.project_dir = Path(__file__).parent
        self.uninstall_script = self.project_dir / "uninstall.py"
        self.install_script = self.project_dir / "install.py"
        
    def print_message(self, message, is_error=False):
        """Imprimir mensaje solo si no está en modo silencioso"""
        if not self.quiet:
            if is_error:
                print(f"❌ {message}", file=sys.stderr)
            else:
                print(f"ℹ️  {message}")
    
    def print_header(self, message):
        """Imprimir encabezado con formato"""
        if not self.quiet:
            print(f"\n🔄 {message}")
            print("=" * (len(message) + 3))
    
    def verificar_scripts(self):
        """Verificar que los scripts necesarios existen"""
        if not self.uninstall_script.exists():
            self.print_message(f"Script de desinstalación no encontrado: {self.uninstall_script}", True)
            return False
            
        if not self.install_script.exists():
            self.print_message(f"Script de instalación no encontrado: {self.install_script}", True)
            return False
            
        self.print_message("✅ Scripts de instalación/desinstalación encontrados")
        return True
    
    def mostrar_confirmacion(self):
        """Mostrar información y pedir confirmación al usuario"""
        if self.force:
            return True
            
        print("\n🔄 REINICIO DE CONFIGURACIÓN DEL MÓDULO TODOLIST")
        print("=" * 50)
        print("Este script realizará las siguientes acciones:")
        print("  1. 🗑️  Desinstalar el módulo actual completamente")
        print("  2. 🧹 Limpiar configuraciones y archivos")
        print("  3. 🚀 Reinstalar el módulo desde cero")
        print("  4. ⚙️  Regenerar configuraciones de waybar")
        print("\n⚠️  NOTA: Se mantendrán tus archivos de tareas markdown")
        print("⚠️  NOTA: El historial de archivos recientes se conservará")
        
        respuesta = input("\n¿Continuar con el reinicio? [s/N]: ").lower().strip()
        return respuesta in ['s', 'si', 'sí', 'y', 'yes']
    
    def ejecutar_comando(self, comando, descripcion):
        """Ejecutar comando y manejar errores"""
        self.print_message(f"Ejecutando: {descripcion}")
        
        try:
            if self.quiet:
                # En modo silencioso, capturar toda la salida
                result = subprocess.run(
                    comando,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return True, ""
            else:
                # En modo normal, mostrar salida en tiempo real
                result = subprocess.run(
                    comando,
                    check=True
                )
                return True, ""
                
        except subprocess.CalledProcessError as e:
            error_msg = f"Error ejecutando {descripcion}"
            if hasattr(e, 'stderr') and e.stderr:
                error_msg += f": {e.stderr}"
            self.print_message(error_msg, True)
            return False, error_msg
        except Exception as e:
            error_msg = f"Error inesperado ejecutando {descripcion}: {e}"
            self.print_message(error_msg, True)
            return False, error_msg
    
    def desinstalar_modulo(self):
        """Ejecutar script de desinstalación"""
        self.print_header("PASO 1: Desinstalando módulo actual")
        
        # Preparar comando de desinstalación
        cmd = [sys.executable, str(self.uninstall_script)]
        if self.force:
            cmd.append("--force")
        if self.quiet:
            cmd.append("--quiet")
            
        exito, error = self.ejecutar_comando(cmd, "Desinstalación del módulo")
        
        if exito:
            self.print_message("✅ Módulo desinstalado correctamente")
            time.sleep(1)  # Pequeña pausa para que los procesos terminen
        
        return exito, error
    
    def instalar_modulo(self):
        """Ejecutar script de instalación"""
        self.print_header("PASO 2: Instalando módulo")
        
        cmd = [sys.executable, str(self.install_script)]
        
        exito, error = self.ejecutar_comando(cmd, "Instalación del módulo")
        
        if exito:
            self.print_message("✅ Módulo instalado correctamente")
        
        return exito, error
    
    def verificar_instalacion(self):
        """Verificar que la instalación fue exitosa"""
        self.print_header("PASO 3: Verificando instalación")
        
        # Verificar archivos clave
        verificaciones = [
            (Path.home() / ".local" / "bin" / "current.py", "Script current.py"),
            (Path.home() / ".local" / "bin" / "choose_and_check.py", "Script choose_and_check.py"),
            (Path.home() / ".config" / "waybar" / "modules" / "custom-todolist.jsonc", "Módulo waybar"),
            (Path.home() / ".local" / "share" / "todolist" / "todolist.md", "Archivo de tareas")
        ]
        
        todos_ok = True
        for archivo, descripcion in verificaciones:
            if archivo.exists():
                self.print_message(f"✅ {descripcion}: OK")
            else:
                self.print_message(f"❌ {descripcion}: NO ENCONTRADO", True)
                todos_ok = False
        
        return todos_ok
    
    def mostrar_resumen_final(self, exito_total, tiempo_total):
        """Mostrar resumen final del proceso"""
        if self.quiet:
            return
            
        print("\n" + "=" * 60)
        if exito_total:
            print("🎉 REINICIO COMPLETADO EXITOSAMENTE")
            print("=" * 60)
            print("✅ Módulo todolist reiniciado correctamente")
            print(f"⏱️  Tiempo total: {tiempo_total:.1f} segundos")
            print("\n📝 El módulo está listo para usar:")
            print("  • Click en waybar para abrir interfaz rofi")
            print("  • Tus archivos de tareas se mantuvieron intactos")
            print("  • Historial de archivos recientes conservado")
        else:
            print("❌ REINICIO FALLÓ")
            print("=" * 60)
            print("⚠️  El reinicio no se completó correctamente")
            print("💡 Puedes intentar ejecutar manualmente:")
            print(f"   1. {self.uninstall_script}")
            print(f"   2. {self.install_script}")
    
    def ejecutar_reinicio(self):
        """Ejecutar el proceso completo de reinicio"""
        inicio = time.time()
        
        # Verificaciones preliminares
        if not self.verificar_scripts():
            return False
        
        # Confirmación del usuario
        if not self.mostrar_confirmacion():
            self.print_message("Reinicio cancelado por el usuario")
            return False
        
        try:
            # Paso 1: Desinstalar
            exito_uninstall, error_uninstall = self.desinstalar_modulo()
            if not exito_uninstall:
                self.print_message(f"Falló la desinstalación: {error_uninstall}", True)
                return False
            
            # Paso 2: Instalar
            exito_install, error_install = self.instalar_modulo()
            if not exito_install:
                self.print_message(f"Falló la instalación: {error_install}", True)
                return False
            
            # Paso 3: Verificar
            exito_verificacion = self.verificar_instalacion()
            if not exito_verificacion:
                self.print_message("La verificación encontró problemas", True)
                return False
            
            tiempo_total = time.time() - inicio
            self.mostrar_resumen_final(True, tiempo_total)
            return True
            
        except KeyboardInterrupt:
            self.print_message("\nReinicio interrumpido por el usuario", True)
            return False
        except Exception as e:
            self.print_message(f"Error inesperado durante el reinicio: {e}", True)
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Reiniciar configuración del módulo todolist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  ./restart-config.py            # Reinicio con confirmación
  ./restart-config.py --force    # Reinicio automático sin preguntar
  ./restart-config.py --quiet    # Reinicio silencioso
  
Este script automatiza el proceso de desinstalar y reinstalar 
el módulo todolist para waybar, útil para:
  • Resolver problemas de configuración
  • Aplicar cambios después de actualizaciones
  • Limpiar y reiniciar la configuración

NOTA: Tus archivos de tareas markdown se mantienen intactos.
        """
    )
    
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Ejecutar reinicio sin pedir confirmación"
    )
    
    parser.add_argument(
        "--quiet", 
        action="store_true", 
        help="Ejecutar en modo silencioso (sin output detallado)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="restart-config.py 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Crear y ejecutar el reiniciador
    restarter = ModuleRestarter(force=args.force, quiet=args.quiet)
    exito = restarter.ejecutar_reinicio()
    
    # Código de salida apropiado
    sys.exit(0 if exito else 1)

if __name__ == "__main__":
    main()
