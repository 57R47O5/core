"""
Script maestro para generar automáticamente:
- RestController
- Serializers
- URLs
- Form (React)
- Filter (React)
- FormPage (React)
- ListPage (React)

Guía al usuario paso a paso para recopilar datos.
"""

import re
import os
from generators.rest_controller import generate_rest_controller
from generators.serializer import generate_serializer
from generators.urls import generate_urls
from generators.frontend_form_generator import generate_frontend_form, generate_frontend_filter
from generators.frontend_formpage_generator import generate_form_page
from generators.frontend_list_page_generator import generate_frontend_list_page
from scripts.django_model_analyzer import analyze_django_model


def main():
    print("\n=== Generador Automático Django + React ===\n")

    # --- diálogo interactivo ---
    app_name = input("👉 Ingrese el nombre de la app (ej: carteles): ").strip()
    model_name = input("👉 Ingrese el nombre del modelo en PascalCase (ej: Paciente): ").strip()

    if not app_name or not model_name:
        print("\n❌ ERROR: Debe ingresar app_name y model_name.\n")
        return

    # --- rutas basadas en tu estructura real ---
    base_backend_dir = "backend/apps"
    model_file_name = (
        model_name[0].lower() +
        re.sub(r"([A-Z])", lambda m: "_" + m.group(1).lower(), model_name[1:]) +
        ".py"
    )

    model_path = os.path.join(
        base_backend_dir,
        app_name,
        "models",
        model_file_name
    )

    if not os.path.exists(model_path):
        print(f"\n❌ ERROR: No se encontró el archivo del modelo: {model_path}")
        return

    # Analizar modelo
    fields = analyze_django_model(model_path, model_name)

    # Base del frontend
    base_frontend_path = "frontend/src/componentes"

    print("\n🚀 Generando archivos...\n")

    # --- generación backend ---
    generate_rest_controller(app_name, model_name)
    generate_serializer(app_name, model_name)
    generate_urls(app_name, model_name)

    # --- generación frontend ---
    generate_form_page(model_name)
    generate_frontend_form(model_name, fields, base_frontend_path)
    generate_frontend_filter(model_name, fields, base_frontend_path)
    generate_frontend_list_page(model_name, fields, base_frontend_path)

    print("\n✅ PROCESO COMPLETADO")
    print(f"Archivos generados correctamente para el modelo {model_name} en la app {app_name}.\n")


if __name__ == "__main__":
    main()
