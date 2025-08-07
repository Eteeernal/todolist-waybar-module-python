#!/usr/bin/env python3
import os
import re
import json

# Ruta a tu archivo markdown
archivo = "/home/sergiof/proyectos/todolist-waybar-module-python/todolist.md"

primera_pendiente = None
pendientes = []

try:
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            match = re.match(r"\s*[-*]\s+\[ \]\s+(.*)", linea)
            if match:
                tarea = match.group(1).strip()
                pendientes.append(tarea)
                if not primera_pendiente:
                    primera_pendiente = tarea

    if not primera_pendiente:
        primera_pendiente = "✅ Todo listo"
        tooltip = "¡No hay tareas pendientes!"
    else:
        tooltip = "\n".join([f"[ ] {t}" for t in pendientes])

    output = {
        "text": primera_pendiente,
        "tooltip": tooltip,
        "class": "todo"
    }

    print(json.dumps(output), flush=True)

except Exception as e:
    print(json.dumps({
        "text": "⚠️ Error",
        "tooltip": str(e),
        "class": "error"
    }), flush=True)
