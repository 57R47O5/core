from pathlib import Path

def generate_frontend_app(
    app_name: str,
    *,
    frontend_apps_path: str,
):
    app_dir = Path(frontend_apps_path) / app_name

    if app_dir.exists():
        raise RuntimeError(f"Frontend app '{app_name}' ya existe")

    # --------------------------------------------------
    # Estructura base
    # --------------------------------------------------
    (app_dir / "pages").mkdir(parents=True)
    (app_dir / "components").mkdir()
    (app_dir / "hooks").mkdir()

    # --------------------------------------------------
    # api.js
    # --------------------------------------------------
    api_content = f"""\
import getAPIBase from "@/api/BaseAPI";

const API = getAPIBase("/{app_name}");

export default API;
"""
    (app_dir / "api.js").write_text(api_content, encoding="utf-8")

    # --------------------------------------------------
    # routes.jsx
    # --------------------------------------------------
    routes_content = f"""\
export default [
  {{
    path: "/{app_name}",
    element: <div>{app_name} works</div>,
  }},
];
"""
    (app_dir / "routes.jsx").write_text(routes_content, encoding="utf-8")

    # --------------------------------------------------
    # index.js
    # --------------------------------------------------
    index_content = """\
import routes from "./routes";

export default {
  routes,
};
"""
    (app_dir / "index.js").write_text(index_content, encoding="utf-8")
