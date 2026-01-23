from orchestrator.scripts.generators.domain_model_definition import (
    DomainModelDefinition, 
    FieldDefinition,
    _fail)

# --------------------------------------------------
# Helpers AST
# --------------------------------------------------
def generate_liquibase_initial_data(
    definition: DomainModelDefinition
) -> str:
    """
    Genera el changelog XML de Liquibase para los datos iniciales
    de un DomainModelDefinition.
    """

    if not definition.has_initial_data:
        _fail(
            f"El modelo {definition.ModelName} no define datos iniciales"
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
        descripcion = f"{definition.ModelName} {nombre}"

        xml.append(f"""
    <changeSet id="{definition.db_table}-{constant['value'].lower()}" author="orco">
        <insert tableName="{definition.db_table}">
            <column name="id" valueComputed="nextval('{definition.db_table}_id_seq')"/>
            <column name="codigo" value="{constant['value']}"/>
            <column name="nombre" value="{nombre}"/>
            <column name="descripcion" value="{descripcion}"/>

            <!-- BaseModel -->
            <column name="is_deleted" valueBoolean="false"/>
            <column name="createdat" valueDate="NOW()"/>
            <column name="updatedat" valueDate="NOW()"/>
            <column name="createdby" valueNumeric="null"/>
            <column name="updatedby" valueNumeric="null"/>

            <!-- ConstantModel -->
            <column name="activo" valueBoolean="true"/>
    """.rstrip())

        # -----------------------------------------
        # Campos adicionales (incluye FK)
        # -----------------------------------------
        for field in definition.extra_fields:
            if field.name in (
                "id",
                "codigo",
                "nombre",
                "descripcion",
                "is_deleted",
                "createdat",
                "updatedat",
                "createdby",
                "updatedby",
                "activo",
            ):
                continue

            # ForeignKey
            if field.is_foreign_key:
                if not field.null:
                    _fail(
                        f"No se puede generar dato inicial para FK no nullable "
                        f"'{field.name}' en {definition.ModelName}"
                    )

                xml.append(
                    f'        <column name="{field.name}" valueNumeric="null"/>'
                )
                continue

            # Campos normales
            xml.append(
                f'        <column name="{field.name}" value=""/>'
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

def generate_column_xml(field: FieldDefinition) -> str:
    
    liquibase_type = map_field_type(field)
    # Column base (SIN constraints)
    column_xml = [
        f'        <column name="{field.name}" type="{liquibase_type}">'
    ]

    constraints = []

    if field.primary_key:
        constraints.append('primaryKey="true"')

    if not field.null:
        constraints.append('nullable="false"')

    if field.unique:
        constraints.append('unique="true"')

    # Constraints en su tag correcto
    if constraints:
        column_xml.append(
            f'            <constraints {" ".join(constraints)}/>'
        )

    column_xml.append('        </column>')
    return "\n".join(column_xml)

def generate_model_changelog(definition: DomainModelDefinition) -> str:
    """
    Genera el changelog estructural (DDL) del modelo.
    Incluye creación explícita de la secuencia para el ID.
    """

    table = definition.db_table
    seq = f"{table}_id_seq"

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<databaseChangeLog '
        'xmlns="http://www.liquibase.org/xml/ns/dbchangelog" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog '
        'http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.8.xsd">',

        f'<changeSet id="create-{table}" author="orco">',

        # -----------------------------------------
        # Secuencia explícita para el ID
        # -----------------------------------------
        f'    <createSequence '
        f'sequenceName="{seq}" '
        f'startValue="1" />',

        # -----------------------------------------
        # Tabla
        # -----------------------------------------
        f'    <createTable tableName="{table}">',

        # ID
        f'        <column name="id" type="int">',
        f'            <constraints primaryKey="true" nullable="false"/>',
        f'        </column>',
    ]

    # Resto de campos (heredados + extra)
    for field in definition.extra_fields:
        if field.name == "id":
            continue
        xml.append(generate_column_xml(field))

    xml.extend([
        f'    </createTable>',

        # -----------------------------------------
        # Default del ID → secuencia
        # -----------------------------------------
        f'    <addDefaultValue '
        f'tableName="{table}" '
        f'columnName="id" '
        f'defaultValueComputed="nextval(\'{seq}\')" />',

        f'</changeSet>',
        '</databaseChangeLog>',
    ])

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
    for field in definition.extra_fields:
        column_type = map_field_type(field)

        attrs = [f'name="{field.name}"', f'type="{column_type}"']

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

