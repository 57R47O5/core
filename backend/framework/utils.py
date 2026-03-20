import io
import pandas as pd

def leer_archivo(file):
    formato = detectar_formato(file)

    file.seek(0)
    content = file.read()

    if formato == "xlsx":
        return pd.read_excel(io.BytesIO(content), engine="openpyxl")

    if formato == "xls":
        return pd.read_excel(io.BytesIO(content), engine="xlrd")

    if formato == "csv":
        return leer_csv(content)

    raise Exception("Formato no soportado")

def detectar_formato(file):
    file.seek(0)
    header = file.read(4)
    file.seek(0)

    # XLSX (zip)
    if header.startswith(b'PK'):
        return "xlsx"

    # CSV / texto
    try:
        sample = file.read(200).decode("utf-8")
        file.seek(0)
        if "," in sample or ";" in sample:
            return "csv"
    except:
        pass

    # fallback
    return "xls"

def leer_csv(content):
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            return pd.read_csv(
                io.BytesIO(content),
                encoding=encoding,
                sep=";"
            )
        except UnicodeDecodeError:
            continue

    raise Exception("No se pudo decodificar el CSV")