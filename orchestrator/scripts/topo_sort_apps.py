from typing import Dict, Set, List


class AppDependencyCycleError(Exception):
    pass


def topo_sort_apps(app_graph: Dict[str, Set[str]]) -> List[str]:
    visited: Set[str] = set()
    visiting: Set[str] = set()
    result: List[str] = []

    def visit(app: str):
        if app in visited:
            return

        if app in visiting:
            raise AppDependencyCycleError(
                f"Ciclo detectado en dependencias de apps: {app}"
            )

        visiting.add(app)

        for dep in app_graph.get(app, []):
            visit(dep)

        visiting.remove(app)
        visited.add(app)
        result.append(app)

    for app in app_graph:
        if app not in visited:
            visit(app)

    return result
