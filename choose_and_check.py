#!/usr/bin/env python3
import re
import subprocess

ruta = "/home/sergiof/proyectos/todolist-waybar-module-python/todolist.md"

try:
    # Leer archivo
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Extraer tareas sin marcar
    pendientes = []
    indices = []
    for i, linea in enumerate(lineas):
        match = re.match(r"\s*[-*]\s+\[ \]\s+(.*)", linea)
        if match:
            pendientes.append(match.group(1).strip())
            indices.append(i)

    if not pendientes:
        subprocess.run(["notify-send", "🎉 No hay tareas pendientes"])
        exit(0)

    # Mostrar lista con rofi
    rofi = subprocess.run(
        ["rofi", "-dmenu", "-p", "Marcar tarea como completada:"],
        input="\n".join(pendientes),
        text=True,
        capture_output=True
    )

    seleccionada = rofi.stdout.strip()
    if not seleccionada:
        exit(0)

    # Buscar y marcar la tarea elegida
    for idx in indices:
        if seleccionada in lineas[idx]:
            lineas[idx] = re.sub(r"\[ \]", "[x]", lineas[idx], count=1)
            break

    # Guardar archivo actualizado
    with open(ruta, "w", encoding="utf-8") as f:
        f.writelines(lineas)

    subprocess.run(["notify-send", f"✅ Completada: {seleccionada}"])

except Exception as e:
    subprocess.run(["notify-send", "❌ Error en choose_and_check.py", str(e)])
