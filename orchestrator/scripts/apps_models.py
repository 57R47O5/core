from typing import Dict, List, Tuple, Iterator


class AppsModels:
    def __init__(self):
        self._data: Dict[str, Dict[str, dict]] = {}

    def add_app(self, app: str):
        self._data.setdefault(app, {})

    def add_model(self, app: str, model: str, meta: dict):
        self.add_app(app)
        self._data[app][model] = meta

    def apps(self) -> List[str]:
        return list(self._data.keys())

    def models(self, app: str) -> Dict[str, dict]:
        return self._data.get(app, {})

    def items(self) -> Iterator[Tuple[str, Dict[str, dict]]]:
        return self._data.items()

    def __iter__(self):
        return iter(self._data.items())

    def __str__(self):
        lines = ["=== AppsModels ==="]
        for app, models in self._data.items():
            lines.append(f"App: {app}")
            for model, meta in models.items():
                lines.append(f"  {model} -> {meta}")
        return "\n".join(lines)
