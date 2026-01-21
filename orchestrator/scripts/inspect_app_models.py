import ast
from pathlib import Path
from typing import List

def get_app_models(project_root: Path, app_name: str) -> List[str]:
    models_init = (
        project_root
        / "backend"
        / "apps"
        / app_name
        / "models"
        / "__init__.py"
    )

    if not models_init.exists():
        return []

    source = models_init.read_text(encoding="utf-8")
    tree = ast.parse(source)

    model_names: list[str] = []

    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "__all__"
            and isinstance(node.value, (ast.List, ast.Tuple))
        ):
            for elt in node.value.elts:

                # __all__ = [User, Rol, ...]
                if isinstance(elt, ast.Name):
                    model_names.append(elt.id)

                # __all__ = ["User", ...] (soportado, pero secundario)
                elif isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    model_names.append(elt.value)

    return model_names
