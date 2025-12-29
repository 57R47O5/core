import os
import shutil
import sys

# ==============================
# CONFIG
# ==============================
BACKEND_TEMPLATE = "templates/backend_project_template"
FRONTEND_TEMPLATE = "templates/frontend_project_template"

BACKEND_TARGET = "backend/projects"
FRONTEND_TARGET = "frontend/projects"

# ==============================
# UTILS
# ==============================
def copy_and_replace(src, dst, project_name):
    """
    Copia un directorio y reemplaza "project_name" interno por el nuevo nombre.
    """
    if not os.path.exists(dst):
        shutil.copytree(src, dst)

    # Recorre todos los archivos y reemplaza el texto project_name por el nombre real
    for root, _, files in os.walk(dst):
        for filename in files:
            path = os.path.join(root, filename)

            # Lee solo archivos de texto
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                continue  # archivos binarios se ignoran

            # Reemplaza placeholder
            new_content = content.replace("project_name", project_name)

            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)


def rename_project_folder(base_path, old_name, new_name):
    old_path = os.path.join(base_path, old_name)
    new_path = os.path.join(base_path, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)


# ==============================
# MAIN GENERATION LOGIC
# ==============================
def create_project(project_name):
    print(f"🚀 Creando proyecto {project_name}...")

    # ------------------------------
    # BACKEND
    # ------------------------------
    backend_dst = os.path.join(BACKEND_TARGET, project_name)
    print(f"📁 Backend → {backend_dst}")

    copy_and_replace(BACKEND_TEMPLATE, backend_dst, project_name)

    # renombrar carpeta project_name dentro del template
    rename_project_folder(
        os.path.join(backend_dst), "project_name", project_name
    )

    print("✔ Backend generado\n")

    # ------------------------------
    # FRONTEND
    # ------------------------------
    frontend_dst = os.path.join(FRONTEND_TARGET, project_name)
    print(f"📁 Frontend → {frontend_dst}")

    copy_and_replace(FRONTEND_TEMPLATE, frontend_dst, project_name)

    print("✔ Frontend generado\n")

    print("🎉 Proyecto creado con éxito!")
    print(f"- Backend: {backend_dst}")
    print(f"- Frontend: {frontend_dst}")


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python create_project.py nombre_proyecto")
        sys.exit(1)

    name = sys.argv[1].lower().strip()
    create_project(name)
