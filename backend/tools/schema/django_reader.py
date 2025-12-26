"""
Django model reader.

This module inspects Django ORM models and converts them into
neutral domain schema representations.

It does NOT:
- touch the database
- run migrations
- depend on Liquibase
"""

from typing import Type

from django.db import models

from tools.schema.domain import (
    Schema,
    Table,
    Column,
    ForeignKey,
    Index,
)


# =========================
# Public API
# =========================

def read_model(model: Type[models.Model]) -> Schema:
    """
    Read a Django model and produce a Schema containing a single table.

    This function is idempotent and has no side effects.

    :param model: Django model class
    :return: Schema instance
    """
    schema = Schema()
    table = _build_table_from_model(model)
    schema.add_table(table)

    # Optional: historical table
    if _has_history(model):
        history_table = _build_history_table(table)
        schema.add_table(history_table)

    return schema


# =========================
# Table builders
# =========================

def _build_table_from_model(model: Type[models.Model]) -> Table:
    """
    Build a Table from a Django model.
    """
    table = Table(
        name=model._meta.db_table,
        is_history=False,
    )

    for field in model._meta.local_fields:
        _handle_field(field, table)

    _handle_indexes(model, table)

    return table


def _build_history_table(source_table: Table) -> Table:
    """
    Build a history table from a source table.

    Naming convention:
        <table_name>_history
    """
    history = Table(
        name=f"{source_table.name}_history",
        is_history=True,
    )

    for column in source_table.columns.values():
        history.add_column(column)

    # History tables do NOT replicate FKs or indexes by default
    return history


# =========================
# Field handlers
# =========================

def _handle_field(field: models.Field, table: Table) -> None:
    """
    Dispatch field handling based on Django field type.
    """
    if isinstance(field, models.ForeignKey):
        _handle_foreign_key(field, table)
    else:
        column = _build_column(field)
        table.add_column(column)


def _handle_foreign_key(field: models.ForeignKey, table: Table) -> None:
    """
    Handle Django ForeignKey fields.
    """
    column_name = field.column
    referenced_table = field.target_field.model._meta.db_table

    column = Column(
        name=column_name,
        type=_map_field_type(field),
        nullable=field.null,
        unique=field.unique,
    )

    table.add_column(column)

    fk = ForeignKey(
        column=column_name,
        referenced_table=referenced_table,
        referenced_column=field.target_field.column,
        on_delete=_map_on_delete(field),
    )

    table.add_foreign_key(fk)


def _build_column(field: models.Field) -> Column:
    """
    Build a Column from a Django field.
    """
    return Column(
        name=field.column,
        type=_map_field_type(field),
        nullable=field.null,
        unique=field.unique,
        default=_map_default(field),
        indexed=field.db_index,
    )


# =========================
# Index handling
# =========================

def _handle_indexes(model: Type[models.Model], table: Table) -> None:
    """
    Handle Django model indexes.
    """
    for index in model._meta.indexes:
        idx = Index(
            name=index.name,
            columns=list(index.fields),
            unique=index.unique,
        )
        table.add_index(idx)


# =========================
# Utilities
# =========================

def _map_field_type(field: models.Field) -> str:
    """
    Map Django field types to database column types.

    This mapping is intentionally conservative and explicit.
    """
    if isinstance(field, models.AutoField):
        return "SERIAL"
    if isinstance(field, models.BigAutoField):
        return "BIGSERIAL"
    if isinstance(field, models.CharField):
        return f"VARCHAR({field.max_length})"
    if isinstance(field, models.TextField):
        return "TEXT"
    if isinstance(field, models.BooleanField):
        return "BOOLEAN"
    if isinstance(field, models.DateTimeField):
        return "TIMESTAMP"
    if isinstance(field, models.IntegerField):
        return "INTEGER"
    if isinstance(field, models.BigIntegerField):
        return "BIGINT"

    raise NotImplementedError(
        f"Unsupported Django field type: {field.__class__.__name__}"
    )


def _map_default(field: models.Field):
    """
    Map Django default values.

    Only static defaults are supported.
    """
    if callable(field.default):
        return None
    if field.default is models.NOT_PROVIDED:
        return None
    return str(field.default)


def _map_on_delete(field: models.ForeignKey) -> str:
    """
    Map Django on_delete behavior to DB-level action.
    """
    mapping = {
        models.CASCADE: "CASCADE",
        models.PROTECT: "RESTRICT",
        models.SET_NULL: "SET NULL",
        models.DO_NOTHING: "NO ACTION",
    }

    return mapping.get(field.remote_field.on_delete, None)


def _has_history(model: Type[models.Model]) -> bool:
    """
    Detect whether the model supports history tables.

    Current heuristic:
    - model has attribute 'history'
    """
    return hasattr(model, "history")
