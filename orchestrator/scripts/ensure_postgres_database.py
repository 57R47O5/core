import subprocess
import os


def run_psql(command: str, db, database="postgres"):
    env = os.environ.copy()
    env["PGPASSWORD"] = db["password"]

    cmd = [
        "psql",
        "-h", db["host"],
        "-p", str(db.get("port", 5432)),
        "-U", db["user"],
        "-d", database,
        "-t",
        "-c", command,
    ]

    result = subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True,
    )

    return result

def ensure_postgres_database(context):
    db = context["database"]

    print(f"🐘 Verificando base de datos '{db['name']}'...")

    check_sql = (
        "SELECT 1 FROM pg_database "
        f"WHERE datname = '{db['name']}';"
    )

    result = run_psql(check_sql, db)

    if result.returncode != 0:
        raise RuntimeError(
            f"No se pudo verificar la base de datos:\n{result.stderr}"
        )

    if result.stdout.strip() == "1":
        print(f"✅ La base '{db['name']}' ya existe")
        return

    print("⚠️  La base no existe. Creándola...")

    create_sql = f"CREATE DATABASE {db['name']};"
    result = run_psql(create_sql, db)

    if result.returncode != 0:
        raise RuntimeError(
            f"❌ No se pudo crear la base '{db['name']}':\n{result.stderr}"
        )

    print(f"✅ Base de datos '{db['name']}' creada correctamente")
