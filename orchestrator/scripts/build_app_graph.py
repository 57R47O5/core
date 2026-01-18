from typing import Dict, List, Tuple, Iterator, Set
from apps_models import AppsModels

def build_app_graph(apps_models: AppsModels) -> Dict[str, Set[str]]:
    app_graph: Dict[str, Set[str]] = {
        app: set() for app in apps_models.apps()
    }

    for app, models in apps_models:
        for model, meta in models.items():
            for fk in meta.get("fks", []):
                if fk.startswith("ex-"):
                    dep_app = fk.replace("ex-", "")
                    app_graph[app].add(dep_app)

    return app_graph
