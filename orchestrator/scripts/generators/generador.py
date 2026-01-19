import sys
from orchestrator.scripts.generators.changelog import (
    generate_constant_model_changelog,
)
from orchestrator.scripts.generators.paths import REPO_ROOT
from orchestrator.utils.naming import to_snake_case
from orchestrator.utils.logger import get_logger

log = get_logger("orc.generate")

def main():
    app_name = sys.argv[1]
    model_name = sys.argv[2]

    generate_changelogs(app_name, model_name)

    print("[GEN] done")

def generate_changelogs(app_name:str, model_name:str):
    print(f"[GEN] changelog {model_name} ({app_name})")

    schema_xml, data_xml, history_xml = generate_constant_model_changelog(
        app_name, model_name
    )

    if not schema_xml:
        raise RuntimeError("No se generó el changelog del modelo")

    # --------------------------------------------------
    # Paths (idénticos a PowerShell)
    # --------------------------------------------------
    project_root = REPO_ROOT
    output_dir = (
        project_root
        / "liquibase"
        / "changelog"
        / "apps"
        / app_name
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    model_snake=to_snake_case(model_name)

    # --------------------------------------------------
    # schema
    # --------------------------------------------------
    schema_file = output_dir / f"{model_snake}.xml"
    schema_file.write_text(schema_xml.strip() + "\n", encoding="utf-8")

    print(f"[GEN] schema  -> {schema_file}")

    # --------------------------------------------------
    # data (opcional)
    # --------------------------------------------------
    if data_xml:
        data_file = output_dir / f"{model_snake}-data.xml"
        data_file.write_text(data_xml.strip() + "\n", encoding="utf-8")

        print(f"[GEN] data    -> {data_file}")

    # --------------------------------------------------
    # history (opcional)
    # --------------------------------------------------
    if history_xml:
        history_file = output_dir / f"{model_snake}-hist.xml"
        history_file.write_text(history_xml.strip() + "\n", encoding="utf-8")

        print(f"[GEN] history -> {history_file}")

if __name__ == "__main__":
    main()
