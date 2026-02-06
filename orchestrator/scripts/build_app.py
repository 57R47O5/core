import os
import sys
import ast
from orchestrator.scripts.generators.paths import (
    LIQUIBASE_CHANGELOG_APPS, APPS_DIR)
from orchestrator.scripts.generators.changelog import (
    generate_liquibase_initial_data,
)
from orchestrator.scripts.generators.domain_model_definition import (
    parse_ast_file, extract_constants)
from orchestrator.scripts.generators.domain_model_definition import (
    load_domain_model_definition, 
    )

def main():
    app_name = sys.argv[1]
    build_app(app_name)
    print("Build done")

def build_app(app_name: str):
    build_app_permissions(app_name)
    build_app_roles(app_name)

def build_app_permissions(app_name: str):
    permisos = discover_app_permisos(app_name)

    if not permisos:
        return

    output_dir = LIQUIBASE_CHANGELOG_APPS / app_name

    # Permiso está en auth
    model_definition=load_domain_model_definition("auth", "Permiso")
    model_definition.constants=permisos

    data_xml=generate_liquibase_initial_data(
        model_definition
    )
    
    output_dir.mkdir(parents=True, exist_ok=True)
    if data_xml:
        data_file = output_dir / "permiso-data.xml"
        data_file.write_text(data_xml.strip() + "\n", encoding="utf-8")

        print(f"[GEN] data   -> {data_file}")


def build_app_roles(app_name: str):
    roles = discover_app_roles(app_name)

    if not roles:
        return

    output_dir = LIQUIBASE_CHANGELOG_APPS / app_name

    #rol está en auth
    model_definition = load_domain_model_definition("auth", "Rol")
    model_definition.constants=roles

    data_xml=generate_liquibase_initial_data(
        model_definition)

    output_dir.mkdir(parents=True, exist_ok=True)
    if data_xml:
        data_file = output_dir / "rol-data.xml"
        data_file.write_text(data_xml.strip() + "\n", encoding="utf-8")

        print(f"[GEN] data   -> {data_file}")        


def discover_app_permisos(app_name: str) -> list[dict]:
    path = APPS_DIR/ app_name /"permisos.py"

    if not os.path.exists(path):
        return []

    tree = parse_ast_file(path)

    permiso_managers = find_classes_inheriting(tree, "PermisoManager")

    permisos = []

    for manager in permiso_managers:
        permisos.extend(extract_constants(manager))

    return permisos

def discover_app_roles(app_name: str) -> list[dict]:
    path = APPS_DIR / app_name / "roles.py"

    if not os.path.exists(path):
        return []    

    tree = parse_ast_file(path)

    permiso_managers = find_classes_inheriting(tree, "RolManager")

    roles = []

    for manager in permiso_managers:
        roles.extend(extract_constants(manager))

    return roles

def find_classes_inheriting(tree: ast.AST, base_name: str) -> list[ast.ClassDef]:
    classes = []

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == base_name:
                classes.append(node)

    return classes

if __name__ == "__main__":
    main()