"""
liquibase_writer.py

Convierte una representación intermedia de modelos Django
en archivos XML compatibles con Liquibase.

Responsabilidades:
- Generar XML de tablas
- Incluir rollback explícito
- Mantener idempotencia
"""

from pathlib import Path
from typing import List
from xml.etree.ElementTree import Element, SubElement, ElementTree


# =========================
# Tipos esperados (contrato)
# =========================

class FieldSchema:
    """
    Representa un campo de un modelo Django
    ya normalizado por django_reader.
    """
    def __init__(
        self,
        name: str,
        column_type: str,
        nullable: bool = True,
        primary_key: bool = False,
        unique: bool = False,
    ):
        self.name = name
        self.column_type = column_type
        self.nullable = nullable
        self.primary_key = primary_key
        self.unique = unique


class ModelSchema:
    """
    Representa un modelo Django listo para
    ser transformado en Liquibase.
    """
    def __init__(
        self,
        name: str,
        table_name: str,
        fields: List[FieldSchema],
        has_log_table: bool = False,
    ):
        self.name = name
        self.table_name = table_name
        self.fields = fields
        self.has_log_table = has_log_table


# =========================
# XML helpers
# =========================

def create_database_change_log() -> Element:
    """
    Crea el nodo raíz <databaseChangeLog>.
    """
    root = Element(
        "databaseChangeLog",
        {
            "xmlns": "http://www.liquibase.org/xml/ns/dbchangelog",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": (
                "http://www.liquibase.org/xml/ns/dbchangelog "
                "http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.23.xsd"
            ),
        },
    )
    return root


def add_create_table_changeset(
    root: Element,
    model: ModelSchema,
    author: str,
):
    """
    Agrega un changeSet que crea una tabla
    con rollback explícito.
    """
    changeset_id = f"create-table-{model.table_name}"

    changeset = SubElement(
        root,
        "changeSet",
        {
            "id": changeset_id,
            "author": author,
            "runOnChange": "true",
        },
    )

    create_table = SubElement(
        changeset,
        "createTable",
        {"tableName": model.table_name},
    )

    for field in model.fields:
        column = SubElement(
            create_table,
            "column",
            {
                "name": field.name,
                "type": field.column_type,
            },
        )

        constraints = {}
        if field.primary_key:
            constraints["primaryKey"] = "true"
        if not field.nullable:
            constraints["nullable"] = "false"
        if field.unique:
            constraints["unique"] = "true"

        if constraints:
            SubElement(column, "constraints", constraints)

    rollback = SubElement(changeset, "rollback")
    SubElement(
        rollback,
        "dropTable",
        {"tableName": model.table_name},
    )


# =========================
# Log table
# =========================

def build_log_model(model: ModelSchema) -> ModelSchema:
    """
    Construye la definición de la tabla de log
    a partir del modelo base.
    """
    log_fields = [
        FieldSchema(
            name="log_id",
            column_type="BIGINT",
            primary_key=True,
            nullable=False,
        ),
        FieldSchema(
            name="operation",
            column_type="VARCHAR(10)",
            nullable=False,
        ),
    ]

    for field in model.fields:
        log_fields.append(
            FieldSchema(
                name=field.name,
                column_type=field.column_type,
                nullable=True,
            )
        )

    return ModelSchema(
        name=f"{model.name}Log",
        table_name=f"{model.table_name}_log",
        fields=log_fields,
        has_log_table=False,
    )


# =========================
# Writer
# =========================

def write_model_xml(
    model: ModelSchema,
    output_dir: Path,
    author: str = "system",
):
    """
    Genera el archivo XML de un modelo
    (y su tabla de log si corresponde).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    root = create_database_change_log()
    add_create_table_changeset(root, model, author)

    tree = ElementTree(root)
    file_path = output_dir / f"{model.table_name}.xml"
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

    if model.has_log_table:
        log_model = build_log_model(model)
        write_model_xml(log_model, output_dir, author)


# =========================
# API pública
# =========================

def write_models(
    models: List[ModelSchema],
    output_dir: Path,
    author: str = "system",
):
    """
    Punto de entrada principal.

    Genera los XML de Liquibase
    para todos los modelos recibidos.
    """
    for model in models:
        write_model_xml(model, output_dir, author)
