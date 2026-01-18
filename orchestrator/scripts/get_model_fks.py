import ast
import logging
import sys
from pathlib import Path
from typing import List


def get_model_fks(
    project_root: Path,
    app_name: str,
    model_name: str
) -> List[str]:

    model_file = (
        project_root
        / "backend"
        / "apps"
        / app_name
        / "models"
        / f"{model_name.lower()}.py"
    )

    if not model_file.exists():
        return []

    source = model_file.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # -----------------------------------------
    # 1. Resolver de dónde viene cada import
    #    NombreModelo -> app_origen | None
    # -----------------------------------------
    import_origin: dict[str, str | None] = {}

    for node in ast.walk(tree):

        # from .user import User
        if isinstance(node, ast.ImportFrom):
            if not node.module:
                continue

            for alias in node.names:
                model = alias.asname or alias.name

                # import interno (from .xxx import Model)
                if node.level == 1:
                    import_origin[model] = None

                # import externo (from other_app.models.xxx import Model)
                elif node.module.endswith(".models") or ".models." in node.module:
                    external_app = node.module.split(".")[0]
                    import_origin[model] = external_app

    # -----------------------------------------
    # 2. Detectar ForeignKeys
    # -----------------------------------------
    fk_targets: list[str] = []

    for node in ast.walk(tree):

        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "ForeignKey"
            and node.args
        ):
            target = node.args[0]
            model_name_fk: str | None = None

            # ForeignKey(User)
            if isinstance(target, ast.Name):
                model_name_fk = target.id

            # ForeignKey("User") o ForeignKey("base.User")
            elif isinstance(target, ast.Constant) and isinstance(target.value, str):
                model_name_fk = target.value.split(".")[-1]

            if not model_name_fk:
                continue

            origin_app = import_origin.get(model_name_fk)

            # FK interna
            if origin_app is None:
                fk_targets.append(model_name_fk)

            # FK externa
            else:
                fk_targets.append(f"ex-{origin_app}")

    return fk_targets
