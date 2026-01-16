# orc/generators/rest_controller.py

from generators.rest_controller import generate_rest_controller


def run(model_name: str, app_name: str):
    generate_rest_controller(
        model_name=model_name,
        app_name=app_name
    )
