import sys
from orchestrator.scripts.generators.changelog import (
    generate_historical_model_changelog,
    generate_model_changelog,
    generate_liquibase_initial_data,
)
from orchestrator.scripts.generators.domain_model_definition import (
    load_domain_model_definition, 
    DomainModelDefinition,
    )
from orchestrator.scripts.generators.rest_controller import generate_rest_controller
from orchestrator.scripts.generators.serializer import generate_serializer
from orchestrator.scripts.generators.rest_urls import generate_rest_urls
from orchestrator.scripts.generators.urls import generate_urls
from orchestrator.scripts.generators.tests import generate_model_tests
from orchestrator.scripts.generators.paths import REPO_ROOT
from orchestrator.utils.logger import get_logger
from orchestrator.scripts.generators.frontend_form_generator import generate_frontend_form, generate_frontend_filter
from orchestrator.scripts.generators.frontend_formpage_generator import generate_form_page
from orchestrator.scripts.generators.frontend_list_page_generator import generate_frontend_list_page


log = get_logger("orc.generate")

def main():
    app_name = sys.argv[1]
    model_name = sys.argv[2]

    definition = load_domain_model_definition(app_name, model_name)
    #generate_changelogs(definition)
    generate_rest_controller(definition)
    generate_serializer(definition)
    generate_urls(definition)
    generate_rest_urls(app_name)
    generate_model_tests(definition)

    # Frontend

    generate_form_page(definition)
    generate_frontend_form(definition)
    generate_frontend_filter(definition)
    # generate_frontend_list_page(model_name, fields, base_frontend_path)


    print("[GEN] done")

def generate_changelogs(definition:DomainModelDefinition):
    print(f"[GEN] changelog {definition.model_name} ({definition.app_name})")

    schema_xml = generate_model_changelog(definition)

    data_xml = (
        generate_liquibase_initial_data(definition)
        if definition.has_initial_data
        else None
    )

    history_xml = (
        generate_historical_model_changelog(definition)
        if definition.has_history
        else None
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
        / definition.app_name
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # schema
    # --------------------------------------------------
    schema_file = output_dir / f"{definition.model_name}.xml"
    schema_file.write_text(schema_xml.strip() + "\n", encoding="utf-8")

    print(f"[GEN] schema  -> {schema_file}")

    # --------------------------------------------------
    # data (opcional)
    # --------------------------------------------------
    if data_xml:
        data_file = output_dir / f"{definition.model_name}-data.xml"
        data_file.write_text(data_xml.strip() + "\n", encoding="utf-8")

        print(f"[GEN] data    -> {data_file}")

    # --------------------------------------------------
    # history (opcional)
    # --------------------------------------------------
    if history_xml:
        history_file = output_dir / f"{definition.model_name}-hist.xml"
        history_file.write_text(history_xml.strip() + "\n", encoding="utf-8")

        print(f"[GEN] history -> {history_file}")

if __name__ == "__main__":
    main()
