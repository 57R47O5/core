from dataclasses import dataclass
from typing import Dict, List, Iterator, Tuple


@dataclass(frozen=True)
class ModelNode:
    name: str
    fks: List[str]


@dataclass(frozen=True)
class AppNode:
    name: str
    models: List[ModelNode]

class ExecutionPlan:
    def __init__(self, apps: List[AppNode]):
        self._apps = apps

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """
        Itera en el orden real de ejecución:
        (app_name, model_name)
        """
        for app in self._apps:
            for model in app.models:
                yield app.name, model.name

    def __repr__(self) -> str:
        lines = ["ExecutionPlan:"]
        for app in self._apps:
            lines.append(f"  App: {app.name}")
            for model in app.models:
                lines.append(f"    - {model.name} (fks: {model.fks})")
        return "\n".join(lines)

    def apps(self) -> List[str]:
        return [app.name for app in self._apps]

    def models_for_app(self, app_name: str) -> List[str]:
        for app in self._apps:
            if app.name == app_name:
                return [m.name for m in app.models]
        return []

