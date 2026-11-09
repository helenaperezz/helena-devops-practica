# Imagen base ligera con Python 3.12
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Evita ficheros .pyc y muestra los logs al instante
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Primero copiamos solo las dependencias para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias sin guardar caché (imagen más pequeña)
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente
COPY src/ .

# Creamos un usuario sin privilegios y le damos permisos sobre el código
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Puerto en el que escucha la API
EXPOSE 8000

# Comando de inicio
CMD ["python", "main.py"]
