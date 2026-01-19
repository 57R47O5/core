import re


def to_snake_case(name: str) -> str:
    """
    Convierte un nombre de modelo en CamelCase / PascalCase
    a snake_case en minúsculas.

    Ejemplos:
    - Moneda -> moneda
    - TipoCambio -> tipo_cambio
    - HTTPStatusCode -> http_status_code
    """
    if not name:
        return ""

    # ABCWord -> ABC_Word
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    # wordWord -> word_Word
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)

    return s2.lower()
