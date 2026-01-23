import os
from orchestrator.scripts.generators.domain_model_definition import DomainModelDefinition
from orchestrator.scripts.generators.paths import FRONTEND_DIR
from orchestrator.scripts.utils.naming import to_snake_case

# ============================================================
#  GENERADOR DEL FORM 
# ============================================================
def generate_model_route(definition:DomainModelDefinition):
    model_route_folder = FRONTEND_DIR / "src" / "apps" / definition.app_name / "routes"
    os.makedirs(model_route_folder, exist_ok=True)

    file_path = f"{model_route_folder}/{definition.model_name}Route.jsx"

    content = f"""
import {definition.ModelName}ListPage from "../{definition.model_name}/{definition.ModelName}ListPage";
import {definition.ModelName}FormPage from "../{definition.model_name}/{definition.ModelName}FormPage";

const {definition.model_name}Routes = [
    {{
        path: "/{definition.model_name.replace("_","-")}",
        element: <{definition.ModelName}ListPage />,
    }},
    {{
        path: "/{definition.model_name.replace("_","-")}/:id",
        element: <{definition.ModelName}FormPage />,
    }},
    {{
        path: "/{definition.model_name.replace("_","-")}/nuevo",
        element: <{definition.ModelName}FormPage />,
    }}
];

export default {definition.model_name}Routes
"""
    
    with open(file_path, "w", encoding="utf-8") as field:
        field.write(content)

    print("✅ Router del modelo generado:", file_path)
