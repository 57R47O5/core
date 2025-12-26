"""
Domain model for database schema representation.

This module defines a neutral, framework-agnostic representation
of database structures. It is the shared contract between:

- Django model readers
- Liquibase XML readers
- Liquibase XML writers
- Schema validators

It intentionally contains NO logic related to:
- Django
- Liquibase
- SQL execution
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict


# =========================
# Core primitives
# =========================

@dataclass(frozen=True)
class Column:
    """
    Represents a database column.

    This is a pure value object.
    """
    name: str
    type: str
    nullable: bool = True
    unique: bool = False
    default: Optional[str] = None
    indexed: bool = False

    def signature(self) -> Dict:
        """
        Canonical representation used for comparison.
        """
        return {
            "name": self.name,
            "type": self.type,
            "nullable": self.nullable,
            "unique": self.unique,
            "default": self.default,
        }


@dataclass(frozen=True)
class ForeignKey:
    """
    Represents a foreign key constraint.
    """
    column: str
    referenced_table: str
    referenced_column: str = "id"
    on_delete: Optional[str] = None

    def signature(self) -> Dict:
        return {
            "column": self.column,
            "referenced_table": self.referenced_table,
            "referenced_column": self.referenced_column,
            "on_delete": self.on_delete,
        }


@dataclass(frozen=True)
class Index:
    """
    Represents a database index.
    """
    name: str
    columns: List[str]
    unique: bool = False

    def signature(self) -> Dict:
        return {
            "name": self.name,
            "columns": tuple(self.columns),
            "unique": self.unique,
        }


# =========================
# Table model
# =========================

@dataclass
class Table:
    """
    Represents a database table.

    Mutable by design during construction, immutable once finalized.
    """
    name: str
    columns: Dict[str, Column] = field(default_factory=dict)
    foreign_keys: List[ForeignKey] = field(default_factory=list)
    indexes: List[Index] = field(default_factory=list)
    is_history: bool = False

    def add_column(self, column: Column) -> None:
        """
        Adds a column to the table.

        Idempotent: re-adding the same column name is forbidden.
        """
        if column.name in self.columns:
            raise ValueError(f"Column '{column.name}' already exists in table '{self.name}'")
        self.columns[column.name] = column

    def add_foreign_key(self, fk: ForeignKey) -> None:
        self.foreign_keys.append(fk)

    def add_index(self, index: Index) -> None:
        self.indexes.append(index)

    def signature(self) -> Dict:
        """
        Canonical representation for comparison.
        """
        return {
            "name": self.name,
            "columns": {k: v.signature() for k, v in self.columns.items()},
            "foreign_keys": [fk.signature() for fk in self.foreign_keys],
            "indexes": [idx.signature() for idx in self.indexes],
            "is_history": self.is_history,
        }


# =========================
# Schema container
# =========================

@dataclass
class Schema:
    """
    Represents a full database schema (or a subset of it).

    This is the unit of comparison for validation.
    """
    tables: Dict[str, Table] = field(default_factory=dict)

    def add_table(self, table: Table) -> None:
        """
        Adds a table to the schema.

        Idempotent by name.
        """
        if table.name in self.tables:
            raise ValueError(f"Table '{table.name}' already exists in schema")
        self.tables[table.name] = table

    def get_table(self, name: str) -> Optional[Table]:
        return self.tables.get(name)

    def signature(self) -> Dict:
        """
        Canonical schema representation.
        """
        return {
            name: table.signature()
            for name, table in self.tables.items()
        }
