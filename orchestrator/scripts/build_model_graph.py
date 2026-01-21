from typing import Dict, Set

def build_model_graph(app_models: Dict[str, dict]) -> Dict[str, Set[str]]:
    model_graph: Dict[str, Set[str]] = {
        model: set() for model in app_models
    }

    for model, meta in app_models.items():
        for fk in meta.get("fks", []):
            # solo dependencias internas
            if fk in app_models:
                model_graph[model].add(fk)

    return model_graph
