#!/usr/bin/env python3
import re

ruta = "/home/sergiof/proyectos/todolist-waybar-module-python/todolist.md"

try:
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    for i, linea in enumerate(lineas):
        if re.match(r"\s*[-*]\s+\[ \]\s+.*", linea):
            lineas[i] = re.sub(r"\[ \]", "[x]", linea, count=1)
            break

    with open(ruta, "w", encoding="utf-8") as f:
        f.writelines(lineas)

    import subprocess
    subprocess.run(["notify-send", "✔️ Tarea completada"])
except Exception as e:
    # Para debugging
    with open("/tmp/check_next_error.log", "w") as f:
        f.write(str(e))