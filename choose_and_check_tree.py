#!/usr/bin/env python3
import re
import sys

archivo = "/home/sergiof/proyectos/todolist-waybar-module-python/todolist-tree.md"

class Nodo:
    def __init__(self, texto, nivel, checked, linea_idx):
        self.texto = texto
        self.nivel = nivel
        self.checked = checked
        self.linea_idx = linea_idx
        self.hijos = []
        self.padre = None

def parsear_tareas(lineas):
    nodos = []
    stack = []

    for idx, linea in enumerate(lineas):
        # Detectar checkbox con niveles según indentación (espacios o tabs)
        m = re.match(r"^(\s*)[-*]\s+\[( |x)\]\s+(.*)", linea)
        if not m:
            continue

        indent, check, texto = m.groups()
        nivel = len(indent) // 4  # Asumiendo 4 espacios por nivel

        nodo = Nodo(texto.strip(), nivel, check == "x", idx)

        # Insertar en el árbol
        while stack and stack[-1].nivel >= nivel:
            stack.pop()

        if stack:
            nodo.padre = stack[-1]
            stack[-1].hijos.append(nodo)

        stack.append(nodo)
        nodos.append(nodo)

    return nodos

def buscar_primera_tarea_pendiente(nodos):
    # DFS: recorrer y devolver primer nodo no marcado (hoja o padre)
    def dfs(nodo):
        if not nodo.checked:
            # Si tiene hijos, verificar si todos están marcados
            if nodo.hijos:
                for hijo in nodo.hijos:
                    res = dfs(hijo)
                    if res:
                        return res
            else:
                return nodo
        return None

    for nodo in nodos:
        if nodo.padre is None:  # raíz
            res = dfs(nodo)
            if res:
                return res
    return None

def marcar_tarea(lineas, nodos, texto_seleccionado):
    # Marcar la tarea seleccionada y sus padres si corresponde
    # Buscar nodo por texto exacto
    nodo_obj = None
    for n in nodos:
        if n.texto == texto_seleccionado:
            nodo_obj = n
            break
    if not nodo_obj:
        print("No se encontró la tarea seleccionada.", file=sys.stderr)
        return False

    # Marcar nodo como hecho (en el archivo)
    linea = lineas[nodo_obj.linea_idx]
    nueva_linea = re.sub(r"\[ \]", "[x]", linea, count=1)
    lineas[nodo_obj.linea_idx] = nueva_linea

    # Actualizar estado en memoria
    nodo_obj.checked = True

    # Subir recursivamente y marcar padres si todos sus hijos están marcados
    padre = nodo_obj.padre
    while padre:
        if all(h.checked for h in padre.hijos):
            # Marcar padre en archivo y memoria
            linea_padre = lineas[padre.linea_idx]
            nueva_linea_padre = re.sub(r"\[ \]", "[x]", linea_padre, count=1)
            lineas[padre.linea_idx] = nueva_linea_padre
            padre.checked = True
            padre = padre.padre
        else:
            break

    return True

def main():
    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nodos = parsear_tareas(lineas)

    # Si se llamó con argumento, es para marcar esa tarea
    if len(sys.argv) > 1:
        tarea_a_marcar = sys.argv[1]
        exito = marcar_tarea(lineas, nodos, tarea_a_marcar)
        if exito:
            with open(archivo, "w", encoding="utf-8") as f:
                f.writelines(lineas)
        else:
            sys.exit(1)
        sys.exit(0)

    # Si no, mostrar la primera tarea pendiente
    primera = buscar_primera_tarea_pendiente(nodos)
    if primera:
        print(primera.texto)
    else:
        print("✅ Todo listo")

if __name__ == "__main__":
    main()
