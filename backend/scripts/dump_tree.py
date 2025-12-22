"""
README / Manual de uso
======================

dump_tree.py
------------

Script para inspeccionar la estructura de un proyecto desde la carpeta actual
y volcarla a un archivo JSON. Está pensado para análisis arquitectónico
(namespace, capas, organización de código).

FUNCIONALIDADES
----------------
- Recorre todo el árbol de directorios desde la carpeta actual
- Ignora automáticamente: bin/, obj/, .git/
- Genera un JSON con:
  - Carpetas
  - Archivos
  - Tamaño
- Opción --verbose:
  - Incluye contenido de archivos con <= 500 líneas
- Opción --cs-namespaces:
  - Analiza archivos .cs
  - Extrae declaraciones de namespace (file-scoped y clásicas)

USO
----
Desde la carpeta raíz del proyecto:

  python dump_tree.py

Con contenido de archivos pequeños:
  python dump_tree.py --verbose

Analizar namespaces C#:
  python dump_tree.py --cs-namespaces

Todo junto:
  python dump_tree.py --verbose --cs-namespaces --output estructura.json

SALIDA
------
Por defecto genera:
  tree_dump.json

Compatible con Windows.
"""

import os
import json
import argparse
import re

MAX_LINES_VERBOSE = 500
IGNORED_DIRS = {"bin", "obj", ".git"}

NAMESPACE_REGEX = re.compile(
    r'^\s*namespace\s+([A-Za-z0-9_.]+)\s*;?|^\s*namespace\s+([A-Za-z0-9_.]+)',
    re.MULTILINE
)


def extract_cs_namespaces(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            matches = NAMESPACE_REGEX.findall(content)
            namespaces = {m[0] or m[1] for m in matches if (m[0] or m[1])}
            return sorted(namespaces)
    except Exception as e:
        return [f"ERROR: {e}"]


def read_file_if_small(path, verbose):
    if not verbose:
        return None

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            if len(lines) <= MAX_LINES_VERBOSE:
                return {
                    "line_count": len(lines),
                    "content": "".join(lines)
                }
            else:
                return {
                    "line_count": len(lines),
                    "content": None
                }
    except Exception as e:
        return {
            "error": str(e)
        }


def build_tree(base_path, verbose, cs_namespaces):
    tree = {
        "type": "directory",
        "name": os.path.basename(base_path),
        "path": os.path.abspath(base_path),
        "children": []
    }

    try:
        entries = sorted(os.listdir(base_path))
    except Exception as e:
        tree["error"] = str(e)
        return tree

    for entry in entries:
        if entry in IGNORED_DIRS:
            continue

        full_path = os.path.join(base_path, entry)

        if os.path.isdir(full_path):
            tree["children"].append(
                build_tree(full_path, verbose, cs_namespaces)
            )
        else:
            file_info = {
                "type": "file",
                "name": entry,
                "path": full_path,
                "size_bytes": os.path.getsize(full_path)
            }

            if cs_namespaces and entry.lower().endswith(".cs"):
                file_info["cs_namespaces"] = extract_cs_namespaces(full_path)

            file_content = read_file_if_small(full_path, verbose)
            if file_content:
                file_info.update(file_content)

            tree["children"].append(file_info)

    return tree


def main():
    parser = argparse.ArgumentParser(
        description="Dump directory tree to JSON (architecture analysis friendly)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include file contents for files with <= 500 lines"
    )
    parser.add_argument(
        "--cs-namespaces",
        action="store_true",
        help="Analyze C# files and extract namespace declarations"
    )
    parser.add_argument(
        "--output",
        default="tree_dump.json",
        help="Output JSON file (default: tree_dump.json)"
    )

    args = parser.parse_args()

    base_path = os.getcwd()
    tree = build_tree(base_path, args.verbose, args.cs_namespaces)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2, ensure_ascii=False)

    print(f"Tree dumped to {args.output}")


if __name__ == "__main__":
    main()
