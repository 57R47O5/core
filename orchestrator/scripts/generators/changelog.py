import ast
from pathlib import Path
from orchestrator.scripts.generators.paths import APPS_DIR
from dataclasses import dataclass
from typing import List, Dict, Optional

class ConstantModelGenerationError(RuntimeError):
    pass

@dataclass(frozen=True)
class FieldDefinition:
    name: str
    type: str          
    max_length: Optional[int] = None
    null: bool = True
    primary_key: bool = False
    unique: bool = False
    args: Dict[str,object] = None

    is_foreign_key: bool = False
    references_table: str | None = None
    references_column: str = "id"

    def __str__(self):
        return self.name

@dataclass
class DomainModelDefinition:
    """
    Definición canónica de un modelo de dominio persistente.

    Es independiente de:
    - Django
    - Liquibase
    - la base de datos

    Sirve como fuente única de verdad para generar:
    - schema
    - datos iniciales
    - documentación
    - otros artefactos futuros
    """
    model_name: str
    db_table: str
    constants: List[Dict[str, str]]
    extra_fields: List[FieldDefinition]

    inherits_from_base_model: bool

    @property
    def has_initial_data(self) -> bool:
        """
        Indica si el modelo define datos iniciales (constantes).
        """
        return bool(self.constants)
    
    @property
    def has_history(self)->bool:
        """
        Indica si el modelo necesita una  tabla histórica
        """
        return self.inherits_from_base_model
    
BASE_MODEL_FIELDS = {
    "BaseModel": [
        FieldDefinition(
            name="id",
            type="AutoField",
            max_length=None,
            null=False,
            primary_key=True,
            args={}
        ),
        FieldDefinition(
            name="is_deleted",
            type="BooleanField",
            max_length=None,
            null=False,
            args={"default": False}
        ),
        FieldDefinition(
            name="createdby",
            type="CharField",
            null=True,
            is_foreign_key=True,
            references_table="auth_user"
        ),
        FieldDefinition(
            name="updatedby",
            type="CharField",
            null=True,
            is_foreign_key=True,
            references_table="auth_user"
        ),
        FieldDefinition(
            name="createdat",
            type="DateTimeField",
            max_length=None,
            null=True,
            args={"auto_now_add": True}
        ),
        FieldDefinition(
            name="updatedat",
            type="DateTimeField",
            max_length=None,
            null=True,
            args={"auto_now": True}
        ),
    ],

    "BasicModel": [
        FieldDefinition(
            name="nombre",
            type="CharField",
            max_length=200,
            null=False,
            args={}
        ),
        FieldDefinition(
            name="descripcion",
            type="TextField",
            max_length=None,
            null=True,
            args={}
        ),
    ],
    "ConstantModel": [
    ],

}

MODEL_INHERITANCE = {
    "ConstantModel": "BasicModel",
    "BasicModel": "BaseModel",
    "BaseModel": None,
}


# --------------------------------------------------
# Helpers AST
# --------------------------------------------------
IGNORED_ATTRIBUTES = {"objects"}

def _fail(msg):
    raise ConstantModelGenerationError(msg)

def _get_str_constant(node, ctx):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    _fail(f"{ctx} debe ser un string literal")

def _is_false(node):
    return isinstance(node, ast.Constant) and node.value is False

def parse_ast_file(model_file: Path) -> ast.Module:
    """
    Lee y parsea un archivo Python en un AST.

    Falla si el archivo no existe o no puede parsearse.
    """
    if not model_file.exists():
        _fail(f"Archivo no encontrado: {model_file}")

    try:
        return ast.parse(model_file.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        _fail(f"Error de sintaxis en {model_file}: {exc}")


def find_model_and_manager(tree: ast.Module):
    """
    Localiza el ConstantModel/BasicModel y su Manager asociado
    según la convención del monorepo:

    - Un solo modelo por archivo
    - Un solo manager por archivo
    """
    model_class = None
    manager_class = None

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        bases = {getattr(base, "id", None) for base in node.bases}

        if "ConstantModel" in bases or "BasicModel" in bases:
            if model_class:
                _fail("Más de un modelo encontrado en el archivo")
            model_class = node

        elif node.name.endswith("Manager"):
            if manager_class:
                _fail("Más de un Manager encontrado en el archivo")
            manager_class = node

    if not model_class:
        _fail("No se encontró ConstantModel o BasicModel en el archivo")

    if not manager_class:
        _fail("No se encontró Manager en el archivo")

    return model_class, manager_class

def extract_model_bases(model_class: ast.ClassDef) -> list[str]:
    bases = []

    for base in model_class.bases:
        if isinstance(base, ast.Name):
            bases.append(base.id)
        elif isinstance(base, ast.Attribute):
            bases.append(base.attr)

    return bases

def resolve_inherited_fields(base_names: list[str]) -> list[FieldDefinition]:
    fields = []

    for base in base_names:
        parent = MODEL_INHERITANCE.get(base)

        if parent:
            fields.extend(resolve_inherited_fields([parent]))

        fields.extend(BASE_MODEL_FIELDS.get(base, []))

    return fields

def extract_model_meta(model_class: ast.ClassDef) -> str:
    """
    Extrae y valida Meta.db_table y Meta.managed del modelo.

    Reglas:
    - db_table debe existir y ser string literal
    - managed debe ser False
    """
    db_table = None
    managed = None

    for node in model_class.body:
        if isinstance(node, ast.ClassDef) and node.name == "Meta":
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    key = stmt.targets[0].id
                    if key == "db_table":
                        if not isinstance(stmt.value, ast.Constant):
                            _fail("Meta.db_table debe ser un string literal")
                        db_table = stmt.value.value
                    elif key == "managed":
                        managed = stmt.value

    if not db_table:
        _fail(f"{model_class.name} debe definir Meta.db_table")

    if not (isinstance(managed, ast.Constant) and managed.value is False):
        _fail(f"{model_class.name} debe tener Meta.managed = False")

    return db_table

def extract_constants(manager_class: ast.ClassDef):
    """
    Extrae las constantes definidas en el Manager mediante Constant("XXX").

    Retorna una lista de dicts con name y value.
    """
    constants = []

    for stmt in manager_class.body:
        if not isinstance(stmt, ast.Assign):
            continue

        if not isinstance(stmt.value, ast.Call):
            continue

        if getattr(stmt.value.func, "id", None) != "Constant":
            continue

        name = stmt.targets[0].id
        arg = stmt.value.args[0]

        if not isinstance(arg, ast.Constant):
            _fail(f"Constant {name} debe usar un literal string")

        constants.append(
            {
                "name": name,
                "value": arg.value,
            }
        )

    if not constants:
        _fail(f"{manager_class.name} no define constantes")

    return constants

def extract_extra_fields(model_class: ast.ClassDef):
    """
    Descubre campos adicionales al contrato base y los devuelve
    como definiciones de dominio (no strings sueltos).

    Reglas:
    - Se ignoran: id, codigo, nombre, descripcion
    - Se ignora explícitamente: objects
    - Solo se permiten CharField (por ahora)
    """
    base_fields = {"id", "codigo", "nombre", "descripcion"}
    ignored_attrs = {"objects"}

    extra_fields = []

    for stmt in model_class.body:
        if not isinstance(stmt, ast.Assign):
            continue

        if not stmt.targets or not isinstance(stmt.targets[0], ast.Name):
            continue

        field_name = stmt.targets[0].id

        if field_name in base_fields or field_name in ignored_attrs:
            continue

        if not isinstance(stmt.value, ast.Call):
            continue

        field_type = getattr(stmt.value.func, "attr", None)

        if field_type == "CharField":
            extra_fields.append(
                FieldDefinition(
                    name=field_name,
                    type="CharField",
                    args={}   # futuro: max_length, null, etc.
                )
            )
        else:
            _fail(
                f"Campo no soportado '{field_name}' "
                f"(solo CharField permitido)"
            )

    return extra_fields

def generate_liquibase_initial_data(
    definition: DomainModelDefinition
) -> str:
    """
    Genera el changelog XML de Liquibase para los datos iniciales
    de un DomainModelDefinition.
    """

    if not definition.has_initial_data:
        _fail(
            f"El modelo {definition.model_name} no define datos iniciales"
        )

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<databaseChangeLog '
        'xmlns="http://www.liquibase.org/xml/ns/dbchangelog" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog '
        'http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.8.xsd">'
    ]

    for constant in definition.constants:
        nombre = constant["name"].replace("_", " ").title()
        descripcion = f"{definition.model_name} {nombre}"

        xml.append(f"""
<changeSet id="{definition.db_table}-{constant['value'].lower()}" author="orco">
    <insert tableName="{definition.db_table}">
        <column name="codigo" value="{constant['value']}"/>
        <column name="nombre" value="{nombre}"/>
        <column name="descripcion" value="{descripcion}"/>
""".rstrip())

        # -----------------------------------------
        # Campos adicionales (incluye FK)
        # -----------------------------------------
        for field in definition.extra_fields:
            if field.name in ("id", "codigo", "nombre", "descripcion"):
                continue

            # ForeignKey
            if field.is_foreign_key:
                if not field.null:
                    _fail(
                        f"No se puede generar dato inicial para FK no nullable "
                        f"'{field.name}' en {definition.model_name}"
                    )

                xml.append(
                    f'        <column name="{field.name}" value="{""}"/>'
                )
                continue

            # Campos normales
            xml.append(
                f'        <column name="{field.name}" value="{""}"/>'
            )

        xml.append(f"""
    </insert>
    <rollback>
        <delete tableName="{definition.db_table}">
            <where>codigo = '{constant['value']}'</where>
        </delete>
    </rollback>
</changeSet>
""".rstrip())

    xml.append("</databaseChangeLog>")

    return "\n".join(xml)


def resolve_model_file(app_name:str, model_name: str) -> Path:
    model_file = APPS_DIR / app_name / "models" /f"{model_name.lower()}.py"
    
    if not model_file.exists():
        _fail(f"Modelo '{model_name}' no encontrado en {APPS_DIR}")
    return model_file

def build_domain_model_definition(
    tree: ast.AST
) -> DomainModelDefinition:
    """
    Construye una DomainModelDefinition a partir del AST de un archivo de modelo.

    Responsabilidades:
    - localizar el modelo y su manager
    - extraer metadata obligatoria
    - descubrir constantes de dominio
    - descubrir campos heredados y propios
    - determinar semántica de auditoría

    Falla rápida y ruidosamente si el contrato no se cumple.
    """

    # --------------------------------------------------
    # Localización de clases
    # --------------------------------------------------
    model_class, manager_class = find_model_and_manager(tree)

    # --------------------------------------------------
    # Metadata del modelo
    # --------------------------------------------------
    db_table = extract_model_meta(model_class)

    # --------------------------------------------------
    # Constantes (datos iniciales)
    # --------------------------------------------------
    constants = extract_constants(manager_class)

    # --------------------------------------------------
    # Herencia
    # --------------------------------------------------
    base_names = extract_model_bases(model_class)

    inherits_from_base_model = any(
        base in ("BaseModel", "BasicModel")
        for base in base_names
    )

    # --------------------------------------------------
    # Campos
    # --------------------------------------------------
    inherited_fields = resolve_inherited_fields(base_names)
    model_fields = extract_extra_fields(model_class)

    all_fields = inherited_fields + model_fields

    # --------------------------------------------------
    # Construcción de la definición
    # --------------------------------------------------
    return DomainModelDefinition(
        model_name=model_class.name,
        db_table=db_table,
        constants=constants,
        extra_fields=all_fields,
        inherits_from_base_model=inherits_from_base_model,
    )

def load_domain_model_definition(
    app_name: str,
    model_name: str,
) -> DomainModelDefinition:
    """
    Carga y construye la definición de dominio de un modelo
    usando AST y convenciones del monorepo.
    """
    model_file = resolve_model_file(app_name, model_name)
    tree = parse_ast_file(model_file)
    return build_domain_model_definition(tree)

FIELD_TYPE_MAP = {
    "AutoField": lambda f: "int",
    "ForeignKey": lambda f: "int",
    "CharField": lambda f: f'varchar({f.max_length or 255})',
    "TextField": lambda f: 'text',
    "IntegerField": lambda f: 'int',
    "BigIntegerField": lambda f: 'bigint',
    "BooleanField": lambda f: 'boolean',
    "DateField": lambda f: 'date',
    "DateTimeField": lambda f: 'timestamp',
}

def map_field_type(field: FieldDefinition) -> str:
    try:
        return FIELD_TYPE_MAP[field.type](field)
    except KeyError:
        raise Exception(
            f"Tipo de campo no soportado para Liquibase: {field.type}, en el campo {str(field)}"
        )

def generate_column_xml(field:FieldDefinition) -> str:
    liquibase_type = map_field_type(field)

    attrs = [
        f'name="{field.name}"',
        f'type="{liquibase_type}"'
    ]

    if not field.null:
        attrs.append('nullable="false"')

    column_xml = [f'        <column {" ".join(attrs)}>']

    constraints = []

    if field.primary_key:
        constraints.append('primaryKey="true"')

    if not field.null:
        constraints.append('nullable="false"')

    if field.unique:
        constraints.append('unique="true"')

    if constraints:
        column_xml.append(
            f'            <constraints {" ".join(constraints)}/>'
        )

    column_xml.append('        </column>')
    return "\n".join(column_xml)


def generate_model_changelog(definition:DomainModelDefinition) -> str:
    """
    Genera el changelog estructural (DDL) del modelo.
    Soporta campos comunes y está pensado para extenderse fácilmente.
    """

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<databaseChangeLog '
        'xmlns="http://www.liquibase.org/xml/ns/dbchangelog" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog '
        'http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.8.xsd">',
        f'<changeSet id="create-{definition.db_table}" author="orco">',
        f'    <createTable tableName="{definition.db_table}">'
    ]

    for field in definition.extra_fields:
        xml.append(generate_column_xml(field))

    xml.append('    </createTable>')
    xml.append('</changeSet>')
    xml.append('</databaseChangeLog>')

    return "\n".join(xml)

def generate_historical_model_changelog(
    definition: DomainModelDefinition
) -> str:
    """
    Genera el changelog del modelo histórico asociado
    a un DomainModelDefinition.

    Implementación mínima y extensible.
    """

    hist_table = f"hist_{definition.db_table}"

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<databaseChangeLog '
        'xmlns="http://www.liquibase.org/xml/ns/dbchangelog" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog '
        'http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.8.xsd">',
        f'''
<changeSet id="create-{hist_table}" author="orco">
    <createTable tableName="{hist_table}">
'''
    ]

    # --- Campos técnicos del histórico ---
    xml.append('        <column name="history_id" type="bigint"/>')
    xml.append('        <column name="history_date" type="timestamp"/>')
    xml.append('        <column name="history_type" type="char(1)"/>')
    xml.append('        <column name="history_user" type="varchar(150)"/>')

    # --- Campos del modelo original ---
    for field in definition.fields:
        column_type = map_field_type(field)

        attrs = [f'name="{field.name}"', f'type="{column_type}"']

        if not field.null:
            attrs.append('nullable="false"')

        if field.unique:
            attrs.append('unique="true"')

        xml.append(
            f'        <column {" ".join(attrs)}/>'
        )

    xml.append(f'''
    </createTable>
</changeSet>
</databaseChangeLog>
''')

    return "\n".join(line.rstrip() for line in xml)

def generate_constant_model_changelog(app_name: str, model_name: str):
    definition = load_domain_model_definition(app_name, model_name)

    model_xml = generate_model_changelog(definition)

    data_xml = (
        generate_liquibase_initial_data(definition)
        if definition.has_initial_data
        else None
    )

    history_xml = (
        generate_historical_model_changelog(definition)
        if definition.has_history
        else None
    )

    return model_xml, data_xml, history_xml

