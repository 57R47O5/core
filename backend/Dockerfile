FROM python:3.14

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta base
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requirements primero (para cache)
COPY projects/elecciones/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos TODO el backend (incluye apps + projects)
COPY . .

#  MUY IMPORTANTE: path de Python
ENV PYTHONPATH=/app

# Nos movemos al proyecto Django
WORKDIR /app/projects/elecciones

EXPOSE 8000

CMD ["gunicorn", "elecciones.wsgi:application", "--bind", "0.0.0.0:8000"]