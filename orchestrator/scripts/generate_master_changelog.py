from pathlib import Path
from generators.paths import REPO_ROOT, LIQUIBASE_CHANGELOG_APPS
from utils.naming import to_snake_case
from execution_plan import ExecutionPlan

def generate_master_changelog(
    project_name: str,
    execution_plan: ExecutionPlan,
    logger
) -> None:
    """
    Genera el changelog maestro del proyecto, incluyendo en orden:
    0. Inicializaciones por app (init.xml)
    1. La estructura completa de la base de datos.
    2. Las cargas de datos distribuidas entre las apps.
    """
    master_path = get_master_path(project_name)
    master_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Generando master changelog en %s", master_path)

    lines: list[str] = ["databaseChangeLog:"]

    # 0. Inicializaciones (PostGIS, extensiones, schemas, etc.)
    include_init_changelogs(
        execution_plan,
        lines,
        logger
    )

    # 1. Estructura
    apps_in_order = include_structural_changelogs(
        execution_plan,
        lines,
        logger
    )
    
    # 2. Datos
    include_data_changelogs(
        apps_in_order,
        lines,
        logger
    )

    master_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("master.yaml generado correctamente")


def include_structural_changelogs(
    execution_plan: ExecutionPlan,
    lines: list[str],
    logger
) -> list[str]:
    """
    Incluye los changelogs estructurales (modelo e histórico) siguiendo
    el orden de dependencias del execution plan.

    Retorna la lista de apps involucradas, en orden y sin duplicados.
    """
    apps_seen: list[str] = []

    for app, model in execution_plan:
        if app not in apps_seen:
            apps_seen.append(app)

        app_dir = (
            REPO_ROOT
            / "liquibase"
            / "changelog"
            / "apps"
            / app
        )

        base_name = to_snake_case(model)

        for suffix in ("", "-hist"):
            changelog_file = app_dir / f"{base_name}{suffix}.xml"
            if changelog_file.exists():
                include_changelog(
                    changelog_file,
                    lines,
                    logger,
                    f"{app}.{base_name}{suffix}"
                )

    return apps_seen

def include_changelog(changelog_file, lines, logger, label):
    """
    Construye las inclusiones del changelog maestro del proyecto a partir del
    plan de ejecución de modelos.

    La función es responsable de:
    - Incluir todos los changelogs estructurales (modelo e histórico) de los
        modelos del proyecto, respetando el orden de dependencias calculado.
    - Incluir posteriormente los changelogs de datos asociados a esos modelos,
        permitiendo que los datos estén distribuidos en múltiples apps.

    El resultado garantiza que:
    - La estructura de la base de datos se crea completamente antes de aplicar
        cualquier carga de datos.
    - El changelog maestro refleja la composición real del proyecto, sin asumir
        que los datos de un modelo viven en una única app.

    Esta función no decide dependencias ni genera changelogs; únicamente
    orquesta su inclusión en el orden correcto dentro del master changelog.
    """
    relative_path = changelog_file.relative_to(
        REPO_ROOT / "liquibase" / "changelog"
    )

    include_path = Path("..") / ".." / relative_path

    logger.info("Incluyendo %s -> %s", label, include_path.as_posix())

    lines.append("  - include:")
    lines.append(f"      file: {include_path.as_posix()}")
    lines.append("      relativeToChangelogFile: true")

def include_data_changelogs(
    apps_ordered: list[str],
    lines: list[str],
    logger
) -> None:
    """
    Incluye todos los changelogs de datos (*-data.xml) de las apps
    participantes, asegurando que la estructura ya fue creada.
    """
    apps_dir = REPO_ROOT / "liquibase" / "changelog" / "apps"

    for app in apps_ordered:
        app_dir = apps_dir / app
        if not app_dir.exists():
            continue

        for changelog_file in sorted(app_dir.glob("*-data.xml")):
            include_changelog(
                changelog_file,
                lines,
                logger,
                f"{app}.{changelog_file.name}"
            )

def get_master_path(project_name:str):
    '''
    Indica la ubicación del master changelog a generarse
    
    :param project_name: Nombre  del proyecto
    :type project_name: str
    '''
    return (
        REPO_ROOT
        / "liquibase"
        / "changelog"
        / "generated"
        / project_name
        / "master.yaml"
    )

def include_init_changelogs(
    execution_plan: ExecutionPlan,
    lines: list[str],
    logger
) -> None:
    """
    Incluye los init.xml de las apps, si existen.
    Se ejecutan antes de cualquier estructura.
    """
    logger.info("Incluyendo inicializaciones por app (init.xml)")

    for app in execution_plan.apps():
        init_path = LIQUIBASE_CHANGELOG_APPS / app / "initial.xml"
        if init_path.exists():
            logger.info("Incluyendo init.xml de app %s", app)
            lines.append(f"  - include:")
            lines.append(f"      file: ../../apps/{app}/initial.xml")
            lines.append(f"      relativeToChangelogFile: true")
