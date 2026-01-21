from typing import List
from execution_plan import AppNode, ModelNode, ExecutionPlan
from build_app_graph import build_app_graph
from build_model_graph import build_model_graph
from topo_sort_apps import topo_sort_apps

def build_execution_plan(
    apps_models: list[tuple[str, dict[str, dict]]]
) -> ExecutionPlan:

    # Ordenar apps
    app_graph = build_app_graph(apps_models)
    print(f"app_graph es:  {app_graph}")
    apps_sorted = topo_sort_apps(app_graph)

    apps_models_map = {
        app: models
        for app, models in apps_models
    }

    app_nodes: List[AppNode] = []

    for app in apps_sorted:
        models = apps_models_map.get(app, {})

        if not models:
            app_nodes.append(AppNode(name=app, models=[]))
            continue

        model_graph = build_model_graph(models)
        models_sorted = topo_sort_apps(model_graph)

        model_nodes = [
            ModelNode(
                name=model,
                fks=models[model].get("fks", [])
            )
            for model in models_sorted
        ]

        app_nodes.append(
            AppNode(
                name=app,
                models=model_nodes
            )
        )

    return ExecutionPlan(app_nodes)
