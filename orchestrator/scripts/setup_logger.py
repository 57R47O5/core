from pathlib import Path
import logging
import sys

def setup_logger(project_root: Path) -> logging.Logger:
    log_file = project_root / "migrate_engine.log"

    logger = logging.getLogger("migrate_engine")
    logger.setLevel(logging.INFO)

    # evitar duplicados si se importa
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
