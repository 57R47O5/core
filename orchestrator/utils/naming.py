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

def to_pascal_case(name: str) -> str:
    """
    Convierte un nombre en snake_case / kebab-case / lowercase
    a PascalCase.

    Ejemplos:
    - moneda -> Moneda
    - tipo_cambio -> TipoCambio
    - http_status_code -> HttpStatusCode
    - tipo-cambio -> TipoCambio
    """
    if not name:
        return ""

    # Normalizamos separadores a _
    normalized = re.sub(r"[-\s]+", "_", name)

    parts = normalized.split("_")

    return "".join(
        part[:1].upper() + part[1:].lower()
        for part in parts
        if part
    )
