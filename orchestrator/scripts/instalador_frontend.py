import subprocess
from typing import Union, Sequence
import os
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]

BACKEND_PROJECTS_DIR = REPO_ROOT / "backend" / "projects"
FRONTEND_PROJECTS_DIR = REPO_ROOT / "frontend" / "proyectos"

def patch_vite_config(project_dir: Path):
    vite_config = project_dir / "vite.config.js"

    if not vite_config.exists():
        raise FileNotFoundError(
            f"No se encontró vite.config.js en {project_dir}"
        )

    vite_config_content = """\
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

// Reconstruir __dirname en ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 3000,
  },
  plugins: [react()],
  resolve: {
    alias: {
      "@apps": path.resolve(__dirname, "../../src/apps"),
    },
  },
});
"""

    vite_config.write_text(vite_config_content, encoding="utf-8")


def run(cmd: Union[str, Sequence[str]], cwd=None, env=None, input_text=None, **kwargs):
    """
    Ejecuta un comando del sistema mostrando stdout/stderr.
    Falla inmediatamente si el comando devuelve error.

    - Si cmd es str → se ejecuta vía shell
    - Si cmd es lista → ejecución directa (recomendado)
    """
    print("dentro de run")
    print("→", cmd if isinstance(cmd, str) else " ".join(cmd))

    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        shell=isinstance(cmd, str),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout, stderr = process.communicate(input=input_text)

    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    if process.returncode != 0:
        raise RuntimeError(f"❌ Comando falló ({process.returncode})")


def create_frontend_project(project_name):
    project_dir = FRONTEND_PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    if any(project_dir.iterdir()):
        raise RuntimeError("El directorio frontend no está vacío")

    env = os.environ.copy()
    env["CI"] = "true"

    run(
    ["npx.cmd", "create-vite", ".", "--template", "react"],
    cwd=project_dir, env=env,
    )
    run(["npm.cmd", "install"], cwd=project_dir, env=env)

    patch_vite_config(project_dir)

    return project_dir

def main():
    if len(sys.argv) < 2:
        print("Uso: generador_proyectos.py <project_name>", file=sys.stderr)
        sys.exit(1)

    project_name = sys.argv[1]

    create_frontend_project(project_name)

if __name__ == "__main__":
    main()