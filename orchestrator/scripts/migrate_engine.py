from pathlib import Path
import logging
import sys

from inspect_orc_apps import get_orc_apps
from inspect_app_models import get_app_models
from get_model_fks import get_model_fks


def setup_logger(project_root: Path) -> logging.Logger:
    log_file = project_root / "migrate_engine.log"

    logger = logging.getLogger("migrate_engine")
    logger.setLevel(logging.INFO)

    # evitar duplicados si se importa
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

def main(project_name: str):
    project_root = Path.cwd()
    logger = setup_logger(project_root)

    logger.info("=== migrate_engine iniciado ===")
    logger.info("Proyecto: %s", project_name)
    logger.info("Project root: %s", project_root)

    orc_apps_path = (
        project_root
        / "backend"
        / "projects"
        / project_name
        / "config"
        / "settings"
        / "orc_apps.py"
    )

    logger.info("Leyendo orc_apps desde %s", orc_apps_path)

    apps = get_orc_apps(orc_apps_path)

    logger.info("Apps detectadas: %s", ", ".join(apps))

    # Nueva estructura canónica:
    # [(app_name, { model_name: { "fks": [...] } })]
    apps_models: list[tuple[str, dict[str, dict]]] = []

    for app in apps:
        logger.info("Procesando app: %s", app)

        models = get_app_models(project_root, app)

        app_models: dict[str, dict] = {}

        if not models:
            logger.info("  - sin modelos migrables")
            apps_models.append((app, app_models))
            continue

        for model in models:
            logger.info("  - modelo: %s", model)

            fks = get_model_fks(project_root, app, model)

            app_models[model] = {
                "fks": fks
            }

            logger.info("    FK %s -> %s", model, fks)

        apps_models.append((app, app_models))

    # Logging estructural final (clave para validar)
    logger.info("=== Estructura apps_models construida ===")
    for app, models in apps_models:
        logger.info("App: %s", app)
        if not models:
            logger.info("  (sin modelos)")
            continue
        for model, data in models.items():
            logger.info("  %s -> fks: %s", model, data["fks"])

    print_apps_models(apps_models)

    logger.info("=== migrate_engine finalizado ===")

def print_apps_models(
    apps_models: list[tuple[str, dict[str, dict]]]
) -> None:

    print("\n=== Estructura apps_models construida ===")

    for app, models in apps_models:
        print(f"\nApp: {app}")

        if not models:
            print("  (sin modelos migrables)")
            continue

        for model, meta in models.items():
            fks = meta.get("fks", [])

            if not fks:
                print(f"  - {model}")
            else:
                print(f"  - {model}")
                for fk in fks:
                    print(f"      FK -> {fk}")

if __name__ == "__main__":
    project_name = sys.argv[1] if len(sys.argv) > 1 else None
    main(project_name)
