from pathlib import Path
from execution_plan import ExecutionPlan
import re


def camel_to_snake(name: str) -> str:
    """
    UserRol        -> user_rol
    ModeloPrueba   -> modelo_prueba
    XMLHTTPParser -> xmlhttp_parser
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def generate_master_changelog(
    project_name: str,
    execution_plan: ExecutionPlan,
    logger
) -> None:
    
    project_root = Path.cwd()

    master_path = (
        project_root
        / "liquibase"
        / "changelog"
        / "generated"
        / project_name
        / "master.yaml"
    )

    master_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Generando master changelog en %s", master_path)

    lines: list[str] = []
    lines.append("databaseChangeLog:")

    for app, model in execution_plan:
        app_dir = (
            project_root
            / "liquibase"
            / "changelog"
            / "apps"
            / app
        )

        base_name = camel_to_snake(model)

        candidates = [
            f"{base_name}.xml",
            f"{base_name}-data.xml",
            f"{base_name}-hist.xml",
        ]

        for filename in candidates:
            changelog_file = app_dir / filename

            if not changelog_file.exists():
                continue

            relative_path = changelog_file.relative_to(
                project_root / "liquibase" / "changelog"
            )

            logger.info(
                "Incluyendo %s.%s -> %s",
                app,
                base_name,
                relative_path.as_posix()
            )

            lines.append(f"  - include:")
            lines.append(f"      file: {relative_path.as_posix()}")
            lines.append(f"      relativeToChangelogFile: false")

    master_path.write_text("\n".join(lines), encoding="utf-8")

    logger.info("master.yaml generado correctamente")
