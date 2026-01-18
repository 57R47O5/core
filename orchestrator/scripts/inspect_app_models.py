import sys
import ast
from pathlib import Path

app_name = sys.argv[1]

project_root = Path.cwd()
models_init = (
    project_root
    / "backend"
    / "apps"
    / app_name
    / "models"
    / "__init__.py"
)

# Si no existe, no hay modelos migrables
if not models_init.exists():
    sys.exit(0)

source = models_init.read_text(encoding="utf-8")

tree = ast.parse(source)

model_names = []

for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__all__":
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Name):
                            model_names.append(elt.id)

for name in model_names:
    print(name)
