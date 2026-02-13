import os
import sys
import ast
import re
from pathlib import Path
from orchestrator.scripts.generators.paths import (
    LIQUIBASE_CHANGELOG_APPS, APPS_DIR, FRONTEND_DIR)
from orchestrator.scripts.generators.changelog import (
    generate_liquibase_initial_data,
    generate_liquibase_relation_data
)
from orchestrator.scripts.generators.domain_model_definition import (
    parse_ast_file)
from orchestrator.scripts.generators.domain_model_definition import (
    load_domain_model_definition, 
    )
from orchestrator.scripts.utils.security_definition import (
    ResourceDefinition, RoleDefinition, AppSecurityModel, PermissionGrant)

RELOAD_COMPLEX = {}
class Constant:
    '''
    Copiamos de backend/framework/models/basemodels.py 
    Por qué? Por si no puede levantar el orco
    '''
    def __init__(self, codigo):
        self.codigo = codigo
        self._cache = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if RELOAD_COMPLEX.get(self.codigo, False) or self._cache is None:
            self._cache = instance.get(codigo=self.codigo)
            RELOAD_COMPLEX[self.codigo] = False

        return self._cache
class RolPermisoConstant:
    def __init__(self, rol_codigo: str, permiso_codigo: str):
        self.rol_codigo = rol_codigo
        self.permiso_codigo = permiso_codigo


def main():
    app_name = sys.argv[1]
    build_app(app_name)
    print("Build done")

def build_app(app_name: str):
    build_app_permissions(app_name)
    build_app_routes(app_name)

def discover_app_permisos(app_name: str) -> list[dict]:
    path = APPS_DIR / app_name / "permisos.py"

    if not os.path.exists(path):
        return []

    tree = parse_ast_file(path)

    # 1️⃣ Buscar clase que herede de PermisoManager
    permiso_managers = find_classes_inheriting(tree, "PermisoManager")

    if not permiso_managers:
        raise Exception(f"No se encontró PermisoManager en {app_name}")

    if len(permiso_managers) > 1:
        raise Exception(f"Solo puede existir un PermisoManager en {app_name}")

    manager = permiso_managers[0]

    # 2️⃣ Extraer atributo grupos
    grupos = extract_grupos_from_manager(manager)

    # 3️⃣ Resolver imports
    import_map = build_import_map(tree)

    permisos = []

    for grupo_name in grupos:
        grupo_class_node = resolve_grupo_class(
            app_name,
            grupo_name,
            import_map
        )

        permisos.extend(
            extract_permiso_group_constants(grupo_class_node)
        )

    return permisos

def extract_grupos_from_manager(manager_class: ast.ClassDef) -> list[str]:
    for node in manager_class.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "grupos":
                    if isinstance(node.value, ast.List):
                        return [
                            elt.id
                            for elt in node.value.elts
                            if isinstance(elt, ast.Name)
                        ]

    raise Exception("PermisoManager debe definir atributo 'grupos'")

def build_import_map(tree: ast.Module) -> dict[str, str]:
    """
    Devuelve:
    {
        "PermisosSalida": "apps.elecciones.rest_controllers.salida_rest_controller"
    }
    """
    import_map = {}

    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                import_map[alias.name] = module

    return import_map

def resolve_grupo_class(app_name: str, grupo_name: str, import_map: dict) -> ast.ClassDef:

    rest_dir = APPS_DIR / app_name / "rest_controllers"

    for file in os.listdir(rest_dir):
        if not file.endswith(".py"):
            continue

        tree = parse_ast_file(rest_dir / file)

        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == grupo_name:
                return node

    raise Exception(f"No se encontró clase {grupo_name}")

def extract_permiso_group_constants(class_node: ast.ClassDef) -> list[dict]:
    permisos = []

    for node in class_node.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    nombre = target.id

                    if (
                        isinstance(node.value, ast.Call)
                        and isinstance(node.value.func, ast.Name)
                        and node.value.func.id == "Constant"
                    ):
                        value = node.value.args[0].value
                        permisos.append({
                            "nombre": nombre,
                            "codigo": value
                        })

    return permisos

def discover_app_roles(app_name: str) -> list[dict]:
    path = APPS_DIR / app_name / "roles.py"

    if not os.path.exists(path):
        return []    

    tree = parse_ast_file(path)

    rol_managers = find_classes_inheriting(tree, "RolManager")

    roles = []

    for manager in rol_managers:
        roles.extend(extract_roles_with_permissions(manager))

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

def build_resources_from_constants(constants: list[dict]) -> dict[str, ResourceDefinition]:
    '''
    El arg es un objeto Constant

    '''
    resources: dict[str, set[str]] = {}

    for const in constants:
        code = const['codigo']  # ejemplo: elecciones.visita.view
        _, resource, action = code.split(".")

        resources.setdefault(resource, set()).add(action)

    return {
        name: ResourceDefinition(name=name.replace("_","-"), allowed_actions=allowed_actions)
        for name, allowed_actions in resources.items()
    }

def flatten_permissions(permisos):
    flat = []
    for permiso in permisos:
        if isinstance(permiso, list):
            flat.extend(flatten_permissions(permiso))
        else:
            flat.append(permiso)
    return flat

def build_roles(
    role_constants: list[dict],
    resources: dict[str, ResourceDefinition],
    all_permission_constants: list[dict],
) -> dict[str, RoleDefinition]:

    permission_index = build_permission_index(all_permission_constants)

    roles: dict[str, RoleDefinition] = {}

    for const in role_constants:
        role_name = const["name"]

        permission_grants: set[PermissionGrant] = set()

        for permiso_ref in const["permisos"]:

            # Inferir recurso desde el nombre del grupo
            # PermisosVisita -> visita
            group_name = permiso_ref["group"]
            resource = infer_resource_from_group(group_name)

            if resource not in resources:
                raise ValueError(
                    f"Unknown resource '{resource}' in role '{role_name}'"
                )

            if permiso_ref["type"] == "all":

                for action in permission_index.get(resource, set()):
                    permission_grants.add(
                        PermissionGrant(resource=resource, action=action)
                    )

            elif permiso_ref["type"] == "single":

                action = permiso_ref["permiso"].lower()

                if action not in permission_index.get(resource, set()):
                    raise ValueError(
                        f"Invalid action '{action}' "
                        f"for resource '{resource}' in role '{role_name}'"
                    )

                permission_grants.add(
                    PermissionGrant(resource=resource, action=action)
                )

        roles[role_name] = RoleDefinition(
            name=role_name,
            permissions=permission_grants
        )

    return roles

def discover_app_security(app_name: str) -> AppSecurityModel:
    permiso_manager = discover_app_permisos(app_name)
    role_constants = discover_app_roles(app_name)

    all_permission_constants = permiso_manager

    resources = build_resources_from_constants(all_permission_constants)
    roles = build_roles(role_constants, 
                        resources,
                        all_permission_constants)

    security = AppSecurityModel(
        app_name=app_name,
        resources=resources,
        roles=roles
    )

    security.validate()
    return security

def validate(self):
    for role in self.roles.values():
        for resource, action in role.permissions:
            if resource not in self.resources:
                raise ValueError(
                    f"Rol {role.name} referencia recurso inexistente {resource}"
                )
            if action not in self.resources[resource].actions:
                raise ValueError(
                    f"Rol {role.name} referencia acción inválida {action}"
                )

def build_app_permissions(app_name: str):
    security = discover_app_security(app_name)

    output_dir = LIQUIBASE_CHANGELOG_APPS / app_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------
    # 1️⃣ Permisos
    # ------------------------

    permiso_constants = []
    for resource in security.resources.values():
        for action in resource.allowed_actions:
            code = f"{app_name}.{resource.name}.{action}"
            permiso_constants.append(code)

    permiso_xml = generate_permiso_data_xml(permiso_constants)

    permiso_file = output_dir / "permiso-data.xml"
    permiso_file.write_text(permiso_xml, encoding="utf-8")

    print(f"[GEN] permiso-data -> {permiso_file}")

    # ------------------------
    # 2️⃣ Roles
    # ------------------------

    role_codes = [
        f"{app_name}.{role.name}"
        for role in security.roles.values()
    ]

    role_xml = generate_rol_data_xml(role_codes)

    role_file = output_dir / "rol-data.xml"
    role_file.write_text(role_xml, encoding="utf-8")

    print(f"[GEN] rol-data -> {role_file}")

    # ------------------------
    # 3️⃣ Rol-Permiso
    # ------------------------

    role_perm_relations = []

    for role in security.roles.values():
        for permiso in role.permissions:
            role_code = f"{app_name}.{role.name}"
            permiso_code = f"{app_name}.{permiso.resource}.{permiso.action}"

            role_perm_relations.append((role_code, permiso_code))

    rol_perm_xml = generate_rol_permiso_data_xml(role_perm_relations)

    rol_perm_file = output_dir / "rol_permiso-data.xml"
    rol_perm_file.write_text(rol_perm_xml, encoding="utf-8")

    print(f"[GEN] rol_permiso-data -> {rol_perm_file}")

    return security

def generate_permiso_data_xml(permiso_codes: list[str]) -> str:
    if not permiso_codes:
        return ""

    model_definition = load_domain_model_definition("auth", "Permiso")

    constants = []
    for code in permiso_codes:
        const = {"name": code.replace(".", " "), "value": code}
        constants.append(const)

    model_definition.constants = constants

    return generate_liquibase_initial_data(model_definition)

def generate_rol_data_xml(role_codes: list[str]) -> str:
    if not role_codes:
        return ""

    model_definition = load_domain_model_definition("auth", "Rol")

    constants = []
    for code in role_codes:
        const = {"name": code.replace(".", " "), "value": code}
        constants.append(const)

    model_definition.constants = constants

    return generate_liquibase_initial_data(model_definition)

def generate_rol_permiso_data_xml(
    relations: list[tuple[str, str]]
) -> str:
    """
    relations = [(rol_codigo, permiso_codigo)]
    """
    if not relations:
        return ""

    model_definition = load_domain_model_definition("auth", "RolPermiso")

    constants = []
    for rol_codigo, permiso_codigo in relations:
        constants.append(
            RolPermisoConstant(
                rol_codigo=rol_codigo,
                permiso_codigo=permiso_codigo
            )
        )

    model_definition.constants = constants

    return generate_liquibase_relation_data(
        table_name="rol_permiso",
        relations=relations,  # [(rol_codigo, permiso_codigo)]
        left_table="rol",
        right_table="permiso",
        left_fk_column="rol_code",
        right_fk_column="permiso_code",
    )

def extract_roles_with_permissions(manager: ast.ClassDef) -> list[dict]:
    roles = []

    for node in manager.body:
        if not isinstance(node, ast.Assign):
            continue

        if not isinstance(node.value, ast.Call):
            continue

        if not isinstance(node.value.func, ast.Name):
            continue

        if node.value.func.id != "Constant":
            continue

        # Nombre del rol
        role_name = node.targets[0].id

        # Valor principal
        role_value = node.value.args[0].value

        permisos = []

        # Buscar keyword permisos=
        for kw in node.value.keywords:
            if kw.arg == "permisos" and isinstance(kw.value, ast.List):
                permisos = extract_permisos_from_list(kw.value)

        roles.append({
            "name": role_name,
            "value": role_value,
            "owner": manager.name,
            "permisos": permisos
        })

    return roles

def extract_permisos_from_list(list_node: ast.List) -> list[dict]:
    permisos = []

    for elt in list_node.elts:

        # Caso: PermisosVisita.all()
        if isinstance(elt, ast.Call) and isinstance(elt.func, ast.Attribute):
            if isinstance(elt.func.value, ast.Name):
                permisos.append({
                    "type": "all",
                    "group": elt.func.value.id
                })

        # Caso: PermisosVotante.CREATE
        elif isinstance(elt, ast.Attribute):
            if isinstance(elt.value, ast.Name):
                permisos.append({
                    "type": "single",
                    "group": elt.value.id,
                    "permiso": elt.attr
                })

    return permisos

def build_permission_index(all_permission_constants):
    """
    Devuelve:
        {
            "colaborador": {"view", "create", ...},
            "visita": {"view", ...}
        }
    """
    index: dict[str, set[str]] = {}

    for const in all_permission_constants:
        codigo = const["codigo"]
        _, resource, action = codigo.split(".")

        index.setdefault(resource, set()).add(action)

    return index

def infer_resource_from_group(group_name: str) -> str:
    """
    Convierte:
        PermisosVisita -> visita
        PermisosEstadoSalida -> estado_salida
    """

    if not group_name.startswith("Permisos"):
        raise ValueError(f"Invalid group name '{group_name}'")

    base = group_name.replace("Permisos", "", 1)

    # Convertir CamelCase a snake_case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', base)
    snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    return snake


if __name__ == "__main__":
    main()