import importlib.util
import sys
from pathlib import Path

settings_path = Path(sys.argv[1])

spec = importlib.util.spec_from_file_location("orc_apps", settings_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

apps = getattr(module, "ORC_APPS", [])

for app in apps:
    # Normalización del nombre lógico de la app
    if "." in app:
        app_name = app.split(".")[-1]
    else:
        app_name = app

    print(app_name)
