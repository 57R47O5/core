import logging
import sys
from typing import Optional


def get_logger(
    name: str = "orco",
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Devuelve un logger configurado para el orco.

    - Salida por stdout
    - Formato consistente
    - Evita handlers duplicados
    """

    logger = logging.getLogger(name)

    # Evitar reconfigurar si ya existe
    if logger.handlers:
        return logger

    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger
