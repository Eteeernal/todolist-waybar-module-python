#!/usr/bin/env python3
"""
Script de instalación automática para el módulo todolist-tree
============================================================

Este script instala automáticamente el módulo todolist-tree siguiendo las 
mejores prácticas de HyDE para módulos waybar.

Características:
- Detecta automáticamente el nombre de usuario
- Busca o crea el layout específico del usuario (usuario.jsonc)
- Instala scripts en ~/.local/bin/
- Crea la configuración del módulo en waybar
- Actualiza automáticamente includes.json
- Integra el módulo en el layout del usuario
"""

import os
import shutil
import json
import subprocess
import sys
import re
from pathlib import Path
from getpass import getuser

class HyDETodolistInstaller:
    def __init__(self):
        self.user = getuser()
        self.project_dir = Path(__file__).parent
        self.home = Path.home()
        self.config_waybar = self.home / ".config" / "waybar"
        self.local_bin = self.home / ".local" / "bin"
        self.modules_dir = self.config_waybar / "modules"
        self.layouts_dir = self.config_waybar / "layouts"
        self.includes_file = self.config_waybar / "includes" / "includes.json"
        
        # Layout específico del usuario
        self.user_layout = self.layouts_dir / f"{self.user}.jsonc"
        
        # Archivos del módulo todolist
        self.scripts = [
            "scripts/current.py",
            "scripts/choose_and_check.py"
        ]
        
        # Configuración del módulo
        self.module_config = {
            "custom/todolist": {
                "format": "📝 {}",
                "exec": str(self.local_bin / "current.py"),
                "interval": 5,
                "return-type": "json",
                "tooltip": True,
                "on-click": str(self.local_bin / "choose_and_check.py"),
                "on-click-right": str(self.local_bin / "choose_and_check.py")
            }
        }

    def check_dependencies(self):
        """Verificar dependencias necesarias"""
        print("🔍 Verificando dependencias...")
        
        dependencies = {
            "HyDE waybar.py": self.home / ".local" / "lib" / "hyde" / "waybar.py",
            "Directorio waybar": self.config_waybar,
            "Directorio modules": self.modules_dir,
            "Directorio layouts": self.layouts_dir
        }
        
        missing = []
        for name, path in dependencies.items():
            if path.exists():
                print(f"   ✅ {name}: Encontrado")
            else:
                print(f"   ❌ {name}: No encontrado en {path}")
                missing.append(name)
        
        if missing:
            print(f"\n❌ Dependencias faltantes: {', '.join(missing)}")
            print("   Este script requiere HyDE instalado y configurado")
            return False
        
        return True

    def create_directories(self):
        """Crear directorios necesarios"""
        print("📁 Creando directorios...")
        
        directories = [
            self.local_bin,
            self.modules_dir,
            self.layouts_dir,
            self.config_waybar / "includes",
            self.home / ".local" / "share" / "todolist"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {directory}")

    def install_scripts(self):
        """Instalar scripts en ~/.local/bin/"""
        print("📜 Instalando scripts...")
        
        missing_scripts = []
        
        for script in self.scripts:
            src = self.project_dir / script
            # Solo usar el nombre del archivo para el destino, no la ruta completa
            script_name = Path(script).name
            dst = self.local_bin / script_name
            
            if not src.exists():
                print(f"   ❌ Script no encontrado: {src}")
                missing_scripts.append(script)
                continue
                
            # Copiar script y actualizar rutas
            content = src.read_text(encoding='utf-8')
            
            # Actualizar ruta del archivo de tareas
            old_path = 'script_dir / "todolist.md"'
            new_path = f'Path.home() / ".local" / "share" / "todolist" / "todolist.md"'
            content = content.replace(old_path, new_path)
            
            # Escribir script actualizado
            dst.write_text(content, encoding='utf-8')
            dst.chmod(0o755)
            
            print(f"   ✅ {script} → {dst}")
        
        if missing_scripts:
            print(f"   ⚠️  Scripts faltantes: {', '.join(missing_scripts)}")
            return False
        
        return True

    def setup_data_file(self):
        """Configurar archivo de datos de tareas"""
        print("📄 Configurando archivo de tareas...")
        
        data_dir = self.home / ".local" / "share" / "todolist"
        data_file = data_dir / "todolist.md"
        
        if not data_file.exists():
            # Crear archivo inicial
            initial_content = """# Lista de tareas con estructura

- [ ] Proyecto Principal 1
    - [ ] Subtarea 1.1
        - [ ] Sub-subtarea 1.1.1
        - [ ] Sub-subtarea 1.1.2
    - [ ] Subtarea 1.2
- [ ] Proyecto Principal 2
    - [ ] Subtarea 2.1
- [ ] Tarea Independiente
"""
            data_file.write_text(initial_content, encoding='utf-8')
            print(f"   ✅ Archivo inicial creado: {data_file}")
        else:
            print(f"   ✅ Archivo existente: {data_file}")

    def create_waybar_module(self):
        """Crear configuración del módulo para waybar"""
        print("🧩 Creando módulo waybar...")
        
        module_file = self.modules_dir / "custom-todolist.jsonc"
        
        # Escribir configuración
        with open(module_file, 'w', encoding='utf-8') as f:
            json.dump(self.module_config, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Módulo creado: {module_file}")

    def detect_or_create_user_layout(self):
        """Detectar o crear el layout del usuario"""
        print(f"🎨 Procesando layout del usuario: {self.user}.jsonc...")
        
        if self.user_layout.exists():
            print(f"   ✅ Layout existente encontrado: {self.user_layout}")
            return self.update_existing_layout()
        else:
            print(f"   📝 Creando nuevo layout: {self.user_layout}")
            return self.create_new_layout()

    def update_existing_layout(self):
        """Actualizar layout existente añadiendo el módulo tree"""
        try:
            with open(self.user_layout, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parsear JSON con comentarios (JSONC)
            # Remover comentarios para parsing
            json_content = re.sub(r'//.*?\n', '\n', content)
            json_content = re.sub(r'/\*.*?\*/', '', json_content, flags=re.DOTALL)
            
            layout = json.loads(json_content)
            
            # Verificar si ya existe el módulo
            modules_to_check = []
            
            # Buscar en todos los grupos
            for key, value in layout.items():
                if isinstance(value, dict) and "modules" in value:
                    modules_to_check.extend(value["modules"])
            
            if "custom/todolist" in modules_to_check:
                print("   ⚠️  Módulo custom/todolist ya existe en el layout")
                return True
            
            # Crear grupo dedicado para todolist
            tree_group = "group/pill#todolist"
            
            # Verificar si el grupo ya existe
            if tree_group in layout:
                if "custom/todolist" not in layout[tree_group]["modules"]:
                    layout[tree_group]["modules"].append("custom/todolist")
                    print(f"   ✅ Módulo añadido al grupo existente: {tree_group}")
                else:
                    print(f"   ⚠️  Módulo ya existe en grupo: {tree_group}")
            else:
                # Crear nuevo grupo todolist
                layout[tree_group] = {
                    "orientation": "inherit",
                    "modules": ["custom/todolist"]
                }
                
                # Añadir grupo a modules-left si existe
                if "modules-left" in layout:
                    if tree_group not in layout["modules-left"]:
                        layout["modules-left"].append(tree_group)
                        print(f"   ✅ Grupo añadido a modules-left: {tree_group}")
                else:
                    # Crear modules-left si no existe
                    layout["modules-left"] = [tree_group]
                    print(f"   ✅ modules-left creado con grupo: {tree_group}")
                
                print(f"   ✅ Nuevo grupo todolist creado: {tree_group}")
            
            # Guardar layout actualizado preservando formato JSONC
            updated_json = json.dumps(layout, indent=4, ensure_ascii=False)
            with open(self.user_layout, 'w', encoding='utf-8') as f:
                f.write(updated_json)
            
            print(f"   ✅ Layout actualizado: {self.user_layout}")
            return True
            
        except Exception as e:
            print(f"   ❌ Error actualizando layout: {e}")
            return False

    def create_new_layout(self):
        """Crear nuevo layout básico con el módulo tree"""
        try:
            # Layout básico inspirado en la estructura existente
            new_layout = {
                "layer": "top",
                "output": ["*"],
                "height": 10,
                "exclusive": True,
                "passthrough": False,
                "reload_style_on_change": True,
                "include": [
                    "$XDG_CONFIG_HOME/waybar/modules/*json*",
                    "$XDG_CONFIG_HOME/waybar/includes/includes.json"
                ],
                "modules-left": [
                    "group/pill#todolist"
                ],
                "group/pill#todolist": {
                    "orientation": "inherit",
                    "modules": [
                        "custom/todolist"
                    ]
                },
                "modules-center": [
                    "group/pill#center"
                ],
                "group/pill#center": {
                    "modules": [
                        "hyprland/workspaces",
                        "hyprland/window"
                    ],
                    "orientation": "inherit"
                },
                "modules-right": [
                    "group/pill#right1"
                ],
                "group/pill#right1": {
                    "modules": [
                        "clock",
                        "battery"
                    ],
                    "orientation": "inherit"
                }
            }
            
            with open(self.user_layout, 'w', encoding='utf-8') as f:
                json.dump(new_layout, f, indent=4, ensure_ascii=False)
            
            print(f"   ✅ Nuevo layout creado: {self.user_layout}")
            return True
            
        except Exception as e:
            print(f"   ❌ Error creando layout: {e}")
            return False

    def update_waybar_includes(self):
        """Actualizar includes.json usando waybar.py de HyDE"""
        print("🔄 Actualizando configuración de waybar...")
        
        try:
            waybar_py = self.home / ".local" / "lib" / "hyde" / "waybar.py"
            
            # Regenerar includes.json
            subprocess.run([
                str(waybar_py), "--generate-includes"
            ], check=True, capture_output=True, text=True)
            
            print("   ✅ includes.json actualizado")
            
            # Verificar que el módulo está incluido
            if self.includes_file.exists():
                with open(self.includes_file, 'r') as f:
                    content = f.read()
                    if "custom-todolist.jsonc" in content:
                        print("   ✅ Módulo todolist detectado en includes.json")
                    else:
                        print("   ⚠️  Módulo no detectado en includes.json")
            
            # Actualizar configuración completa
            subprocess.run([
                str(waybar_py), "--update"
            ], check=True, capture_output=True, text=True)
            
            print("   ✅ Configuración waybar sincronizada")
            
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Error al actualizar waybar: {e}")
            print("      Ejecuta manualmente:")
            print("      ~/.local/lib/hyde/waybar.py --generate-includes")
            print("      ~/.local/lib/hyde/waybar.py --update")

    def show_completion_message(self):
        """Mostrar mensaje de finalización"""
        print("\n🎉 ¡Instalación del módulo todolist-tree completada!")
        print("=" * 60)
        print("📋 Resumen de la instalación:")
        print()
        print(f"   👤 Usuario detectado: {self.user}")
        print(f"   📄 Layout utilizado: {self.user_layout}")
        print(f"   📜 Scripts instalados en: {self.local_bin}")
        print(f"   📁 Datos de tareas en: ~/.local/share/todolist/")
        print(f"   🧩 Módulo waybar: custom/todolist")
        print()
        print("🎮 Cómo usar:")
        print("   • El módulo aparecerá automáticamente en waybar")
        print("   • Click izquierdo: Abrir interfaz rofi")
        print("   • Click derecho: Abrir interfaz rofi")
        print("   • Tooltip: Ver estructura completa de tareas")
        print()
        print("📝 Editar tareas:")
        print(f"   nano ~/.local/share/todolist/todolist.md")
        print()
        print("🔧 Comandos directos:")
        print(f"   {self.local_bin}/current.py                    # Ver primera tarea")
        print(f"   {self.local_bin}/current.py \"nombre tarea\"     # Marcar tarea")
        print(f"   {self.local_bin}/choose_and_check.py           # Interfaz rofi")
        print()
        print("🔄 Para aplicar cambios de layout:")
        print("   hyde-shell waybar -S    # Selector interactivo")
        print("   # o")
        print("   ~/.local/lib/hyde/waybar.py --update")
        print()
        print("🎯 Características del módulo todolist:")
        print("   ✅ Estructura jerárquica de tareas")
        print("   ✅ Propagación automática (completar subtareas → completar padre)")
        print("   ✅ Funciona con tareas simples (1 nivel) y complejas (multi-nivel)")
        print("   ✅ Interfaz rofi integrada")
        print("   ✅ Tooltips informativos")
        print("   ✅ Integración completa con HyDE")

    def run(self):
        """Ejecutar instalación completa"""
        print("📝 Instalador del Módulo Todolist para HyDE")
        print("=" * 60)
        
        try:
            if not self.check_dependencies():
                sys.exit(1)
            
            self.create_directories()
            
            if not self.install_scripts():
                print("❌ Error: No se pudieron instalar todos los scripts")
                sys.exit(1)
            
            self.setup_data_file()
            self.create_waybar_module()
            self.detect_or_create_user_layout()
            self.update_waybar_includes()
            self.show_completion_message()
            
        except Exception as e:
            print(f"❌ Error durante la instalación: {e}")
            sys.exit(1)

if __name__ == "__main__":
    installer = HyDETodolistInstaller()
    installer.run()
