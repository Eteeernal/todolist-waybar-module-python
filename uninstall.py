#!/usr/bin/env python3
"""
Script de desinstalación del módulo todolist-tree
================================================

Este script elimina completamente el módulo todolist-tree del sistema,
revirtiendo todos los cambios realizados por el instalador.
"""

import os
import shutil
import json
import subprocess
import sys
import re
from pathlib import Path
from getpass import getuser

class HyDETodolistUninstaller:
    def __init__(self):
        self.user = getuser()
        self.home = Path.home()
        self.config_waybar = self.home / ".config" / "waybar"
        self.local_bin = self.home / ".local" / "bin"
        self.modules_dir = self.config_waybar / "modules"
        self.layouts_dir = self.config_waybar / "layouts"
        self.includes_file = self.config_waybar / "includes" / "includes.json"
        
        # Layout específico del usuario
        self.user_layout = self.layouts_dir / f"{self.user}.jsonc"
        
        # Archivos a eliminar
        self.files_to_remove = [
            self.local_bin / "current.py",
            self.local_bin / "choose_and_check.py",
            self.modules_dir / "custom-todolist.jsonc",
        ]
        
        # Directorio de datos (opcional)
        self.data_dir = self.home / ".local" / "share" / "todolist"

    def confirm_uninstall(self):
        """Confirmar desinstalación con el usuario"""
        print("⚠️  Desinstalación del módulo todolist")
        print("=" * 50)
        print("Se eliminarán los siguientes elementos:")
        print()
        
        for file_path in self.files_to_remove:
            if file_path.exists():
                print(f"   🗑️  {file_path}")
        
        if self.data_dir.exists():
            print(f"   📁 {self.data_dir} (OPCIONAL - contiene tus tareas)")
        
        if self.user_layout.exists():
            print(f"   ✏️  Módulo removido de: {self.user_layout}")
        
        print()
        response = input("¿Continuar con la desinstalación? [y/N]: ").lower().strip()
        return response in ['y', 'yes', 'sí', 'si']

    def remove_scripts(self):
        """Eliminar scripts de ~/.local/bin/"""
        print("🗑️  Eliminando scripts...")
        
        removed = []
        for script_path in [self.local_bin / "current.py", self.local_bin / "choose_and_check.py"]:
            if script_path.exists():
                script_path.unlink()
                removed.append(script_path.name)
                print(f"   ✅ Eliminado: {script_path}")
        
        if not removed:
            print("   ℹ️  No se encontraron scripts para eliminar")

    def remove_waybar_module(self):
        """Eliminar configuración del módulo waybar"""
        print("🧩 Eliminando módulo waybar...")
        
        module_file = self.modules_dir / "custom-todolist.jsonc"
        if module_file.exists():
            module_file.unlink()
            print(f"   ✅ Eliminado: {module_file}")
        else:
            print("   ℹ️  Módulo waybar no encontrado")

    def update_user_layout(self):
        """Eliminar el módulo del layout del usuario"""
        print(f"📝 Actualizando layout: {self.user}.jsonc...")
        
        if not self.user_layout.exists():
            print("   ℹ️  Layout del usuario no encontrado")
            return
        
        try:
            with open(self.user_layout, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parsear JSON con comentarios
            json_content = re.sub(r'//.*?\n', '\n', content)
            json_content = re.sub(r'/\*.*?\*/', '', json_content, flags=re.DOTALL)
            
            layout = json.loads(json_content)
            
            # Buscar y eliminar referencias al módulo
            module_removed = False
            empty_groups = []
            
            for key, value in layout.items():
                if isinstance(value, dict) and "modules" in value:
                    if "custom/todolist" in value["modules"]:
                        value["modules"].remove("custom/todolist")
                        module_removed = True
                        print(f"   ✅ Módulo removido de: {key}")
                        
                        # Si el grupo queda vacío, marcarlo para eliminación
                        if len(value["modules"]) == 0:
                            empty_groups.append(key)
            
            # Eliminar grupos vacíos
            for group in empty_groups:
                # Remover de modules-left, modules-center, modules-right
                for module_list_key in ["modules-left", "modules-center", "modules-right"]:
                    if module_list_key in layout and group in layout[module_list_key]:
                        layout[module_list_key].remove(group)
                        print(f"   ✅ Grupo vacío removido de {module_list_key}: {group}")
                
                # Eliminar definición del grupo
                if group in layout:
                    del layout[group]
                    print(f"   ✅ Definición de grupo eliminada: {group}")
            
            if module_removed:
                # Guardar layout actualizado
                updated_json = json.dumps(layout, indent=4, ensure_ascii=False)
                with open(self.user_layout, 'w', encoding='utf-8') as f:
                    f.write(updated_json)
                print(f"   ✅ Layout actualizado: {self.user_layout}")
            else:
                print("   ℹ️  Módulo no encontrado en el layout")
                
        except Exception as e:
            print(f"   ⚠️  Error actualizando layout: {e}")

    def remove_data_directory(self):
        """Eliminar directorio de datos (opcional)"""
        if not self.data_dir.exists():
            print("   ℹ️  Directorio de datos no encontrado")
            return
        
        print(f"📁 Directorio de datos: {self.data_dir}")
        print("   ⚠️  Este directorio contiene tus tareas guardadas")
        
        response = input("¿Eliminar también el directorio de datos? [y/N]: ").lower().strip()
        
        if response in ['y', 'yes', 'sí', 'si']:
            shutil.rmtree(self.data_dir)
            print(f"   ✅ Directorio eliminado: {self.data_dir}")
        else:
            print(f"   ℹ️  Directorio conservado: {self.data_dir}")

    def update_waybar_includes(self):
        """Actualizar includes.json"""
        print("🔄 Actualizando configuración waybar...")
        
        try:
            waybar_py = self.home / ".local" / "lib" / "hyde" / "waybar.py"
            
            if not waybar_py.exists():
                print("   ⚠️  waybar.py de HyDE no encontrado")
                return
            
            # Regenerar includes.json
            subprocess.run([
                str(waybar_py), "--generate-includes"
            ], check=True, capture_output=True, text=True)
            
            print("   ✅ includes.json actualizado")
            
            # Actualizar configuración
            subprocess.run([
                str(waybar_py), "--update"
            ], check=True, capture_output=True, text=True)
            
            print("   ✅ Configuración waybar sincronizada")
            
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Error actualizando waybar: {e}")

    def show_completion_message(self):
        """Mostrar mensaje de finalización"""
        print("\n✅ ¡Desinstalación completada!")
        print("=" * 40)
        print("🧹 El módulo todolist ha sido eliminado del sistema")
        print()
        print("🔄 Para aplicar los cambios:")
        print("   hyde-shell waybar -S    # Selector de layout")
        print("   # o")
        print("   ~/.local/lib/hyde/waybar.py --update")
        print()
        print("💡 Para reinstalar en el futuro:")
        print("   cd /ruta/al/proyecto/todolist/")
        print("   ./install.py")

    def run(self, skip_confirmation=False, quiet=False):
        """Ejecutar desinstalación completa"""
        if not quiet:
            print("📝 Desinstalador del Módulo Todolist")
            print("=" * 50)
        
        if not skip_confirmation and not self.confirm_uninstall():
            if not quiet:
                print("❌ Desinstalación cancelada")
            return False
        
        try:
            if not quiet:
                print("\n🚀 Iniciando desinstalación...")
            
            self.remove_scripts()
            self.remove_waybar_module()
            self.update_user_layout()
            self.remove_data_directory()
            self.update_waybar_includes()
            
            if not quiet:
                self.show_completion_message()
            return True
            
        except Exception as e:
            if not quiet:
                print(f"❌ Error durante la desinstalación: {e}")
            return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Desinstalar módulo todolist",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Ejecutar desinstalación sin pedir confirmación"
    )
    
    parser.add_argument(
        "--quiet", 
        action="store_true", 
        help="Ejecutar en modo silencioso"
    )
    
    args = parser.parse_args()
    
    # Mostrar confirmación solo si no es --force
    if not args.force and not args.quiet:
        print("\n🗑️  DESINSTALACIÓN DEL MÓDULO TODOLIST")
        print("=" * 50)
        print("Se eliminarán:")
        print("  • Scripts de ~/.local/bin")
        print("  • Configuración de waybar")
        print("  • Referencias en layouts")
        print("\n⚠️  Los archivos de tareas (.md) se conservarán")
        
        respuesta = input("\n¿Continuar con la desinstalación? [s/N]: ").lower().strip()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            print("Desinstalación cancelada")
            return False
    
    try:
        uninstaller = HyDETodolistUninstaller()
        success = uninstaller.run(skip_confirmation=args.force, quiet=args.quiet)
        
        if success and not args.quiet:
            print("\n🎉 ¡Desinstalación completada exitosamente!")
            print("============================================================")
            print("✅ El módulo todolist ha sido completamente eliminado")
            print("✅ Configuraciones de waybar limpiadas")
            print("✅ Scripts eliminados de ~/.local/bin")
            print("\n💡 Para reinstalar, ejecuta: ./install.py")
        return success
        
    except KeyboardInterrupt:
        if not args.quiet:
            print("\n\n⚠️  Desinstalación cancelada por el usuario")
        return False
    except Exception as e:
        if not args.quiet:
            print(f"\n❌ Error inesperado durante la desinstalación: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
