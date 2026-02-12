import os
import sys
import ast
from pathlib import Path
from orchestrator.scripts.generators.paths import (
    LIQUIBASE_CHANGELOG_APPS, APPS_DIR, FRONTEND_DIR)
from orchestrator.scripts.generators.changelog import (
    generate_liquibase_initial_data,
)
from orchestrator.scripts.generators.domain_model_definition import (
    parse_ast_file, extract_constants, extract_permission_manager_constants)
from orchestrator.scripts.generators.domain_model_definition import (
    load_domain_model_definition, 
    )

def main():
    app_name = sys.argv[1]
    build_app(app_name)
    print("Build done")

def build_app(app_name: str):
    permisos=build_app_permissions(app_name)
    roles=build_app_roles(app_name)
    build_app_rol_permissions(app_name, roles)
    build_app_routes(app_name)

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

    return permisos

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

    return roles        


def discover_app_permisos(app_name: str) -> list[dict]:
    path = APPS_DIR/ app_name /"permisos.py"

    if not os.path.exists(path):
        return []

    tree = parse_ast_file(path)
    class_index = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }

    permiso_managers = find_classes_inheriting(tree, "PermisoManager")

    permisos = []

    for manager in permiso_managers:        
        permisos.extend(extract_permission_manager_constants(manager, class_index))

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

def build_app_routes(app_name: str) -> None:
    """
    Construye el archivo {app_name}Routes.js
    combinando todos los *Route.jsx de la app.
    """
    route_files = discover_app_route_files(app_name)

    if not route_files:
        print(f"No se encontraron rutas para {app_name}")
        return

    content = generate_routes_file_content(app_name, route_files)
    write_routes_file(app_name, content)

    print(f"✔ Routes generado para {app_name}")

def discover_app_route_files(app_name: str) -> list[str]:
    """
    Devuelve los nombres de archivos *Route.jsx
    dentro de la carpeta routes de la app.
    """
    routes_path = get_routes_path(app_name)

    if not routes_path.exists():
        return []

    return [
        file.stem  # sin extensión
        for file in routes_path.iterdir()
        if file.is_file() and file.name.endswith("Route.jsx")
    ]

def get_routes_path(app_name: str) -> Path:
    return FRONTEND_DIR / "src" / "apps" / app_name / "routes"

def generate_routes_file_content(app_name: str, route_modules: list[str]) -> str:
    """
    Genera el contenido del archivo {app_name}Routes.js
    """
    imports = generate_import_statements(route_modules)
    spread_routes = generate_spread_routes(route_modules)

    return f"""{imports}

const {app_name}Routes = [
{spread_routes}
];

export default {app_name}Routes;
"""

def generate_import_statements(route_modules: list[str]) -> str:
    lines = []
    for module in route_modules:
        lines.append(f'import {module} from "./routes/{module}";')
    return "\n".join(lines)


def generate_spread_routes(route_modules: list[str]) -> str:
    lines = []
    for module in route_modules:
        lines.append(f"    ...{module},")
    return "\n".join(lines)

def write_routes_file(app_name: str, content: str) -> None:
    target_path = FRONTEND_DIR / "src" / "apps" / app_name / f"{app_name}Routes.js"
    target_path.write_text(content, encoding="utf-8")

def build_app_rol_permissions(app_name: str, roles: list):

    if not roles:
        return

    output_dir = LIQUIBASE_CHANGELOG_APPS / app_name
    output_dir.mkdir(parents=True, exist_ok=True)

    change_sets = []

    for rol in roles:
        print(f"El rol es {rol}")
        for permiso in rol.permisos:

            change_sets.append(f"""
        <insert tableName="rol_permiso">
            <column name="rol_id"
                    valueComputed="(SELECT id FROM rol WHERE code='{rol.code}')"/>
            <column name="permiso_id"
                    valueComputed="(SELECT id FROM permiso WHERE code='{permiso.code}')"/>
        </insert>
            """)

    if not change_sets:
        return

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
    xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
        http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.3.xsd">

    <changeSet id="{app_name}-rol-permiso-data" author="orc">
        {''.join(change_sets)}
    </changeSet>

</databaseChangeLog>
"""

    data_file = output_dir / "rol_permiso-data.xml"
    data_file.write_text(xml.strip() + "\n", encoding="utf-8")

    print(f"[GEN] data   -> {data_file}")


if __name__ == "__main__":
    main()