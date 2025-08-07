# 🌳 Todolist Tree Module (Experimental)

Módulo experimental para Waybar que gestiona listas de tareas con estructura jerárquica desde archivos markdown.

## ✅ **Estado: Funcional pero Experimental**

Este módulo está **funcionando correctamente** con las características principales implementadas. Sin embargo, se considera experimental porque carece de instalación automática y algunas características avanzadas. Para uso en producción con instalación completa, se recomienda el [módulo todolist principal](../todolist/).

## 📂 Archivos del Módulo

```
todolist-tree/
├── 📜 tree.py                      # Script principal del módulo (✅ CORREGIDO)
├── 📜 choose_and_check_tree.py     # Interfaz rofi para selección (✅ FUNCIONAL)
├── 📄 todolist-tree.md             # Archivo de tareas con estructura de árbol
├── 🧪 test_tree_module.py          # Script de pruebas (🆕 NUEVO)
└── 📖 README.md                    # Esta documentación
```

## 🎯 Características

### ✅ **Funcionalidades Completamente Implementadas**
- 🌳 **Estructura jerárquica de tareas** con propagación automática
- 📄 **Soporte para markdown** con niveles anidados (espacios y tabs)
- 🔄 **Propagación automática**: cuando se completan todas las subtareas, se marca automáticamente el padre
- 🎯 **Detección inteligente** de la primera tarea trabajable (DFS optimizado)
- 📊 **Salida JSON** compatible con waybar
- 💡 **Tooltip jerárquico** mostrando todas las tareas pendientes
- 🖱️ **Interfaz rofi** para selección manual de tareas
- 📱 **Notificaciones** de progreso y errores

### 🚧 **Pendiente de Implementar**
- ⚙️ Script de instalación automática (estilo HyDE)
- 🎨 Integración completa con el sistema de módulos HyDE
- 📦 Configuración JSONC para waybar
- 🎨 Estilos CSS específicos

## 📄 Formato del Archivo de Tareas

El archivo `todolist-tree.md` utiliza una estructura jerárquica:

```markdown
# Lista de tareas con estructura

## Proyecto A
- [ ] Tarea principal 1
  - [ ] Subtarea 1.1
  - [ ] Subtarea 1.2
- [x] Tarea completada

## Proyecto B  
- [ ] Tarea principal 2
  - [ ] Subtarea 2.1
    - [ ] Sub-subtarea 2.1.1
```

## 🚀 Uso del Módulo

### **1. Verificar Funcionamiento**
```bash
cd todolist-tree/
./test_tree_module.py    # Ejecutar pruebas completas
./tree.py               # Probar script principal
```

### **2. Configuración Manual en Waybar**
Agregar a tu configuración de waybar (ej. `~/.config/waybar/modules/custom-todolist-tree.jsonc`):

```json
{
  "custom/todolist-tree": {
    "format": "🌳 {}",
    "exec": "/home/TU_USUARIO/proyectos/todolist-waybar-module-python/todolist-tree/tree.py",
    "interval": 5,
    "return-type": "json",
    "tooltip": true,
    "on-click": "/home/TU_USUARIO/proyectos/todolist-waybar-module-python/todolist-tree/choose_and_check_tree.py",
    "on-click-right": "/home/TU_USUARIO/proyectos/todolist-waybar-module-python/todolist-tree/choose_and_check_tree.py"
  }
}
```

### **3. Usar las Funciones**
```bash
# Editar tareas
nano todolist-tree.md

# Marcar tarea específica 
./tree.py "nombre de la tarea"

# Interfaz rofi (click derecho en waybar)
./choose_and_check_tree.py
```

### **4. Ejemplo de Uso de Propagación Automática**

**Archivo inicial:**
```markdown
- [ ] Proyecto Web
    - [ ] Frontend
        - [ ] Diseño UI
        - [ ] Implementar CSS
    - [ ] Backend
        - [ ] API Rest
        - [ ] Base de datos
```

**Marcar "Diseño UI":**
```bash
./tree.py "Diseño UI"
```

**Marcar "Implementar CSS":**
```bash
./tree.py "Implementar CSS"
```

**Resultado automático:**
```markdown
- [ ] Proyecto Web
    - [x] Frontend         # ✅ Auto-completado!
        - [x] Diseño UI
        - [x] Implementar CSS
    - [ ] Backend
        - [ ] API Rest
        - [ ] Base de datos
```

## 🔧 Desarrollo

### **Roadmap**
- [ ] Script de instalación automática
- [ ] Mejores interacciones de usuario
- [ ] Integración con HyDE
- [ ] Soporte para múltiples archivos
- [ ] Configuración de colores por nivel

### **Contribuir**
Este módulo está abierto a contribuciones. Las áreas que necesitan desarrollo:

1. **📦 Instalación**: Sistema automático como el módulo principal
2. **🎨 UI/UX**: Mejor visualización jerárquica
3. **⚙️ Configuración**: Opciones personalizables
4. **🧪 Testing**: Pruebas automatizadas

## 🔗 Módulos Relacionados

- **[Todolist Principal](../todolist/)**: Versión estable y recomendada
- **[Documentación General](../README.md)**: Información del proyecto completo

## ⚠️ Limitaciones Actuales

- ⚙️ **Sin instalación automática** (requiere configuración manual)
- 📦 **Sin integración HyDE** (no usa el sistema de módulos estándar)
- 🎨 **Sin estilos CSS** predefinidos
- 🔧 **Rutas hardcodeadas** en configuración waybar

## ✅ Problemas Solucionados

- ✅ **Rutas fijas corregidas**: Ahora usa rutas relativas
- ✅ **Script duplicado**: `choose_and_check_tree.py` ahora tiene funcionalidad rofi específica
- ✅ **Lógica DFS mejorada**: Algoritmo optimizado para encontrar tareas trabajables
- ✅ **Soporte multi-indentación**: Funciona con espacios y tabs
- ✅ **Salida JSON**: Compatible con waybar `return-type: "json"`
- ✅ **Propagación automática**: Funciona correctamente en todos los niveles
- ✅ **Tooltips informativos**: Muestra jerarquía completa
- ✅ **Manejo de errores**: Crea archivo inicial si no existe

## 🤝 Soporte

Para bugs específicos del módulo tree:
1. Verifica que los scripts tengan permisos de ejecución
2. Revisa el formato del archivo `todolist-tree.md`
3. Consulta logs de waybar: `journalctl --user -u waybar -f`

Para uso en producción, considera usar el [módulo todolist principal](../todolist/) que tiene todas las características implementadas.

---

**🌳 Desarrollado como extensión experimental del proyecto todolist-waybar-module**
