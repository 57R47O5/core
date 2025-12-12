import ast
import re

# Mapea tipos Django -> tipos internos
DJANGO_FIELD_TYPES = {
    "CharField": "string",
    "TextField": "string",
    "EmailField": "email",
    "DateField": "date",
    "DateTimeField": "datetime",
    "IntegerField": "number",
    "FloatField": "number",
    "BooleanField": "boolean",
    "ForeignKey": "foreignkey",
}

def to_kebab_case(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower()


def analyze_django_model(file_path, model_name):
    """
    Retorna:
    [
        { name, type, required, target(optional), choices(optional) }
    ]
    """
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    fields = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == model_name:

            for stmt in node.body:

                # ignoramos Meta, métodos, etc.
                if not isinstance(stmt, ast.Assign):
                    continue

                if not isinstance(stmt.value, ast.Call):
                    continue

                field_name = stmt.targets[0].id
                call = stmt.value

                # Tipo Django
                if isinstance(call.func, ast.Attribute):
                    field_type = call.func.attr
                else:
                    continue

                if field_type not in DJANGO_FIELD_TYPES:
                    continue

                final_type = DJANGO_FIELD_TYPES[field_type]
                required = True
                fk_target = None
                choices = None

                # keywords: blank, null, choices, default
                for kw in call.keywords:
                    if kw.arg == "blank" and isinstance(kw.value, ast.Constant):
                        if kw.value.value is True:
                            required = False
                    if kw.arg == "null" and isinstance(kw.value, ast.Constant):
                        if kw.value.value is True:
                            required = False
                    if kw.arg == "default":
                        required = False

                    if kw.arg == "choices":
                        choices = True

                # ForeignKey obtiene modelo apuntado
                if final_type == "foreignkey":
                    if len(call.args) >= 1 and isinstance(call.args[0], ast.Name):
                        fk_target = call.args[0].id

                fields.append({
                    "name": field_name,
                    "type": final_type,
                    "required": required,
                    "target": fk_target,
                    "choices": choices
                })

    return fields