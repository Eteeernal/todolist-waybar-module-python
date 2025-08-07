# 📝 Todolist Waybar Module for HyDE

Módulo personalizado para Waybar que gestiona listas de tareas desde la barra de estado en el entorno HyDE (Hyprland Desktop Environment).

## 📂 Estructura del Proyecto

```
todolist-waybar-module-python/
├── 📁 scripts/                     # Scripts del módulo
│   ├── 📜 current.py               # Script principal - muestra tarea actual
│   ├── 📜 choose_and_check.py      # Interfaz rofi para selección
│   └── 🧪 test.py                  # Suite de pruebas
├── 🚀 install.py                   # Instalador automático
├── 🗑️  uninstall.py                # Desinstalador automático
├── 🔄 restart-config.py            # Reiniciador de configuración
├── 📄 todolist.md                  # Archivo de tareas
├── 📖 README.md                    # Esta documentación
├── 📋 MODULE_README.md             # Documentación técnica detallada
└── 📁 .vscode/                     # Configuración del editor
```

## 🎯 Características del Módulo

### ✨ **Funcionalidad Unificada**
- 📝 **Tareas simples**: Funciona perfecto con listas de 1 nivel
- 🌳 **Tareas jerárquicas**: Soporte completo para estructuras anidadas
- 🔄 **Propagación automática**: Completar subtareas → completar padre automáticamente
- 🎯 **Detección inteligente**: Encuentra la primera tarea trabajable

### 🛠️ **Integración Completa**
- ✅ Instalación completamente automática
- ✅ Detección automática del usuario y layout
- ✅ Integración nativa con HyDE waybar
- ✅ Interfaz rofi para selección manual
- ✅ Tooltips informativos jerárquicos
- ✅ Notificaciones de progreso
- ✅ **Cambio dinámico de archivos markdown**

## 🚀 Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone <repo-url> todolist-waybar-module-python
cd todolist-waybar-module-python

# 2. Verificar sistema
./scripts/test.py                # Verificar dependencias

# 3. Instalar automáticamente
./install.py                     # Instalación completa automática

# 4. ¡Listo! El módulo aparece automáticamente en waybar
```

## 🎯 Casos de Uso

### **📚 Múltiples Proyectos**
```bash
# Proyecto A: Desarrollo
echo "/home/user/proyectos/desarrollo.md" > ~/.local/share/todolist/config.txt

# Proyecto B: Universidad  
echo "/home/user/universidad/tareas.md" > ~/.local/share/todolist/config.txt

# Cambio dinámico desde rofi: "📁 Cambiar archivo markdown..."
```

### **🏠 Organización Personal**
- `~/tareas-casa.md` - Tareas domésticas
- `~/trabajo.md` - Tareas laborales  
- `~/proyectos.md` - Proyectos personales

**El instalador automáticamente:**
- ✅ Detecta tu usuario (`sergiof.jsonc`)
- ✅ Busca o crea tu layout personalizado
- ✅ Instala scripts en `~/.local/bin/`
- ✅ Configura el módulo waybar
- ✅ Actualiza includes.json
- ✅ Integra el módulo en tu layout

## 📄 Formato de Tareas

### **Tareas Simples (1 nivel)**
```markdown
# Mi Lista de Tareas
- [ ] Comprar leche
- [ ] Llamar al médico
- [x] Revisar emails
- [ ] Hacer ejercicio
```

### **Tareas Jerárquicas (multi-nivel)**
```markdown
# Proyecto Complejo
- [ ] Desarrollo Web
    - [ ] Frontend
        - [ ] Diseño UI
        - [ ] Implementar CSS
    - [ ] Backend
        - [ ] API Rest
        - [x] Base de datos
- [ ] Testing
    - [ ] Unit tests
```

**🔄 Propagación Automática**: Cuando completas todas las subtareas, el padre se marca automáticamente como completado.

## 🎮 Uso del Módulo

### **Interacción en Waybar**
- **🖱️ Click izquierdo/derecho**: Abrir interfaz rofi de selección
- **💡 Tooltip**: Ver estructura completa de tareas pendientes
- **📝 Icono**: Muestra la primera tarea trabajable

### **Menú Contextual Rofi**
- **📁 Cambiar archivo markdown...**: Múltiples opciones de selección
  - **🔍 Buscar en archivos encontrados**: Lista visual de archivos .md
  - **📝 Escribir ruta manualmente**: Con autocompletado de directorios
  - **📁 Abrir administrador de archivos**: Integración gráfica
  - **⏰ Archivos recientes**: Historial automático de uso
- **📄 Ver archivo actual...**: Información del archivo activo
- **🔲 Tareas pendientes**: Seleccionar y marcar tareas
- **📊 Navegación intuitiva**: Iconos contextuales y rutas relativas

### **Edición y Gestión de Tareas**

#### **📁 Cambiar Archivo Dinámicamente**

**🎯 Desde Rofi (Recomendado):**
1. Click en waybar → "📁 Cambiar archivo markdown..."
2. Seleccionar método:
   - **🔍 Buscar en archivos encontrados** - Lista automática
   - **📝 Escribir ruta manualmente** - Con autocompletado
   - **📁 Abrir administrador de archivos** - Visual/gráfico  
   - **⏰ Archivos recientes** - Historial de uso

**⚡ Manual (Avanzado):**
```bash
echo "/path/to/mi-proyecto.md" > ~/.local/share/todolist/config.txt
```

#### **📄 Edición Manual**
```bash
# Editar archivo actual
nano ~/.local/share/todolist/todolist.md

# Ver qué archivo está activo
~/.local/bin/choose_and_check.py  # → "📄 Ver archivo actual..."
```

#### **🔧 Comandos Directos**
```bash
~/.local/bin/current.py                # Ver primera tarea del archivo activo
~/.local/bin/current.py "nombre tarea" # Marcar tarea específica  
~/.local/bin/choose_and_check.py       # Interfaz rofi completa
```

### **Gestión del Módulo**

#### **🔄 Reiniciar Configuración**
```bash
# Reinicio interactivo (recomendado)
./restart-config.py

# Reinicio automático sin confirmación  
./restart-config.py --force

# Reinicio silencioso
./restart-config.py --quiet
```

#### **🗑️ Desinstalación**
```bash
# Desinstalación interactiva
./uninstall.py

# Desinstalación automática
./uninstall.py --force --quiet
```

## 🔧 Troubleshooting

### **Si el módulo no aparece**
```bash
# 1. Regenerar configuración
~/.local/lib/hyde/waybar.py --generate-includes
~/.local/lib/hyde/waybar.py --update

# 2. Aplicar layout
hyde-shell waybar -S

# 3. Verificar logs
journalctl --user -u waybar -f
```

### **Verificar funcionamiento**
```bash
./scripts/test.py    # Diagnóstico completo del sistema
```

### **Problemas comunes**
- **Módulo no visible**: Verificar que está en tu layout activo
- **Error de rutas**: Reinstalar con `./install.py`
- **Sin permisos**: Verificar que scripts son ejecutables

## 📖 Documentación Adicional

- **[MODULE_README.md](MODULE_README.md)**: Documentación técnica detallada
- **Configuración waybar**: Se crea automáticamente en `~/.config/waybar/modules/`
- **Datos de usuario**: Almacenados en `~/.local/share/todolist/`

## 🎯 **Ventajas del Módulo Unificado**

1. **🔀 Versatilidad**: Un solo módulo para tareas simples y complejas
2. **🚀 Instalación**: Completamente automática con detección inteligente
3. **🎨 Integración**: Nativa con HyDE siguiendo mejores prácticas  
4. **🔄 Propagación**: Lógica automática jerárquica avanzada
5. **🧹 Limpieza**: Desinstalación completa sin residuos

## 🤝 Contribuir

1. **🐛 Reportar bugs**: Abre un issue con detalles
2. **💡 Sugerir mejoras**: Propón nuevas características  
3. **🔧 Contribuir código**: Fork → Branch → PR
4. **📖 Mejorar docs**: Ayuda con documentación

## 📄 Licencia

Este proyecto es open source. Libre para usar, modificar y distribuir.

---

**🎨 Hecho para la comunidad HyDE con ❤️**

Módulo todolist unificado que **funciona perfecto tanto para tareas simples como jerárquicas**.
