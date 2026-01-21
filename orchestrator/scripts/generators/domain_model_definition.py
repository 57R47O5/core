import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Any
from scripts.generators.paths import APPS_DIR
from scripts.utils.naming import to_snake_case
from scripts.utils.resolve_model_app import resolve_model_app

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
    default: Any | None = None
    choices: list | None = None
    fk_target: str | None = None
    is_embedded: bool = False
    references_model: str | None = None
    references_app: str | None = None
    appears_in_form: bool | None = True

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
    app_name: str
    ModelName: str
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
    
    @property
    def model_name(self)->str:
        return to_snake_case(self.ModelName)

    
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
            appears_in_form=False,
            args={"default": False}
        ),
        FieldDefinition(
            name="createdby",
            type="CharField",
            appears_in_form=False,
            null=True
        ),
        FieldDefinition(
            name="updatedby",
            type="CharField",
            appears_in_form=False,
            null=True,
        ),
        FieldDefinition(
            name="createdat",
            type="DateTimeField",
            max_length=None,
            null=True,
            appears_in_form=False,
            args={"auto_now_add": True}
        ),
        FieldDefinition(
            name="updatedat",
            type="DateTimeField",
            max_length=None,
            null=True,
            appears_in_form=False,
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
        FieldDefinition(
            name="codigo", 
            type="CharField", 
            null= False,
            unique= True,
            appears_in_form=False,
            max_length= 50
        ),
        FieldDefinition(
            name="activo", 
            type="BooleanField", 
            appears_in_form=False,
            null= False),
    ],
}

MODEL_INHERITANCE = {
    "ConstantModel": "BasicModel",
    "BasicModel": "BaseModel",
    "BaseModel": None,
}



class ConstantModelGenerationError(RuntimeError):
    pass

def _fail(msg):
    raise ConstantModelGenerationError(msg)

def resolve_model_file(app_name:str, model_name: str) -> Path:
    model_file = APPS_DIR / app_name / "models" /f"{to_snake_case(model_name)}.py"
    
    if not model_file.exists():
        _fail(f"Modelo '{model_name}' no encontrado en {APPS_DIR}")
    return model_file

def resolve_inherited_fields(base_names: list[str]) -> list[FieldDefinition]:
    fields = []

    for base in base_names:
        parent = MODEL_INHERITANCE.get(base)

        if parent:
            fields.extend(resolve_inherited_fields([parent]))

        fields.extend(BASE_MODEL_FIELDS.get(base, []))

    return fields


def extract_model_bases(model_class: ast.ClassDef) -> list[str]:
    bases = []

    for base in model_class.bases:
        if isinstance(base, ast.Name):
            bases.append(base.id)
        elif isinstance(base, ast.Attribute):
            bases.append(base.attr)

    return bases

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
    como definiciones de dominio ricas (FieldDefinition).
    """

    base_fields = {"id", "codigo", "nombre", "descripcion"}
    ignored_attrs = {"objects", "EMBEDDED_FKS"}

    # --------------------------------------------------
    # Detectar FKs embebidos declarados en el modelo
    # --------------------------------------------------
    embedded_fks = set()

    for stmt in model_class.body:
        if (
            isinstance(stmt, ast.Assign)
            and isinstance(stmt.targets[0], ast.Name)
            and stmt.targets[0].id == "EMBEDDED_FKS"
            and isinstance(stmt.value, (ast.List, ast.Tuple))
        ):
            for elt in stmt.value.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    embedded_fks.add(elt.value)

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

        call = stmt.value
        field_type = getattr(call.func, "attr", None)

        # ----------------------------------------------
        # ForeignKey
        # ----------------------------------------------
        if field_type == "ForeignKey":
            ref_model = None
            ref_app = None

            # ------------------------------------
            # Primer argumento: modelo referenciado
            # ------------------------------------
            if call.args:
                arg = call.args[0]

                # ForeignKey(Modelo)
                if isinstance(arg, ast.Name):
                    ref_model = arg.id

                # ForeignKey("app.Modelo")
                elif isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if "." in arg.value:
                        ref_app, ref_model = arg.value.split(".")
                    else:
                        ref_model = arg.value

            # ------------------------------------
            # Inferir app si no viene explícita
            # ------------------------------------
            if ref_model and not ref_app:
                ref_app = resolve_model_app(ref_model)

            extra_fields.append(
                FieldDefinition(
                    name=field_name,
                    type="ForeignKey",
                    is_foreign_key=True,
                    references_app=ref_app,
                    references_model=ref_model,
                    appears_in_form=True,
                    is_embedded=field_name in embedded_fks,
                )
            )

        # ----------------------------------------------
        # Campo normal
        # ----------------------------------------------
        else:
            extra_fields.append(
                FieldDefinition(
                    name=field_name,
                    type=field_type,
                    is_foreign_key=False,
                )
            )

    return extra_fields

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

        if "ConstantModel" in bases or "BasicModel" in bases or "BaseModel" in bases:
            if model_class:
                _fail("Más de un modelo encontrado en el archivo")
            model_class = node

        elif node.name.endswith("Manager"):
            if manager_class:
                _fail("Más de un Manager encontrado en el archivo")
            manager_class = node

    if not model_class:
        _fail("No se encontró ConstantModel o BasicModel en el archivo")

    return model_class, manager_class


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


def build_domain_model_definition(
    app_name: str,
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
    constants = extract_constants(manager_class) if  manager_class else []

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
        app_name = app_name,
        ModelName=model_class.name,
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
    return build_domain_model_definition(app_name, tree)
